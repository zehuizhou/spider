import requests
import re
import time
from constants import change_proxy, save_list_dict
from parsel import Selector


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'movie.douban.com',
    'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; viewed="26836700_27667375_27028517_26801374_1013208"; push_doumail_num=0; push_noty_num=0; ct=y; __utma=30149280.1397345246.1575978668.1587368117.1588729373.58; __utmc=30149280; __utmz=30149280.1588729373.58.29.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; __utmb=30149280.1.10.1588729373; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1588729391%2C%22https%3A%2F%2Fwww.douban.com%2F%22%5D; _pk_ses.100001.4cf6=*; __utma=223695111.1128099318.1575978668.1587365563.1588729391.32; __utmb=223695111.0.10.1588729391; __utmc=223695111; __utmz=223695111.1588729391.32.14.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/; ap_v=0,6.0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.32.1588729414.1587365570.'
}

url = 'https://movie.douban.com/subject/6982558/reviews?start={}'


def spider(p):

    ret = requests.get(url=url.format(20*p), headers=header, proxies=proxy, timeout=6).content.decode()
    root = Selector(ret)
    div_list = root.xpath("//div[@class='review-list  ']/div")

    need = []
    for div in div_list:
        item = {}
        comment_id = re.findall('\d+', div.xpath(".//div[@class='main-bd']/h2/a/@href").get(''))[0]
        item['评价人'] = div.xpath(".//a[@class='name']/text()").get('')
        item['评分'] = div.xpath(".//span[contains(@class,'main-title-rating')]/@title").get('')
        item['时间'] = div.xpath(".//span[@class='main-meta']/text()").get('')
        item['摘要'] = div.xpath(".//div[@class='main-bd']/h2/a/text()").get('')

        detail_url = 'https://movie.douban.com/j/review/{}/full'.format(comment_id)

        de_ret = requests.get(url=detail_url, headers=header, timeout=6).json()
        de_root = Selector(de_ret['html'])
        item['全文'] = de_root.xpath("string(/)").get('')
        item['有用'] = de_ret['votes']['useful_count']
        item['没用'] = de_ret['votes']['useless_count']
        item['回应'] = div.xpath(".//a[@class='reply ']/text()").get('').replace('回应', '')
        need.append(item)
        print(item)
    return need


if __name__ == '__main__':
    for page in range(0, 500):
        d = spider(page)
        save_list_dict('长城影评', d)
        print(page)

