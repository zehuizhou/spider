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
    'Host': 'sa.sogou.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:46.0) Gecko/20100101 Firefox/46.0',
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate',
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Requested-With': 'XMLHttpRequest',
    'Connection': 'keep-alive'
}


def spider(province):
    ret = requests.get(url='http://sa.sogou.com/new-weball/api/sgs/epidemic/area-charts/data?province={}&_=0.27756390370126893'.format(province), headers=web_header).json()
    print(ret)

    increased_list = [province]
    x = ret['all']['x']
    s = ret['all']['series'][1]['data']

    for i in range(0, len(x)):
        province = province
        date = x[i]['value']
        if type(s[i]) is dict:
            increased = s[i]['value']
        else:
            increased = s[i]
        increased_list += [increased]


    return [increased_list]


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
    pro_list = ['湖北', '广东', '河南', '浙江', '湖南', '安徽', '江西', '山东', '江苏', '重庆', '四川', '黑龙江',
                '北京', '上海', '河北', '福建', '广西', '陕西', '云南', '海南', '贵州', '天津', '山西', '辽宁',
                '香港', '吉林', '甘肃', '新疆', '内蒙古', '宁夏', '台湾', '青海', '澳门', '西藏']
    for pro in pro_list:
        data = spider(pro)
        save_data(filename='2', data=data)
        print('################################################')
        print(pro)
        print('################################################')
