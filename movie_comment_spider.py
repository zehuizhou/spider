import requests
from lxml import html
import csv
import time
import random
import re

etree = html.etree

# 全局的cookie，如果cookie过期了就修改下
cookie = 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; __utmz=223695111.1575978668.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmc=30149280; __utmz=30149280.1576025284.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmc=223695111; _pk_ses.100001.4cf6=*; __utma=30149280.1397345246.1575978668.1576041699.1576044946.6; __utma=223695111.1128099318.1575978668.1576041699.1576044946.5; __utmb=223695111.0.10.1576044946; ap_v=0,6.0; __utmt=1; __utmb=30149280.2.10.1576044946; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; push_noty_num=0; push_doumail_num=0; _pk_id.100001.4cf6=ade6f0a5b5312eb8.1575978668.5.1576048051.1576041953.'

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
    top250_url = 'https://movie.douban.com/top250'
    top250_subject_url_list = []
    html_top250 = requests.get(url=top250_url, headers=common_header).content.decode()
    html_t = etree.HTML(html_top250)
    div_li_list = html_t.xpath("//ol[@class='grid_view']/li")
    for i in div_li_list:
        top250_subject_url = i.xpath("./div/div/a/@href")[0]
        top250_subject_url_list.append(top250_subject_url)
    top250_subject_url_list = top250_subject_url_list[0:10]  # 老师只要前十个，如果想要多，就在这设置
    print(f"电影详情地址个数：{len(top250_subject_url_list)},电影详情地址列表：{top250_subject_url_list}")
    return top250_subject_url_list


def cn_m2018_subject_url_spider():
    """
    2008年华语电影详情地址
    :return:
    """
    movie2018_url = 'https://movie.douban.com/ithil_j/activity/movie_annual2018/widget/1'
    cn_m2018_subject_url_list = []
    result = requests.get(url=movie2018_url, headers=common_header).json()
    for i in result['res']['subjects']:
        cn_m2018_subject_url_list.append(i['m_url'].replace('m.', 'movie.').replace('movie/', ''))
    print(cn_m2018_subject_url_list)
    return cn_m2018_subject_url_list


def comment_spider(m_url):
    data_list = []
    comment_id = -1  # 自增长id，0~200
    for page in range(10):
        # 取前10页的评论，可以自己修改获取的页数
        comment_url = m_url + 'comments?start={}&limit=20&sort=new_score&status=P'.format(page * 20)
        print(f'正在爬第{page + 1}页,{comment_url}的评论------------------------')
        comment_html = requests.get(url=comment_url, headers=common_header).content.decode()
        time.sleep(random.randint(0, 3))
        html_c = etree.HTML(comment_html)
        comment_item = html_c.xpath("//div[@id='comments']/div[@class='comment-item']/div[@class='comment']")

        for item in comment_item:
            comment_id = comment_id + 1
            # 这个comment-time后面有个空字符，把我坑了好久，T T
            datetime = item.xpath("./h3/span[@class='comment-info']/*[@class='comment-time ']/@title")[0]
            name = item.xpath("./h3/span[@class='comment-info']/a/text()")[0]
            comment = item.xpath("./p/span/text()")[0] if item.xpath("./p/span/text()") else ''
            start_and_datetime = item.xpath("./h3/span[@class='comment-info']/span[2]/@title")[0]
            start = re.findall('[\u4e00-\u9fa5]+', start_and_datetime)[0] if re.findall('[\u4e00-\u9fa5]+',
                                                                                        start_and_datetime) else ''
            vote = item.xpath("./h3/span/span[@class='votes']/text()")[0]
            title = html_c.xpath("//div[@id='content']/h1/text()")[0]

            data = [comment_id, datetime, name, comment, start, vote, title]
            data_list.append(data)  # 用来后续存数据用
        print(f'评论总个数{len(data_list)},评论总列表：{data_list}')
    return data_list


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
    top250_subject_url_list = top250_subject_url_spider()
    for i in top250_subject_url_list:
        print(f'正在存储top250电影{i}的评论------------------------>')
        data = comment_spider(i)
        save_data('top250', data)

    cn_m2018_subject_url_list = cn_m2018_subject_url_spider()
    for i in cn_m2018_subject_url_list:
        print(f'正在存储华语2018年前10电影{i}的评论------------------------>')
        data = comment_spider(i)
        save_data('cn2018', data)


if __name__ == '__main__':
    main()
