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
    top250_subject_url_list = []
    for page in range(25):
        top250_url = 'https://movie.douban.com/top250?start={}&filter='.format(page * 25)
        html_top250 = requests.get(url=top250_url, headers=common_header).content.decode()
        time.sleep(random.randint(0, 5))
        html_t = etree.HTML(html_top250)
        div_li_list = html_t.xpath("//ol[@class='grid_view']/li")
        for i in div_li_list:
            top250_subject_url = i.xpath("./div/div/a/@href")[0]
            top250_subject_url_list.append(top250_subject_url)
    print(f"电影详情地址个数：{len(top250_subject_url_list)},电影详情地址列表：{top250_subject_url_list}")
    return top250_subject_url_list


def comment_spider(movie_url):
    data_list = []
    comment_id = -1  # 自增长id，0~200
    for page in range(1):
        # 取前n页的评论，可以自己修改获取的页数
        comment_url = movie_url + 'comments?start={}&limit=20&sort=new_score&status=P'.format(page * 20)
        print(f'正在爬第{page + 1}页,{comment_url}的评论------------------------')
        comment_html = requests.get(url=comment_url, headers=common_header).content.decode()
        time.sleep(random.randint(0, 1))
        html_c = etree.HTML(comment_html)
        comment_item = html_c.xpath("//div[@id='comments']/div[@class='comment-item']/div[@class='comment']")

        for item in comment_item:
            comment_id = comment_id + 1

            datetime = item.xpath("./h3/span[@class='comment-info']/*[@class='comment-time ']/@title")[0]
            name = item.xpath("./h3/span[@class='comment-info']/a/text()")[0]
            comment = item.xpath("./p/span/text()")[0] if len(item.xpath("./p/span/text()")) > 0 else ''
            start_and_datetime = item.xpath("./h3/span[@class='comment-info']/span[2]/@title")[0]
            start = re.findall('[\u4e00-\u9fa5]+', start_and_datetime)[0] if len(
                re.findall('[\u4e00-\u9fa5]+', start_and_datetime)) > 0 else ''
            vote = item.xpath("./h3/span/span[@class='votes']/text()")[0]
            title = html_c.xpath("//div[@id='content']/h1/text()")[0]

            data = [comment_id, datetime, name, comment, start, vote, title]
            data_list.append(data)  # 用来后续存数据用
        print(f'评论总个数{len(data_list)},评论总列表：{data_list}')
    return data_list


def movie_spider(movie_url):
    """
    爬电影数据
    :return:
    """
    html = requests.get(url=movie_url, headers=common_header).content.decode()
    html_e = etree.HTML(html)  # 获取element 类型的html

    movie_name = html_e.xpath("//*[@id='content']/h1/span[1]/text()")[0]
    movie_country = re.findall('.*<span class="pl">制片国家/地区:</span>(.*)<br/>', html)[0]
    try:
        year = html_e.xpath("//span[@class='year']/text()")[0]
        movie_year = re.findall(r'\d+', year)[0]
    except:
        movie_year = ''

    movie_sign = html_e.xpath("string(//div[@class='tags-body'])")
    movie_indent = html_e.xpath("string(//*[@id='link-report']/span[1])")

    movie_rate = html_e.xpath("//*[@id='interest_sectl']/div[1]/div[2]/strong/text()")[0]
    movie_img = html_e.xpath("//*[@id='mainpic']/a/img/@src")[0]
    try:
        movie_runtime = html_e.xpath("//*[@id='info']/span[@property='v:runtime']/text()")[0]
    except:
        movie_runtime = ''
    try:
        movie_attr = html_e.xpath("string(//*[@id='info']/span[@class='actor']/span[@class='attrs'])")
    except:
        movie_attr = ''
    try:
        movie_type = html_e.xpath("//*[@id='info']/span[@property='v:genre']/text()")
    except:
        movie_type = ''

    total_list = [
        [movie_name, movie_rate, movie_country, movie_year, movie_sign, movie_indent, movie_img, movie_runtime,
         movie_attr, movie_type]
    ]
    print(total_list)
    return total_list


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
    url_list = top250_subject_url_spider()

    for url in url_list:
        data = movie_spider(url)
        time.sleep(random.randint(0, 1))
        save_data('top250movie', data)

    # for url in url_list:
    #     print(f'正在存储top250电影{url}的评论------------------------>')
    #     data = comment_spider(url)
    #     save_data('top250comment', data)

    # movie_spider('https://movie.douban.com/subject/1292052/')

if __name__ == '__main__':
    main()
