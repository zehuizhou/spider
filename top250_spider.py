import requests
from lxml import html
import csv
import time
import random
import re

etree = html.etree

# 全局的cookie，如果cookie过期了就修改下
cookie = 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; push_doumail_num=0; push_noty_num=0; ap_v=0,6.0; __utma=30149280.1397345246.1575978668.1576055296.1576458938.9; __utmz=30149280.1576458938.9.3.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=30149280; dbcl2="208034392:Sl/YiLV4Zx0"; ck=pyPv; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1576460119%2C%22https%3A%2F%2Faccounts.douban.com%2Fpassport%2Flogin%22%5D; _pk_id.100001.8cb4=2b01f89a590b449c.1576025283.3.1576460119.1576056053.; _pk_ses.100001.8cb4=*; __utmt=1; __utmv=30149280.20803; __utmb=30149280.2.10.1576458938'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'movie.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}


def top250_subject_url_spider():
    """
    获取电影详情地址
    :return:
    """
    top250_subject_url_list = []
    print("正在获取电影详情地址。。。")
    for page in range(25):
        top250_url = 'https://movie.douban.com/top250?start={}&filter='.format(page * 25)
        html_top250 = requests.get(url=top250_url, headers=common_header).content.decode()
        time.sleep(random.randint(0, 3))
        html_t = etree.HTML(html_top250)
        div_li_list = html_t.xpath("//ol[@class='grid_view']/li")
        for i in div_li_list:
            top250_subject_url = i.xpath("./div/div/a/@href")[0]
            top250_subject_url_list.append(top250_subject_url)
    print(f"电影详情地址个数：{len(top250_subject_url_list)},电影详情地址列表：{top250_subject_url_list}")
    time.sleep(random.randint(0, 3))
    return top250_subject_url_list


def movie_spider(movie_url):
    """
    爬电影数据
    :return:
    """
    html = requests.get(url=movie_url, headers=common_header).content.decode()
    html_e = etree.HTML(html)  # 获取element 类型的html

    movie_name = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0]
    movie_director = html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()")[0]
    try:
        movie_attr = html_e.xpath("string(//*[@id='info']/span[@class='actor']/span[@class='attrs'])")
    except:
        movie_attr = ''
    movie_country = re.findall('.*<span class="pl">制片国家/地区:</span>(.*)<br/>', html)[0]
    try:
        year = html_e.xpath("//span[@class='year']/text()")[0]
        movie_year = re.findall(r'\d+', year)[0]
    except:
        movie_year = ''
    movie_rate = html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()")[0]
    try:
        movie_type = str(html_e.xpath("//*[@id='info']/span[@property='v:genre']/text()")).replace('[', '').replace(']',
                                                                                                                    '')
    except:
        movie_type = ''
    movie_eva = html_e.xpath("//div[@id='comments-section']/div[1]/h2/span/a/text()")[0]
    movie_evaluate = re.findall(r'\d+', movie_eva)[0]

    total_list = [
        [movie_name, movie_rate, movie_director, movie_attr, movie_year, movie_country, movie_type, movie_evaluate]
    ]

    print(total_list)
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
    url_list = top250_subject_url_spider()

    for url in url_list:
        data = movie_spider(url)
        save_data('top250movie', data)
        time.sleep(random.randint(0, 6))


if __name__ == '__main__':
    main()
