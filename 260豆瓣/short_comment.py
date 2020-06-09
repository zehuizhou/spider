import pandas as pd
import requests
import os
import sys
from lxml import html
import time
import random
import re

etree = html.etree

# 全局的cookie，如果cookie过期了就修改下
cookie = 'll="108258"; bid=ZL0GiLd0nOE; __utma=30149280.932882661.1591671703.1591671703.1591671703.1; __utmz=30149280.1591671703.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=30149280; __utmt=1; dbcl2="210057328:O8IkcR5ba2o"; ck=xNVX; push_doumail_num=0; push_noty_num=0; __utmv=30149280.21005; douban-profile-remind=1; __utmb=30149280.5.10.1591671703; _pk_ses.100001.4cf6=*; _pk_ref.100001.4cf6=%5B%22%22%2C%22%22%2C1591671828%2C%22https%3A%2F%2Fwww.douban.com%2Fpeople%2F210057328%2F%22%5D; __utma=223695111.128435007.1591671828.1591671828.1591671828.1; __utmb=223695111.0.10.1591671828; __utmc=223695111; __utmz=223695111.1591671828.1.1.utmcsr=douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/people/210057328/; __yadk_uid=EctSpcJPiHayHNCQxYBOmttZhvJC2JuW; _pk_id.100001.4cf6=fbfbf6b4ac6fc975.1591671828.1.1591671833.1591671828.'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'movie.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}


def comment_spider(m_url):

    for page in range(0, 26):
        # 取前10页的评论，可以自己修改获取的页数
        comment_url = m_url + 'comments?start={}&limit=20&sort=new_score&status=P'.format(page * 20)
        print(f'正在爬第{page + 1}页,{comment_url}的评论------------------------')
        comment_html = requests.get(url=comment_url, headers=common_header).content.decode()
        time.sleep(random.randint(1, 3))
        html_c = etree.HTML(comment_html)
        comment_item = html_c.xpath("//div[@id='comments']/div[@class='comment-item']/div[@class='comment']")

        data_list = []
        for item in comment_item:
            data = {}
            data['电影名'] = html_c.xpath("//div[@id='content']/h1/text()")[0].replace(' 短评', '')
            data['时间'] = item.xpath("./h3/span[@class='comment-info']/*[@class='comment-time ']/@title")[0]
            data['昵称'] = item.xpath("./h3/span[@class='comment-info']/a/text()")[0]
            data['评论内容'] = item.xpath("./p/span/text()")[0] if item.xpath("./p/span/text()") else ''
            start_and_datetime = item.xpath("./h3/span[@class='comment-info']/span[2]/@title")[0]
            data['评分'] = re.findall('[\u4e00-\u9fa5]+', start_and_datetime)[0] if re.findall('[\u4e00-\u9fa5]+', start_and_datetime) else ''
            data['有用'] = item.xpath("./h3/span/span[@class='votes']/text()")[0]
            print(data)
            data_list.append(data)
        save_to_csv(file_name='西红柿首富短评', list_dict=data_list)


def save_to_csv(file_name, list_dict):
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name + '.csv')
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)


if __name__ == '__main__':
    comment_spider('https://movie.douban.com/subject/27605698/')
