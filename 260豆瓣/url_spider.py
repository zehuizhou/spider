import requests
import re
import time
from constants import change_proxy, save_list_dict
from lxml import html
"""
电视剧数据：
电视剧名称，导演（爬取第一个），主演（爬取所有，每个之间按照&&号分隔），类型（爬取所有，每个之间按照&&号分隔），制片国家/地区（爬第一个），年份（只要年份，不要月日），评分，评价人数

电影数据：
电影名称，导演（爬取第一个），主演（爬取所有的，每个之间用&&隔开），类型（爬取所有的，每个之间用&&隔开），制片国家/地区（爬取第一个），时长（注意这个字段和电视剧不一样，电视剧是年份，这个是时长），评分，评价人数
"""
etree = html.etree

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'movie.douban.com',
    'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; viewed="26836700_27667375_27028517_26801374_1013208"; push_doumail_num=0; push_noty_num=0; ct=y; __utma=30149280.1397345246.1575978668.1587368117.1588729373.58; __utmc=30149280; __utmz=30149280.1588729373.58.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1588729373; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588729391%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1128099318.1575978668.1587365563.1588729391.32; __utmb=223695111.0.10.1588729391; __utmc=223695111; __utmz=223695111.1588729391.32.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.32.1588729414.1587365570.'
}


def tv_url_spider(page):
    url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电视剧&start={}'.format(page*20)

    def get_ret(retry_count):
        if retry_count < 0:
            return
        try:
            with open('pro.txt', 'r') as fi:
                proxy = eval(fi.read())
            r = requests.get(url=url, headers=header, proxies=proxy, timeout=6).json()
            u = r['data']
            return r
        except:
            change_proxy(3)
            return get_ret(retry_count-1)

    ret = get_ret(3)
    data = ret['data']
    for d in data:
        url = d['url']
        with open('tv_url.txt', 'a') as f:
            f.write(url + '\n')
    print(ret)


def mv_url_spider(page):
    url = 'https://movie.douban.com/j/new_search_subjects?sort=U&range=0,10&tags=电影&start={}'.format(page*20)

    def get_ret(retry_count):
        if retry_count < 0:
            return
        try:
            with open('pro.txt', 'r') as fi:
                proxy = eval(fi.read())
            r = requests.get(url=url, headers=header, proxies=proxy, timeout=6).json()
            u = r['data']
            return r
        except:
            change_proxy(3)
            return get_ret(retry_count-1)

    ret = get_ret(3)
    data = ret['data']
    for d in data:
        url = d['url']
        with open('mv_url.txt', 'a') as f:
            f.write(url + '\n')
    print(ret)


if __name__ == '__main__':
    change_proxy(1)
    for i in range(500, 501):
        mv_url_spider(i)
        print(f'{i}保存成功'.center(70, '-'))
        time.sleep(1)
