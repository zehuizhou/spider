import requests
import re
import time
from constants import change_proxy, save_list_dict
from lxml import html
"""
电视剧数据：
电视剧名称，导演（爬取第一个），主演（爬取所有，每个之间按照&&号分隔），类型（爬取所有，每个之间按照&&号分隔），
制片国家/地区（爬第一个），年份（只要年份，不要月日），评分，评价人数

电影数据：
电影名称，导演（爬取第一个），主演（爬取所有的，每个之间用&&隔开），类型（爬取所有的，每个之间用&&隔开），制片国家/地区（爬取第一个），
时长（注意这个字段和电视剧不一样，电视剧是年份，这个是时长），评分，评价人数
"""
etree = html.etree

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'movie.douban.com',
    'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; viewed="26836700_27667375_27028517_26801374_1013208"; push_doumail_num=0; push_noty_num=0; ct=y; __utma=30149280.1397345246.1575978668.1587368117.1588729373.58; __utmc=30149280; __utmz=30149280.1588729373.58.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1588729373; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588729391%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1128099318.1575978668.1587365563.1588729391.32; __utmb=223695111.0.10.1588729391; __utmc=223695111; __utmz=223695111.1588729391.32.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.32.1588729414.1587365570.'
}


def tv_spider(movie_url):
    """
    爬取电影信息
    :param movie_url: 传入电影的地址
    :return: 返回电影信息列表，格式[(),(),()]
    """
    item = {}

    def get_movie(retry_count):
        try:
            with open('pro.txt', 'r') as fi:
                proxy = eval(fi.read())
            html = requests.get(url=movie_url, headers=header, proxies=proxy, timeout=6).content.decode()
            html_e = etree.HTML(html)  # 获取element 类型的html
            a = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0]
            return html, html_e
        except:
            # change_proxy(2)
            time.sleep(3)
            return get_movie(retry_count-1)

    all = get_movie(3)
    html = all[0]
    html_e = all[1]
    item['电视剧名称'] = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0].split(' ')[0]
    # item['贴图'] = html_e.xpath("//a[@class='nbgnbg']/img/@src")[0]
    dy = html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()")[0] if html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()") else ''
    item['导演'] = dy.split('/')[0].replace(' ', '')   #  有些电影没有这些内容，所有try下，不存在就为''
    # item['编剧'] = html_e.xpath("string(//*[@id='info']/span[2]/span[2])").replace(' / ', '&&')
    item['主演'] = html_e.xpath("string(//*[@id='info']/span[@class='actor']/span[@class='attrs'])").replace('更多...', '').replace(' / ', '&&')
    item['类型'] = '&&'.join(html_e.xpath("//*[@id='info']/span[@property='v:genre']/text()"))
    try:
        country = re.findall('.*<span class="pl">制片国家/地区:</span>(.*)<br/>', html)[0]
        item['制片国家/地区'] = country.split('/')[0].replace(' ', '')
    except:
        item['制片国家/地区'] = ''
    try:
        year = html_e.xpath("//span[@class='year']/text()")[0]
        movie_year = re.findall(r'\d+', year)[0]
    except:
        movie_year = ''
    item['年份'] = movie_year
    item['评分'] = html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()")[0] if html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()") else ''

    try:
        movie_rating_people = html_e.xpath("//*[@id='interest_sectl']//span[@property='v:votes']/text()")[0]
        movie_rating_people = re.findall(r'\d+', movie_rating_people)[0]
    except:
        movie_rating_people = ''
    item['评价人数'] = movie_rating_people



    try:
        movie_runtime = html_e.xpath("//*[@id='info']/span[@property='v:runtime']/text()")[0]
    except:
        movie_runtime = ''
    # item['时长'] = movie_runtime
    # item['简介'] = html_e.xpath("string(//*[@id='link-report']/span[1])").replace(' ', '').replace('\n', '')
    # item['链接'] = movie_url
    print(item)
    return [item]


if __name__ == '__main__':
    change_proxy(1)
    with open('tv_url.txt') as f:
        url_list = f.read().splitlines()
    for url in url_list:
        data = tv_spider(url)
        save_list_dict('电视', data)
        print(f'{url} 保存成功'.center(70, '-'))

