import time
import pymysql
import requests
import re
from parsel import Selector

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'movie.douban.com',
    'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; viewed="26836700_27667375_27028517_26801374_1013208"; push_doumail_num=0; push_noty_num=0; ct=y; __utma=30149280.1397345246.1575978668.1587368117.1588729373.58; __utmc=30149280; __utmz=30149280.1588729373.58.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1588729373; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588729391%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1128099318.1575978668.1587365563.1588729391.32; __utmb=223695111.0.10.1588729391; __utmc=223695111; __utmz=223695111.1588729391.32.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.32.1588729414.1587365570.'
}


def movie_spider():
    """
    爬取电影信息
    :return: 返回电影信息列表
    """
    movie_list = []

    movie_url_list = ['https://movie.douban.com/subject/24847340/',
                      'https://movie.douban.com/subject/1302827/',
                      'https://movie.douban.com/subject/1291580/',
                      'https://movie.douban.com/subject/4301224/',
                      'https://movie.douban.com/subject/2336785/']
    for movie_url in movie_url_list:
        html = requests.get(url=movie_url, headers=header, timeout=6).content.decode()
        html_e = Selector(html)  # 获取element 类型的html
        time.sleep(1)
        id = re.findall('\d+', movie_url)[0]
        name = html_e.xpath("//*[@id='content']/h1/span[1]/text()").get('')
        picture_url = html_e.xpath("//a[@class='nbgnbg']/img/@src").get('')
        dy = html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()").get('')
        director = dy.split('/')[0].replace(' ', '')
        type = ' / '.join(html_e.xpath("//*[@id='info']/span[@property='v:genre']/text()").getall()).replace(' / ', ' ')
        score = html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()").get('')
        introduction = html_e.xpath("string(//*[@id='link-report']/span[1])").get('').replace(' ', '').replace('\n', '')
        movie_url = movie_url

        movie_info = (id, name, picture_url, director, type, score, introduction, movie_url)
        print(movie_info)
        movie_list.append(movie_info)
    return movie_list


def save_data(data):
    # 创建一个数据库
    pc = pymysql.connect(host="118.89.90.148", port=3306, user="root", password="123456").cursor()
    pc.execute("DROP DATABASE IF EXISTS test")
    pc.execute("CREATE DATABASE test")
    pc.close()
    # 打开数据库连接，使用 cursor() 方法创建一个游标对象 cursor
    db = pymysql.connect(host="118.89.90.148", port=3306, user="root", password="123456", db="test")

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS yyq")

    # "id, name, author, press, imgurl, comment"
    # 使用预处理语句创建表
    sql = """CREATE TABLE `yyq` (
              `id` bigint(11) NOT NULL,
              `name` varchar(255) DEFAULT NULL,
              `picture_url` varchar(255) DEFAULT NULL,
              `director` varchar(255) DEFAULT NULL,
              `type` varchar(255) DEFAULT NULL,
              `score` varchar(255) DEFAULT NULL,
              `introduction` varchar(512) DEFAULT NULL,
              `movie_url` varchar(512) DEFAULT NULL,
              PRIMARY KEY (`id`)
          ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;"""

    cursor.execute(sql)

    # SQL 插入语句
    sql = "INSERT INTO yyq(id, name, picture_url, director, type, score, introduction, movie_url) \
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        # 执行sql语句
        cursor.executemany(sql, data)
        # 执行sql语句
        db.commit()
    except Exception as e:
        # 发生错误时回滚
        print(e)
        db.rollback()

    # 关闭数据库连接
    db.close()


if __name__ == '__main__':
    movie = movie_spider()
    print('开始存数据')
    save_data(data=movie)
