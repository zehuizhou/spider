import sys
import requests
import re
import time
from constants import change_proxy, save_list_dict
from fake_useragent import UserAgent
from parsel import Selector


def search(keyword):
    url = 'https://www.douban.com/search?q={}'.format(keyword)
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Host': 'www.douban.com',
        'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; viewed="26836700_27667375_27028517_26801374_1013208"; push_doumail_num=0; push_noty_num=0; ct=y; __utma=30149280.1397345246.1575978668.1587368117.1588729373.58; __utmc=30149280; __utmz=30149280.1588729373.58.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1588729373; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588729391%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1128099318.1575978668.1587365563.1588729391.32; __utmb=223695111.0.10.1588729391; __utmc=223695111; __utmz=223695111.1588729391.32.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.32.1588729414.1587365570.'
    }

    def get_list(retry_count):
        if retry_count < 0:
            sys.exit()
        try:
            with open('pro.txt', 'r') as fi:
                proxy = eval(fi.read())
            html = requests.get(url=url, headers=header, proxies=proxy, timeout=6).content.decode()

            return html
        except:
            change_proxy(2)
            return get_list(retry_count - 1)

    html = get_list(3)
    root = Selector(html)
    div_list = root.xpath("//div[@class='result']")
    need_list = []

    for div in div_list:
        item = {}
        onclick = div.xpath(".//div[@class='title']/h3/a/@onclick").get('')
        item['关键词'] = keyword
        item['id'] = re.findall('sid: (.*?), qcat', onclick)[0] if re.findall('sid: (.*?), qcat', onclick) else ''
        item['类型'] = div.xpath(".//div[@class='title']/h3/span/text()").get('').replace('[', '').replace(']', '').replace('\n', '').replace(' ', '')
        item['标题'] = div.xpath(".//div[@class='title']/h3/a/text()").get('')
        item['评分'] = div.xpath(".//div[@class='title']/div[@class='rating-info']/span[2]/text()").get('')
        text = div.xpath(".//div[@class='title']/div[@class='rating-info']/span[3]/text()").get('')
        item['评价人数'] = re.findall('\((.*?)人评价\)', text)[0] if re.findall('\((.*?)人评价\)', text) else ''
        introduction = div.xpath(".//div[@class='title']/div[@class='rating-info']/span[@class='subject-cast']/text()").get('')
        year = introduction.split(' / ')[-1]
        item['年份'] = re.findall('\d+', year)[0] if re.findall('\d+', year) else ''
        item['简介'] = introduction
        item['链接'] = div.xpath(".//div[@class='title']/h3/a/@href").get('')
        # if item['类型'] not in ['小组', '']:
        need_list.append(item)
        print(item)
    return need_list


if __name__ == '__main__':

    with open('keywords') as f:
        url_list = f.read().splitlines()
    for key in url_list:
        data = search(key)
        save_list_dict('2016', data)
        print(f'{key} 保存成功'.center(70, '-'))
        time.sleep(0.2)
