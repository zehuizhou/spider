import sys
import requests
import re
import time
from constants import change_proxy, save_list_dict
from fake_useragent import UserAgent
from lxml import html
from parsel import Selector


# ua = UserAgent(verify_ssl=False)

etree = html.etree

header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'movie.douban.com',
    'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; viewed="26836700_27667375_27028517_26801374_1013208"; push_doumail_num=0; push_noty_num=0; ct=y; __utma=30149280.1397345246.1575978668.1587368117.1588729373.58; __utmc=30149280; __utmz=30149280.1588729373.58.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1588729373; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588729391%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1128099318.1575978668.1587365563.1588729391.32; __utmb=223695111.0.10.1588729391; __utmc=223695111; __utmz=223695111.1588729391.32.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.32.1588729414.1587365570.'
}


def movie_spider(movie_id, en_name):
    """
    爬取电影信息
    :param movie_url: 传入电影的地址
    :return: 返回电影信息列表
    """
    item = {}
    movie_url = 'https://movie.douban.com/subject/' + str(movie_id) + '/'

    def get_movie(retry_count):
        if retry_count < 0:
            sys.exit()
        try:
            with open('pro.txt', 'r') as fi:
                proxy = eval(fi.read())
            html = requests.get(url=movie_url, headers=header, proxies=proxy, timeout=6).content.decode()
            html_e = Selector(html)  # 获取element 类型的html
            a = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0]
            return html, html_e
        except:
            change_proxy(2)
            return get_movie(retry_count - 1)

    all = get_movie(3)
    html = all[0]
    html_e = all[1]
    item['英文名'] = en_name
    item['movie_id'] = movie_id
    item['电影名称'] = html_e.xpath("//*[@id='content']/h1/span[1]/text()").get('')
    item['贴图'] = html_e.xpath("//a[@class='nbgnbg']/img/@src").get('')
    dy = html_e.xpath("//*[@id='info']/span[1]/span[2]/a/text()").get('')
    item['导演'] = dy.split('/')[0].replace(' ', '')
    item['编剧'] = html_e.xpath("string(//*[@id='info']/span[2]/span[2])").get('')
    item['主演'] = html_e.xpath("string(//*[@id='info']/span[@class='actor']/span[@class='attrs'])").get('').replace('更多...', '')
    item['类型'] = ' / '.join(html_e.xpath("//*[@id='info']/span[@property='v:genre']/text()").getall())
    try:
        country = re.findall('.*<span class="pl">制片国家/地区:</span>(.*)<br/>', html)[0]
        item['制片国家/地区'] = country.split('/')[0].replace(' ', '')
    except:
        item['制片国家/地区'] = ''

    item['语言'] = re.findall('.*<span class="pl">语言:</span>(.*)<br/>', html)[0] if re.findall('.*<span class="pl">语言:</span>(.*)<br/>', html) else ''
    item['上映日期'] = ' / '.join(html_e.xpath("//span[@property='v:initialReleaseDate']/text()").getall())
    item['又名'] = re.findall('.*span class="pl">又名:</span>(.*)<br/>', html)[0] if re.findall('.*span class="pl">又名:</span>(.*)<br/>', html) else ''
    item['IMDb链接'] = re.findall('.*<span class="pl">IMDb链接:</span> <a href="(.*)" target', html)[0] if re.findall('.*<span class="pl">IMDb链接:</span> <a href="(.*)" target', html) else ''
    item['片长'] = ' / '.join(html_e.xpath("//*[@id='info']/span[@property='v:runtime']/text()").getall())
    try:
        year = html_e.xpath("//span[@class='year']/text()").get('')
        movie_year = re.findall(r'\d+', year)[0]
    except:
        movie_year = ''
    item['年份'] = movie_year
    item['评分'] = html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()").get('')

    try:
        movie_rating_people = html_e.xpath("//*[@id='interest_sectl']//span[@property='v:votes']/text()").get('')
        movie_rating_people = re.findall(r'\d+', movie_rating_people)[0]
    except:
        movie_rating_people = ''
    item['评价人数'] = movie_rating_people
    item['短评数'] = re.findall('.*comments\?status=P">全部 (.*) 条</a>', html)[0] if re.findall('.*comments\?status=P">全部 (.*) 条</a>', html) else ''
    item['影评数'] = html_e.xpath("//a[@href='reviews']/text()").get('').replace('全部 ', '').replace(' 条', '')
    item['简介'] = html_e.xpath("string(//*[@id='link-report']/span[1])").get('').replace(' ', '').replace('\n', '')
    item['链接'] = movie_url
    print(item)
    return [item]


if __name__ == '__main__':
    change_proxy(1)
    with open('ids') as f:
        id_list = f.read().splitlines()

    with open('ids_name') as f:
        name_list = f.read().splitlines()

    for i, n in zip(id_list, name_list):
        data = movie_spider(i, n)
        save_list_dict('2016电影', data)
        print(f'{i} 保存成功'.center(70, '-'))

