import requests
from lxml import html
import re
import sqlite3
import os

etree = html.etree

# 全局的cookie，如果cookie过期了就修改下
cookie = 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; push_doumail_num=0; push_noty_num=0; __utmv=30149280.20803; ct=y; ap_v=0,6.0; __utma=30149280.1397345246.1575978668.1576653493.1576659793.18; __utmb=30149280.0.10.1576659793; __utmc=30149280; __utmz=30149280.1576659793.18.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utma=223695111.1128099318.1575978668.1576653493.1576659793.17; __utmb=223695111.0.10.1576659793; __utmc=223695111; __utmz=223695111.1576659793.17.6.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1576659795%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.16.1576659795.1576654106.; _pk_ses.100001.4cf6=*'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'book.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}
# 豆瓣图书地址列表
book_url_list = [
    'https://book.douban.com/top250?start=0',
    'https://book.douban.com/top250?start=25',
    'https://book.douban.com/top250?start=50',
    'https://book.douban.com/top250?start=75'
]


def book_spider(book_url):
    """
    爬取图书信息
    :param book_url: 图书列表页地址
    :return:
    """
    print("正在获取数据。。。")
    html = requests.get(url=book_url, headers=common_header).content.decode()
    html_e = etree.HTML(html)  # 获取element 类型的html
    total_book_list = []

    table_list = html_e.xpath("//div[@class='article']/div[@class='indent']/table")
    for table in table_list:
        book_detail_url = table.xpath(".//tr[@class='item']/td[2]/div[@class='pl2']/a/@href")[0]
        id = re.findall(r'\d+', book_detail_url)[0]
        name = table.xpath(".//tr/td/div/a/@title")[0]

        pl = table.xpath(".//tr/td/p/text()")[0].split('/')
        "[美] 卡勒德·胡赛尼 / 李继宏 / 上海人民出版社 / 2006-5 / 29.00元"
        "钱锺书 / 人民文学出版社 / 1991-2 / 19.00"
        author = '，'.join(pl[:-3])
        press = pl[-3]

        imgurl = table.xpath(".//tr/td/a/img/@src")[0]
        comment = table.xpath(".//tr/td/p/span/text()")[0] if table.xpath(".//tr/td/p/span/text()") else ''

        book_list = [id, name, author, press, imgurl, comment]
        total_book_list.append(book_list)
        print(total_book_list)

    return total_book_list


def save_data(data):
    # 连接到数据库
    # 数据库文件是“douban.db”
    # 如果数据库已经存在，会删了该数据库然后再创建，如果数据库不存在的话，将会自动创建一个数据库，
    db_file = os.path.join(os.path.dirname(__file__), 'douban.db')
    if os.path.isfile(db_file):
        os.remove(db_file)

    conn = sqlite3.connect("douban.db")

    # 创建一个游标 curson
    cursor = conn.cursor()

    # 执行一条语句,创建 user表
    sql1 = "create table BOOK (id varchar(20) primary key, imgurl varchar(255), press varchar(255), author varchar(255), name varchar(255), comment varchar(512))"

    cursor.execute(sql1)
    # 插入数据

    sql2 = "INSERT INTO BOOK(id, name, author, press, imgurl, comment) VALUES (?, ?, ?, ?, ?, ?)"
    cursor.executemany(sql2, data)

    # 提交数据到数据库
    conn.commit()

    # 查询插入的数据
    cursor.execute('select * from BOOK')
    values = cursor.fetchall()
    print(values)
    # 关闭Connection:
    conn.close()


def main():
    # 遍历电影列表获取电影数据
    totol_data = []
    for url in book_url_list:
        data = book_spider(url)
        totol_data += data
    print(totol_data)

    save_data(totol_data)


if __name__ == '__main__':
    main()
