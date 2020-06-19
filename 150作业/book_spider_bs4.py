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
    i = 1
    need_list = []
    for page in range(0, 10):
        url = 'https://book.douban.com/top250?start={}'.format(page*25)
        request_headers = {'Host': 'book.douban.com',
                           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                           'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmv=30149280.20803; douban-profile-remind=1; douban-fav-remind=1; push_doumail_num=0; push_noty_num=0; ct=y; viewed="4429032_19936010_3426869_26836700_27667375_27028517_26801374_1013208"; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03=431205b1-0128-48b6-994f-2ae5d5606ee4; gr_cs1_431205b1-0128-48b6-994f-2ae5d5606ee4=user_id%3A0; _pk_ref.100001.3ac3=%5B%22%22%2C%22%22%2C1592014263%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D_aGfGvbnawbxhoIUygYnPYxvhO8pw8qYot3VYqxaawWbwKbBkcvQddD0Woi3eWrK%26wd%3D%26eqid%3Db19747da000ac5a7000000045ee435b3%22%5D; _pk_ses.100001.3ac3=*; __utma=30149280.1397345246.1575978668.1591924927.1592014263.76; __utmc=30149280; __utmz=30149280.1592014263.76.36.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt_douban=1; __utma=81379588.499073742.1576573344.1591862725.1592014263.10; __utmc=81379588; __utmz=81379588.1592014263.10.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; gr_session_id_22c937bbd8ebd703f2d8e9445f7dfd03_431205b1-0128-48b6-994f-2ae5d5606ee4=true; Hm_lvt_cfafef0aa0076ffb1a7838fd772f844d=1592014273; Hm_lpvt_cfafef0aa0076ffb1a7838fd772f844d=1592014273; ap_v=0,6.0; _pk_id.100001.3ac3=cb9003205ecd012f.1576573344.10.1592014502.1591862725.; __utmb=30149280.8.10.1592014263; __utmb=81379588.8.10.1592014263'}
        html = requests.get(url=url, headers=request_headers).content.decode()
        time.sleep(random.uniform(1, 3.9))
        html = BeautifulSoup(html, 'lxml')

        # 创建CSS选择器，获取 珞珈新闻 标题
        table_list = html.select('div[class="indent"] table')
        print(len(table_list))

        for table in table_list:
            item = {}
            item['序号'] = i
            item['小说名'] = table.select("div[class='pl2'] a")[0]['title']
            item['评分'] = table.select("span[class='rating_nums']")[0].get_text()
            item['评分人数'] = re.findall('\d+', table.select("span[class='pl']")[0].get_text())[0]
            pl = table.select("p[class='pl']")[0].get_text().split('/')
            item['出版社'] = pl[-3]
            item['作者'] = '，'.join(pl[:-3])
            i += 1
            need_list.append(item)

            print(item)
    df = pd.DataFrame(need_list)
    df.to_excel('book.xlsx', encoding='utf_8_sig', index=False)


if __name__ == "__main__":
    spider()
