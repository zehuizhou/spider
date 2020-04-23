from bs4 import BeautifulSoup
import requests


def spider():
    url = 'http://www.whu.edu.cn/'
    html = requests.get(url).content
    html = BeautifulSoup(html, 'lxml')

    # 创建CSS选择器，获取 珞珈新闻 标题
    ul = html.select('div[class="panel"] div ul[class="list-unstyled list"]')[0]
    li = ul.select('li a')
    print('珞珈新闻标题如下：')
    for a in li:
        print(a['title'])

    # 创建CSS选择器，获取 学术动态 标题
    ul = html.select('div[class="panel"] div ul[class="list-unstyled list"]')[1]
    li = ul.select('li a')
    print('学术动态标题如下：')
    for a in li:
        print(a['title'])

    # 创建CSS选择器，获取 通知公告 标题
    ul = html.select('div[class="panel"] div ul[class="list-unstyled list"]')[2]
    li = ul.select('li a')
    print('通知公告标题如下：')
    for a in li:
        print(a['title'])

if __name__ == "__main__":
   spider()