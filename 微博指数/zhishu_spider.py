# -*- coding: utf-8 -*-
import csv
import os
import sys

import requests
from fake_useragent import UserAgent
from urllib import parse
import json

ua = UserAgent(verify_ssl=False)

web_header = {
    'Host': 'data.weibo.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Referer': 'https://data.weibo.com/index/newindex?visit_type=trend&wid=1091324210225',
    'Cookie': 'UOR=www.baidu.com,data.weibo.com,www.baidu.com; SINAGLOBAL=1213237876483.9214.1464074185942; ULV=1464183246396:2:2:2:3463179069239.6826.1464183246393:1464074185944; DATA=usrmdinst_12; _s_tentry=www.baidu.com; Apache=3463179069239.6826.1464183246393; WBStore=8ca40a3ef06ad7b2|undefined; PHPSESSID=3mn5oie7g3cm954prqan14hbg5',
    'Connection': 'keep-alive'
}

data = {
    'wid': '1091324210225',
    'dateGroup': '3month'
}

ret = requests.post(url='https://data.weibo.com/index/ajax/newindex/getchartdata', data=data, headers=web_header).json()

x = ret['data'][0]['trend']['x']
s = ret['data'][0]['trend']['s']
data_list = []
for i in range(0, 92):
    date = x[i]
    zs = s[i]
    if i == 0:
        hb = '-'
    else:
        hb = str((s[i]-s[i-1])/s[i-1]*100) + '%'
    data = [date, zs, hb]
    data_list.append(data)


def get_path(file_name):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name)
    return path


def save_data(filename, data):
    path = get_path(filename + '.csv')
    if os.path.isfile(path):
        is_exist = True
    else:
        is_exist = False
    with open(path, "a", newline="", encoding="utf_8_sig") as f:
        c = csv.writer(f)
        if not is_exist:
            c.writerow(['日期', '指数', '环比'])
        for line in data:
            c.writerow(line)


if __name__ == '__main__':
    save_data(filename='旅游', data=data_list)
    print(data_list)
