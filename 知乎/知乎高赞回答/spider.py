#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  @Time    : 2020-09-08 15:26
#  @Author  : July
import time
import re
import requests
from parsel import Selector
from tools import save_to_mysql

ranking = 1

def topics_spider(page):
    """
    爬话题
    :param page: Starting from 0
    :return:
    """
    request_url = 'https://www.zhihu.com/node/TopicsPlazzaListV2'
    form_data = {
        'method': 'next',
        'params': '{"topic_id":1761,"offset":' + str(page*20) + ',"hash_id":"964365661497994e5626e45e26170192"}'
    }
    request_headers = {
        'accept': '*/*',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36'
    }
    res = requests.post(request_url, data=form_data, headers=request_headers).json()
    msg = res.get('msg')
    topics_data = []
    for m in msg:
        root = Selector(m)
        item = {}
        item['id'] = re.findall('\d+', root.xpath("//div[@class='blk']/a/@href").get(''))[0]
        item['title'] = root.xpath("//div[@class='blk']/a/strong/text()").get('')
        item['img_url'] = root.xpath("//div[@class='blk']/a/img/@src").get('')
        global ranking
        item['ranking'] = ranking
        ranking += 1
        topics_data.append(item)
    print(topics_data)
    return topics_data


if __name__ == '__main__':
    for p in range(0,50):
        td = topics_spider(p)
        save_to_mysql('topic', td)
        time.sleep(6)
