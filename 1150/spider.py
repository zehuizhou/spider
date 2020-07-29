import os
import re
import sys
import time
import pandas as pd
import requests
from parsel import Selector
from fake_useragent import UserAgent


ua = UserAgent(verify_ssl=False)


# 当前目录路径
DIR_PATH = os.path.dirname(os.path.abspath(__file__))

# 存图片的文件夹的路径
IMG_PATH = DIR_PATH + '/img/'

common_headers = {
    'Accept': '*/*',
    'Host': 'movie.douban.com',
    'User-Agent': ua.random
}

proxy_url = 'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=4bf26f6bdaf1978df580d617a2cffff0&orderNo=GL20200131152126nmVxqyej&count=1&isTxt=0&proxyType=1'

def download(img_name, img_url):
    """
    下载表情到本地
    :param img_name: 保存图片的名称
    :param img_url: 图片的链接
    :return:
    """
    try:
        pic = requests.get(img_url, timeout=3)
        # 保存图片路径
        path = IMG_PATH + img_name
        fp = open(path, 'wb')
        fp.write(pic.content)
        fp.close()
        print(f'图片下载成功~~'.center(70, '-'))
    except requests.exceptions.ConnectionError:
        print('图片下载失败！！'.center(70, '-'))


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


def celebrity_spider(key):
    url = 'https://movie.douban.com/j/subject_suggest?q={}'.format(key)

    def get_res(count):
        if count < 0:
            return
        try:
            with open('pro.txt', 'r') as f:
                proxy = eval(f.read())
            ret = requests.get(url=url, headers=common_headers, proxies=proxy, timeout=6).json()
            r = ret[0]
            return ret
        except Exception as e:
            print(e)
            change_proxy(3)
            return get_res(count - 1)

    res = get_res(1)
    print(11111111111)
    print(res)
    print(11111111111)
    if res:
        cele = []
        for r in res:
            if r['type'] == 'celebrity':
                cele.append(r)
        return cele


def info_spider(c):
    url = 'https://movie.douban.com/celebrity/{}/'.format(c['id'])

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
    item['姓名'] = c['title']
    item['id'] = c['id']
    item['海报'] = c['img']
    download(img_name=item['id']+'.jpg', img_url=item['海报'])
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

    with open('names', encoding='utf-8') as file:
        names = file.read().splitlines()

    for n in range(8, len(names)):
        celebrity_list = celebrity_spider(names[n])
        if celebrity_list is not None:
            for celebrity in celebrity_list:
                data = info_spider(celebrity)
                print(111)
                print(data)
                print(222)
                save_to_csv(file_name='影人', list_dict=data)
        print(f'第 {n} 位保存成功'.center(100, '-'))

