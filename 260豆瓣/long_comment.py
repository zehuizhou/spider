import re
import time
import pandas as pd
import requests
import os
import sys
from parsel import Selector


header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.79 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Host': 'movie.douban.com',
    'Cookie': 'll="108258"; bid=ZL0GiLd0nOE; __utma=30149280.932882661.1591671703.1591671703.1591671703.1; __utmz=30149280.1591671703.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=30149280; __utmt=1; dbcl2="210057328:O8IkcR5ba2o"; ck=xNVX; push_doumail_num=0; push_noty_num=0; __utmv=30149280.21005; douban-profile-remind=1; __utmb=30149280.5.10.1591671703; _pk_ses.100001.4cf6=*; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1591671828%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F210057328%2F%22%5D; __utma=223695111.128435007.1591671828.1591671828.1591671828.1; __utmb=223695111.0.10.1591671828; __utmc=223695111; __utmz=223695111.1591671828.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/210057328/; __yadk_uid=EctSpcJPiHayHNCQxYBOmttZhvJC2JuW; _pk_id.100001.4cf6=fbfbf6b4ac6fc975.1591671828.1.1591671833.1591671828.'
}

url = 'https://movie.douban.com/subject/27605698/reviews?start={}'


def spider(p):

    ret = requests.get(url=url.format(20*p), headers=header, timeout=6).content.decode()
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
        time.sleep(1)
        de_ret = requests.get(url=detail_url, headers=header, timeout=6).json()
        de_root = Selector(de_ret['html'])
        item['全文'] = de_root.xpath("string(/)").get('')
        item['有用'] = de_ret['votes']['useful_count']
        item['没用'] = de_ret['votes']['useless_count']
        item['回应'] = div.xpath(".//a[@class='reply ']/text()").get('').replace('回应', '')
        need.append(item)
        print(item)
    return need


def save_to_csv(file_name, list_dict):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name + '.csv')
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


if __name__ == '__main__':
    for page in range(0, 500):
        d = spider(page)
        save_to_csv('西红柿首富影评', d)
        print(page)

