import requests
from lxml import html
import time
import random
import re
import pymysql

etree = html.etree

# https://movie.douban.com/subject/34805219/comments?start=0&limit=20&sort=new_score&status=P 登录后，复制cookie粘贴到下面，如果cookie过期了就修改下
cookie = 'll="118172"; bid=3Dh0xsyFmwA; __yadk_uid=RgXyFoVawO6nKmoMUaqWL7NSloLWBHSR; trc_cookie_storage=taboola%2520global%253Auser-id%3Da77d4d48-6454-4c13-8867-dfb5f48d677b-tuct40ce95c; __gads=ID=f56a861753a9f791:T=1562376536:S=ALNI_MZcqCAYVy-Sr1ZtdMwnxfLirn38vw; _ga=GA1.2.646133900.1561181775; _vwo_uuid_v2=DD418FAC2AAD807406F1064CEE9D2A086|855479519c9a30fec64b0408ee39390b; gr_user_id=9743cda7-6f6a-4884-a8e3-fc3513ebf3a8; douban-fav-remind=1; __utmv=30149280.20803; viewed="1950970_1857022"; __utma=30149280.646133900.1561181775.1584869372.1585984471.39; __utmc=30149280; __utmz=30149280.1585984471.39.22.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="208034392:nEbsTJjvIbI"; ck=Y4MR; push_noty_num=0; push_doumail_num=0; douban-profile-remind=1; __utmb=30149280.23.9.1585984522535; __utma=223695111.1353761110.1561181775.1584869372.1585984527.56; __utmb=223695111.0.10.1585984527; __utmc=223695111; __utmz=223695111.1585984527.56.43.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1585984527%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DbLmgwDm6m-uvSsFQbHjrPiqmIb-v0XibTpK8YhVJVNI-ZtjFCiTg--jPlvXxu-oa%26wd%3D%26eqid%3Db3dbba3d00182c2b000000045e8833d3%22%5D; _pk_ses.100001.4cf6=*; ct=y; _pk_id.100001.4cf6=8a270c8a38b2c16e.1561181775.56.1585984649.1584869371.'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'movie.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}


def movie_url_spider():
    for page in range(0, 10):
        top250_url = 'https://movie.douban.com/top250?start={}&filter='.format(page*25)
        html = requests.get(url=top250_url, headers=common_header).content.decode()
        time.sleep(random.randint(1, 3))
        html_e = etree.HTML(html)  # 获取element 类型的html
        li_list = html_e.xpath("//ol[@class='grid_view']/li")
        for li in li_list:
            movie_url = li.xpath(".//div[@class='pic']/a/@href")[0]
            with open('movie_url.txt', 'a') as f:
                f.writelines(movie_url+'\n')


def movie_spider(movie_url):
    """
    爬取电影信息
    :param movie_url: 传入电影的地址
    :return: 返回电影信息列表，格式[(),(),()]
    """
    html = requests.get(url=movie_url, headers=common_header).content.decode()
    html_e = etree.HTML(html)  # 获取element 类型的html

    id = html_e.xpath("//span[@class='top250-no']/text()")[0].replace('No.', '')
    movie_name = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0]
    movie_img = html_e.xpath("//a[@class='nbgnbg']/img/@src")[0]
    movie_director = html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()")[0] if html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()") else ''
    #  有些电影没有这些内容，所有try下，不存在就为''
    movie_screenwriter = html_e.xpath("string(//*[@id='info']/span[2]/span[2])")
    movie_attr = html_e.xpath("string(//*[@id='info']/span[@class='actor']/span[@class='attrs'])").replace('更多...', '')
    movie_country = re.findall('.*<span class="pl">制片国家/地区:</span>(.*)<br/>', html)[0]
    try:
        year = html_e.xpath("//span[@class='year']/text()")[0]
        movie_year = re.findall(r'\d+', year)[0]
    except:
        movie_year = ''
    movie_rate = html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()")[0] if html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()") else ''

    try:
        movie_rating_people = html_e.xpath("//*[@id='interest_sectl']//span[@property='v:votes']/text()")[0]
        movie_rating_people = re.findall(r'\d+', movie_rating_people)[0]
    except:
        movie_rating_people = ''

    try:
        movie_type = ' '.join(html_e.xpath("//*[@id='info']/span[@property='v:genre']/text()"))
    except:
        movie_type = ''
    try:
        movie_runtime = html_e.xpath("//*[@id='info']/span[@property='v:runtime']/text()")[0]
    except:
        movie_runtime = ''
    movie_indent = html_e.xpath("string(//*[@id='link-report']/span[1])").replace(' ', '').replace('\n', '')

    total_list = [
        (
            int(id), movie_name, movie_img, movie_year, movie_rate, movie_rating_people,
            movie_director, movie_attr, movie_screenwriter,
            movie_type, movie_runtime, movie_country, movie_indent
        )
    ]

    print(total_list)
    return total_list


"""
保存到数据库的代码，如果有需要就用
"""
def create_table():
    # 打开数据库连接
    db = pymysql.connect("localhost", "root", "123456", "douban")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS movie")
    # "id, name, author, press, imgurl, comment"
    # 使用预处理语句创建表
    sql = """
           CREATE TABLE `movie` (
              `id` bigint(20) NOT NULL,
              `movie_name` varchar(255) DEFAULT NULL,
              `movie_img` varchar(255) DEFAULT NULL,
              `movie_year` varchar(255) DEFAULT NULL,
              `movie_rate` varchar(255) DEFAULT NULL,
              `movie_rating_people` varchar(255) DEFAULT NULL,
              `movie_director` varchar(2000) DEFAULT NULL,
              `movie_attr` varchar(2000) DEFAULT NULL,
              `movie_screenwriter` varchar(2000) DEFAULT NULL,
              `movie_type` varchar(255) DEFAULT NULL,
              `movie_runtime` varchar(255) DEFAULT NULL,
              `movie_country` varchar(255) DEFAULT NULL,
              `movie_indent` varchar(5000) DEFAULT NULL,
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
    sql = "INSERT INTO movie(id, movie_name, movie_img, movie_year, movie_rate, movie_rating_people,movie_director, movie_attr, movie_screenwriter, movie_type, movie_runtime, movie_country, movie_indent) \
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
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


def main():
    create_table()
    # 存电影地址到txt
    movie_url_spider()

    # 获取电影列表
    with open('movie_url.txt', 'r') as f:
        url_list = f.read().splitlines()

    for u in url_list:
        data = movie_spider(movie_url=u)
        save_data(data=data)


if __name__ == '__main__':
    main()
