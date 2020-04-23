# -*- coding: utf-8 -*-
import csv
import os
import sys
import requests
from fake_useragent import UserAgent
from lxml import html

ua = UserAgent(verify_ssl=False)

etree = html.etree

web_header = {
    'origin': 'https://news.sina.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def spider(page):
    ret = requests.get(url='https://interface.sina.cn/news/fy.piyao.d.json?size=10&page={}'.format(page), headers=web_header).json()
    need_list = []
    data_list = ret['data']
    for data in data_list:
        title = data['title']
        url = data['url']
        date = data['date']
        status = data['status']
        pic = data['pic']
        desc = data['desc']

        dl_ret = requests.get(url=url, headers=web_header).content.decode()
        root = etree.HTML(dl_ret)
        author = root.xpath("//span[@class='author']/a/text()")[0] if root.xpath("//span[@class='author']/a/text()") else ''
        print(author)
        content = '\n'.join(root.xpath("//div[@class='paragraph']//text()"))
        like_number = root.xpath("//div[@class='content']/p[@class='like_number']/span/text()")[0] if root.xpath("//p[@class='like_number']/span/text()") else ''
        imgs = '\n'.join(root.xpath("//div[@class='paragraph']//img/@src"))

        need = [title, url, date, status, pic, desc, author, content, imgs]
        print(need)
        need_list.append(need)
    return need_list


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    # now = datetime.datetime.now().replace()
    # now = str(now)[0:10].replace('-', '').replace(' ', '').replace(':', '')
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['title', 'url', 'date', 'status', 'pic', 'desc', 'author', 'content', 'imgs'])
        for line in data:
            c.writerow(line)



if __name__ == '__main__':
    for i in range(1, 200):
        data = spider(i)
        save_data(filename='新浪谣言', data=data)
        print('################################################')
        print(i)
        print('################################################')
