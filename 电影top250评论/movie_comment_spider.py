import requests
from lxml import html
import pymysql
import time
import random
import re
import os
import sys
import csv


"""
下载依赖：requests、lxml
cmd 运行：
pip install requests
pip install lxml
"""

etree = html.etree

# https://movie.douban.com/subject/34805219/comments?start=0&limit=20&sort=new_score&status=P 登录后，复制cookie粘贴到下面，如果cookie过期了就修改下
cookie = 'll="118172"; bid=3Dh0xsyFmwA; __yadk_uid=RgXyFoVawO6nKmoMUaqWL7NSloLWBHSR; trc_cookie_storage=taboola%2520global%253Auser-id%3Da77d4d48-6454-4c13-8867-dfb5f48d677b-tuct40ce95c; __gads=ID=f56a861753a9f791:T=1562376536:S=ALNI_MZcqCAYVy-Sr1ZtdMwnxfLirn38vw; _ga=GA1.2.646133900.1561181775; _vwo_uuid_v2=DD418FAC2AAD807406F1064CEE9D2A086|855479519c9a30fec64b0408ee39390b; gr_user_id=9743cda7-6f6a-4884-a8e3-fc3513ebf3a8; douban-fav-remind=1; __utmv=30149280.20803; viewed="1950970_1857022"; __utma=30149280.646133900.1561181775.1584869372.1585984471.39; __utmc=30149280; __utmz=30149280.1585984471.39.22.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="208034392:nEbsTJjvIbI"; ck=Y4MR; push_noty_num=0; push_doumail_num=0; douban-profile-remind=1; __utmb=30149280.23.9.1585984522535; __utma=223695111.1353761110.1561181775.1584869372.1585984527.56; __utmb=223695111.0.10.1585984527; __utmc=223695111; __utmz=223695111.1585984527.56.43.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1585984527%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DbLmgwDm6m-uvSsFQbHjrPiqmIb-v0XibTpK8YhVJVNI-ZtjFCiTg--jPlvXxu-oa%26wd%3D%26eqid%3Db3dbba3d00182c2b000000045e8833d3%22%5D; _pk_ses.100001.4cf6=*; ct=y; _pk_id.100001.4cf6=8a270c8a38b2c16e.1561181775.56.1585984649.1584869371.'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'movie.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}


# 爬取评论
def comment_spider(url):
    # 要存的数据列表
    data_list = []

    # 获取网页代码
    comment_html = requests.get(url=url, headers=common_header).content.decode()
    # 休眠随机0~3秒，爬被封
    time.sleep(random.randint(0, 3))
    # 转成etree树
    html_c = etree.HTML(comment_html)
    # 获取20个评论的div
    comment_item = html_c.xpath("//div[@id='comments']/div[@class='comment-item']/div[@class='comment']")
    # 遍历这20个评论div，获取想要的字段

    for item in comment_item:
        # 这个comment-time后面有个空字符，坑了我好久，T T
        id = random.randint(1000000000, 9999990000)
        datetime = item.xpath("./h3/span[@class='comment-info']/*[@class='comment-time ']/text()")[0] if item.xpath("./h3/span[@class='comment-info']/*[@class='comment-time ']/text()") else ''
        datetime = datetime.replace('\n', '').replace(' ', '')
        user_name = item.xpath("./h3/span[@class='comment-info']/a/text()")[0] if item.xpath("./h3/span[@class='comment-info']/a/text()") else '0'
        user_url = item.xpath("./h3/span[@class='comment-info']/a/@href")[0]
        user_id = re.findall(".*people/(.*)/", user_url)[0] if re.findall(".*people/(.*)/", user_url) else ''
        comment = item.xpath("./p/span/text()")[0] if item.xpath("./p/span/text()") else ''
        start = item.xpath("./h3/span[@class='comment-info']/span[2]/@title")[0]
        vote = item.xpath("./h3/span/span[@class='votes']/text()")[0]
        title = html_c.xpath("//div[@id='content']/h1/text()")[0]
        movie_url = url
        movie_id = re.findall('\d+', movie_url)[0]

        data = (id, user_id, user_name, datetime, comment, start, vote, title, movie_url, int(movie_id))
        data_list.append(data)  # 用来后续存数据用
    print(f'评论总个数{len(data_list)},评论总列表：{data_list}')
    return data_list


"""
保存到数据库的代码，如果有需要就用
"""
def create_table():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "douban")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS movie_comment")
    # "id, name, author, press, imgurl, comment"
    # 使用预处理语句创建表
    sql = """
               CREATE TABLE `movie_comment` (
                  `id` bigint(20) NOT NULL,
                  `user_id` varchar(255) DEFAULT NULL,
                  `user_name` varchar(255) DEFAULT NULL,
                  `datetime` varchar(255) DEFAULT NULL,
                  `comment` varchar(5000) DEFAULT NULL,
                  `start` varchar(255) DEFAULT NULL,
                  `vote` varchar(255) DEFAULT NULL,
                  `title` varchar(255) DEFAULT NULL,
                  `movie_url` varchar(255) DEFAULT NULL,
                  `movie_id` bigint(20) DEFAULT NULL,
                  PRIMARY KEY (`id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
          """

    cursor.execute(sql)

    # 关闭数据库连接
    db.close()


def save_data(data):
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "douban")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # SQL 插入语句
    sql = "INSERT INTO movie_comment(id, user_id, user_name, datetime, comment, start, vote, title, movie_url, movie_id) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        # 执行sql语句
        cursor.executemany(sql, data)
        # 执行sql语句
        db.commit()
    except Exception as e:
        # 发生错误时回滚
        print(e)
        print('-----------保存失败-----------')
        db.rollback()

    # 关闭数据库连接
    db.close()


# 程序入口
def start():
    # 读取 movie_url.txt 文件，获取电影链接，存放到list
    with open('movie_url.txt', 'r') as f:
        url_list = f.read().splitlines()[0:300]

    # 遍历这些电影链接，爬取评论
    for u in url_list:
        print("即将爬取： " + u)
        # 每一页20条短评，只爬第一页的数据，如想爬多点，可以改下下面的数字，比如for page in range(0, 50):
        for page in range(0, 1):
            'https://movie.douban.com/subject/30176393/'
            url = u + 'comments?start={}&limit=20&sort=new_score&status=P'.format(page * 20)
            data = comment_spider(url)
            save_data(data=data)
            print(f'------------------------第{page + 1}页,{url}的评论保存成功------------------------')


if __name__ == '__main__':
    create_table()
    start()
