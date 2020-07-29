import os
import re
import sys
import time
import pandas as pd
import requests
from parsel import Selector
from fake_useragent import UserAgent
from tool import download

ua = UserAgent(verify_ssl=False)


common_headers = {
    'Accept': '*/*',
    'Host': 'movie.douban.com',
    'User-Agent': ua.random
}

proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=4bf26f6bdaf1978df580d617a2cffff0&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'




def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}

        with open('pro.txt', 'w') as f:
            f.write(str(proxies))

        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


def save_to_csv(file_name, list_dict):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name + '.csv')
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


def info_spider(celebrity_id):
    url = 'https://movie.douban.com/celebrity/{}/'.format(celebrity_id)

    def get_res(count):
        if count < 0:
            sys.exit()
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())
            ret = requests.get(url=url, headers=common_headers, proxies=proxy, timeout=6).content.decode()
            return ret
        except Exception as e:
            print(e)
            change_proxy(3)
            return get_res(count - 1)

    res = get_res(3)
    root = Selector(res)
    item = {}
    item['姓名'] = root.xpath("//div[@id='content']/h1/text()").get('')
    item['id'] = celebrity_id
    item['海报'] = root.xpath("//div[@class='pic']/a[@class='nbg']/@href").get('')

    download(img_name=str(item['id'])+'.jpg', img_url=item['海报'])
    li_list = root.xpath("//div[@class='info']/ul/li")
    item['性别'], item['星座'], item['出生日期'], item['生卒日期'], item['出生地'], item['职业'] = '', '', '', '', '', ''
    for li in li_list:
        item[li.xpath("./span/text()").get('')] = li.xpath("./text()[2]").get('').replace('\n', '').replace(':', '').strip()
    if '更多外文名' in item:
        del item['更多外文名']
    if '更多中文名' in item:
        del item['更多中文名']
    if '家庭成员' in item:
        del item['家庭成员']
    if 'imdb编号' in item:
        del item['imdb编号']
    if '官方网站' in item:
        del item['官方网站']

    item['简介'] = ''.join(root.xpath("//div[@class='bd']/span[@class='all hidden']/text()").getall()).replace('\n', '').strip() \
        if root.xpath("//div[@class='bd']/span[@class='all hidden']") \
        else ''.join(root.xpath("//div[@class='bd']/text()").getall()).replace('\n', '').strip()
    item['影片id'] = movies_spider(item['id'])

    return [item]


def movies_spider(uid):
    url = 'https://movie.douban.com/celebrity/{}/movies?start=0&format=pic&sortby=time'.format(uid)

    def get_res(count):
        if count < 0:
            sys.exit()
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())
            ret = requests.get(url=url, headers=common_headers, proxies=proxy, timeout=6).content.decode()
            return ret
        except Exception as e:
            print(e)
            change_proxy(3)
            return get_res(count - 1)

    res = get_res(3)
    root = Selector(res)
    count = int(re.findall('\d+', str(root.xpath("//span[@class='count']/text()").get(0)))[0])
    total_page = count//10 + 1
    print(f'总页数为 {total_page} '.center(50, '-'))
    movie_ids = []
    for page in range(0, total_page):
        url = 'https://movie.douban.com/celebrity/{}/movies?start={}&format=pic&sortby=time'.format(uid, page*10)

        def get_res(count):
            if count < 0:
                sys.exit()
            try:
                with open('pro.txt', 'r') as f:
                    proxy = eval(f.read())
                ret = requests.get(url=url, headers=common_headers, proxies=proxy, timeout=6).content.decode()
                return ret
            except Exception as e:
                print(e)
                change_proxy(3)
                return get_res(count - 1)

        res = get_res(3)
        root = Selector(res)
        movie_urls = root.xpath("//div[@class='grid_view']/ul/li/dl/dt/a/@href").getall()
        movie_id = map(lambda x: re.findall('\d+', x)[0], movie_urls)
        movie_ids += movie_id
        print(f'第 {page} 爬取成功'.center(50, '-'))

    return movie_ids


if __name__ == '__main__':
    # change_proxy(2)

    for n in range(1412860, 1416000):
        data = info_spider(n)
        print(data)
        save_to_csv(file_name='影人', list_dict=data)
        print(f'第 {n} 位保存成功'.center(100, '-'))

