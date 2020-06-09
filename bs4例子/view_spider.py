import os
import random
import re
import sys
import time
import pandas as pd
from bs4 import BeautifulSoup
import requests


def save_to_csv(file_name, list_dict):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name + '.csv')
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


def spider():
    for page in range(1, 3):
        url = 'https://you.ctrip.com/sight/hangzhou14/s0-p{}.html'.format(page)
        request_headers = {
            'cookie': '_abtest_userid=8401d222-6177-4e40-8d08-149366abd9c8; _RF1=115.238.47.230; _RSG=3iaIhyOzT00tNn9c5jJJWB; _RDG=286f5d405adf8f2126286fae667fc0dbd0; _RGUID=001df58f-2b4a-4b03-b813-4ed1662715f7; MKT_CKID=1579158186297.rtqrs.8ar4; _ga=GA1.2.1466164872.1579158187; GUID=09031150411707933324; AHeadUserInfo=VipGrade=0&VipGradeName=%C6%D5%CD%A8%BB%E1%D4%B1&UserName=&NoReadMessageCount=0; FlightIntl=Search=[%22HGH|%E6%9D%AD%E5%B7%9E(HGH)|17|HGH|480%22%2C%22HKG|%E9%A6%99%E6%B8%AF(HKG)|58|HKG|480%22%2C%222020-01-25%22%2C%222020-02-01%22]; nfes_isSupportWebP=1; ASP.NET_SessionSvc=MTAuNjAuMzUuNDR8OTA5MHxqaW5xaWFvfGRlZmF1bHR8MTU4OTAwMzI4NDkwNA; MKT_Pagesource=PC; _gid=GA1.2.1032340996.1591409906; MKT_CKID_LMT=1591409906023; gad_city=78a2062d1790b42fa1a75f591a7869b2; _bfa=1.1579158183499.2nvhzb.1.1587460765853.1591409902424.14.142.10320608806; _bfs=1.8; _jzqco=%7C%7C%7C%7C%7C1.349465944.1579158186294.1591410230572.1591410257488.1591410230572.1591410257488.0.0.0.24.24; __zpspc=9.8.1591409906.1591410257.7%232%7Cwww.baidu.com%7C%7C%7C%7C%23; appFloatCnt=7; _bfi=p1%3D290546%26p2%3D290546%26v1%3D142%26v2%3D141',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'
        }
        html = requests.get(url=url, headers=request_headers).content.decode()
        time.sleep(random.uniform(1, 3.9))
        html = BeautifulSoup(html, 'lxml')

        # 创建CSS选择器，获取 珞珈新闻 标题
        div_list = html.select('div[class="rdetailbox"]')
        print(len(div_list))

        need_list = []
        for div in div_list:
            item = {}
            item['标题'] = div.select('dl dt a')[0]['title']
            item['地址'] = div.select('dl dd')[0].get_text().replace('\n', '').strip()
            item['评分'] = div.select('ul li a strong')[0].get_text()
            item['价格'] = div.select("span[class='price']")[0].get_text().replace('¥', '') if div.select("span[class='price']") else ''
            item['点评量'] = re.findall('\d+', div.select("a[class='recomment']")[0].get_text())[0]
            item['链接'] = 'https://you.ctrip.com/' + div.select('dl dt a')[0]['href']

            need_list.append(item)

            print(item)
        save_to_csv('杭州景点', need_list)
        print(f'第{page}页保存成功'.center(100, '-'))


if __name__ == "__main__":
   spider()
