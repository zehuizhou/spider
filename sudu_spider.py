import requests
from lxml import html
import csv
import re
import time
import random

with open('b.txt', 'r') as f:
    content = f.read().splitlines()
    url_list = content

etree = html.etree
# 全局的cookie，如果cookie过期了就修改下
cookie = 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; dbcl2="166993767:SvDhHe+fb6A"; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; ct=y; ck=ZUnE; __utmc=30149280; __utmz=30149280.1575963790.15.7.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; frodotk="3886ad677f508237a99408367df186a5"; ap_v=0,6.0; __utma=30149280.184410278.1573005299.1575971720.1575976395.18; __utmt_douban=1; __utmb=30149280.13.10.1575976395'
# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'movie.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}


def movie_spider(movie_url):
    """
    爬电影数据
    :return:
    """
    html = requests.get(url=movie_url, headers=common_header).content.decode()
    html_e = etree.HTML(html)  # 获取element 类型的html
    movie_name = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0]
    movie_country = re.findall('.*<span class="pl">制片国家/地区:</span>(.*)<br/>', html)[0]
    try:
        year = html_e.xpath("//span[@class='year']/text()")[0]
        movie_year = re.findall(r'\d+', year)[0]
    except:
        movie_year = ''

    movie_sign = html_e.xpath("string(//div[@class='tags-body'])")
    movie_indent = html_e.xpath("string(//*[@id='link-report']/span[1])")
    # movie_comment = html_e.xpath("//*[@id='hot-comments']/div[1]/div/p/span/text()")[0]
    print(movie_name, movie_country, movie_year, movie_sign, movie_indent)

    total_list = [[movie_name, movie_country, movie_year, movie_sign, movie_indent]]
    return total_list




def save_data(file_name, data_list):
    """
    保存数据
    :param file_name: 文件名，不需要加后缀
    :param data_list: 写入的值,格式：[[],[],[],[],[]]
    :return:
    """
    f_name = file_name + ".csv"
    f = open(f_name, "a", newline="", encoding="utf-8")
    c = csv.writer(f)
    for i in data_list:
        c.writerow(i)


def main():
    for url in url_list:
        data = movie_spider(url)
        save_data('123', data)



if __name__ == '__main__':
    main()
