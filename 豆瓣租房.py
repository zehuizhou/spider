# -*- coding: utf-8 -*-
import time
import requests
from parsel import Selector
import zmail

"""
杭州租房小助手
"""

server = zmail.server('244776919@qq.com', 'xuzrqkazsiifbgcf')
receive_mail = ['291435861@qq.com']

web_header = {
    'Host': 'www.douban.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# 标题包含的词语
words = ['滨江', '网易', '滨兴', '华为', '丁香园', '江虹', '春波', '南岸晶都', '云际', '滨康', '西兴', '半岛国际', '铂金时代',
         '星耀鑫']

title_list = []


def spider(page):
    url = 'https://www.douban.com/group/HZhome/discussion?start={}'.format(page*25)
    ret = requests.get(url=url.format(page), headers=web_header).content.decode()

    time.sleep(1)
    root = Selector(ret)
    tr_list = root.xpath("//table[@class='olt']//tr")

    for tr in tr_list:
        if tr != tr_list[0]:
            item = {}
            title = tr.xpath("./td/a/@title").get('')
            for word in words:
                if word in title:
                    global title_list
                    if title not in title_list:
                        title_list.append(title)
                        item['标题'] = title
                        item['链接'] = tr.xpath("./td/a/@href").get('')
                        item['最后回应'] = tr.xpath("./td[@class='time']/text()").get('')

                        server.send_mail(receive_mail, {'subject': title, 'content_text': item['链接']})
                        print(item)


if __name__ == '__main__':
    while True:
        spider(1)
        time.sleep(180)

    # for i in range(0, 30):
    #     spider(i)
    #     time.sleep(6)

