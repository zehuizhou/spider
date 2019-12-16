import requests
from lxml import html
import csv
import time
import random
import re

etree = html.etree
# 全局的cookie，如果cookie过期了就修改下
cookie = 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1575853469%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIpN0ksKn_tQZJCMT1Hid-RafFbps-o0MBxW2HiLwgSG%26wd%3D%26eqid%3De612e673004758c6000000045ded9d9a%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.184410278.1573005299.1575622972.1575853471.6; __utmc=30149280; __utmz=30149280.1575853471.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; _pk_id.100001.8cb4=88b4639602988da6.1575853469.1.1575853484.1575853469.; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; __utmb=30149280.3.10.1575853471'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'movie.douban.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                 'Cookie': cookie}


people_url_list = []  # 用户的地址列表，很重要，接下来爬用户的详情、评论、评分会用到
comment_url_list = []  # 评论地址列表
comment_detail_url_list = []  # 评论详情地址列表
collect_movie_url_list = []  # 看过的电影地址列表，爬取评分用到


def get_start_url_list(page_number):
    """
    获取url
    :param page_number: 想获取的页数
    :return:
    """
    index_url = "https://movie.douban.com/subject/27668250/comments?start={}&limit=20&sort=new_score&status=P"
    url_index_list = []
    for i in range(page_number):  # 通过循环拼接50个url，也就是1000个用户的url
        url_index_list.append(index_url.format(i * 20))
    print(f"start地址个数：{len(url_index_list)},start地址列表：{url_index_list}")
    return url_index_list


def parse_people_url(start_url):
    """
    抓用户详情地址
    :param start_url: 被抓的地址
    :return: 返回用户的详情地址
    """
    html_index = requests.get(url=start_url, headers=common_header).content.decode()
    html_i = etree.HTML(html_index)
    div_temp_list = html_i.xpath("//div[@id='comments']//div[@class='comment-item']")
    global people_url_list
    for i in div_temp_list:
        people_url = i.xpath(".//div[@class='comment']/h3/span[@class='comment-info']/a/@href")[0]
        people_url_list.append(people_url)
    print(f"用户地址个数：{len(people_url_list)},用户地址列表：{people_url_list}")
    return people_url_list


def parse_people(people_url):
    """
    获取个人主页数据，这个方法比较关键
    注意，这里要把header里的cookie参数加进去，需求登录
    :param people_url:
    :return:
    """
    user_url = people_url
    user_id = re.findall(".*people/(.*)/", user_url)[0] if len(re.findall(".*people/(.*)/", user_url)) > 0 else ''
    header_people = {
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': cookie
    }
    html_people = requests.get(url=people_url, headers=header_people).content.decode()
    html_p = etree.HTML(html_people)
    try:
        user_lacation = html_p.xpath("//*[@id='profile']/div/div[2]/div[1]/div/a/text()")[0]
    except:
        user_lacation = ''
    user_sign = html_p.xpath("//*[@id='intro_display']/text()") if len(
        html_p.xpath("//*[@id='intro_display']/text()")) > 0 else ''

    # 获取评论页地址
    comment_url = html_p.xpath("//*[@id='review']/h2/span/a/@href")
    global comment_url_list
    comment_url_list += comment_url
    print(f"评论地址个数：{len(comment_url_list)},评论地址列表：{comment_url_list}")

    # 获取看过电影页面，获取标签
    try:
        # all_url有可能有3种url
        # https://movie.douban.com/people/1019579/do
        # https://movie.douban.com/people/1019579/wish
        # https://movie.douban.com/people/1019579/collect
        all_url = html_p.xpath("//*[@id='movie']/h2/span/a/@href")

        user_collect_url = None
        for i in all_url:
            if 'collect' in i:
                user_collect_url = i

        # 顺便把看过的电影url存起来，用来获取1.csv的数据，也就是看过电影的评分
        global collect_movie_url_list
        collect_movie_url_list.append(user_collect_url)  # 第一页
        collect_movie_url_list.append(user_collect_url+'?start=15&sort=time&rating=all&filter=all&mode=grid')  # 第二页

        # 获取看过电影页面，获取标签
        html_sign = requests.get(url=user_collect_url, headers=common_header).content.decode()
        html_s = etree.HTML(html_sign)
        user_wish_label = html_s.xpath("//*[@id='content']/div[2]/div[2]/ul/li/a/@title")
    except:
        user_wish_label = ''

    total_people_item = []
    item = [user_id, user_url, user_lacation, user_sign, user_wish_label]
    print(item)
    total_people_item.append(item)
    return total_people_item


def parse_collect_movie(collect_url):
    """
    获取表格1
    :param user_collect_url: 看过电影地址
    :return:
    """
    html_collect = requests.get(url=collect_url, headers=common_header).content.decode()
    html_c = etree.HTML(html_collect)

    user_name = html_c.xpath("//*[@id='content']/div[2]/div[2]/div[1]/div[1]/h3/text()")[0]
    user_url = html_c.xpath("//*[@id='content']/div[2]/div[2]/div[1]/a/@href")[0]
    user_id = re.findall(".*people/(.*)/", user_url)[0]
    total_collect_item = []

    div_list = html_c.xpath("//div[@class='article']/div[@class='grid-view']/div")
    for i in div_list:
        movie_url = i.xpath("./div/a/@href")[0]
        movie_id = re.findall(r'\d+', movie_url)[0]
        movie_name = i.xpath("./div/a/@title")[0]
        movie_rate = i.xpath("./div/ul/li[3]/span[1]/@class")[0]

        item = [user_name, user_id, user_url, movie_name, movie_rate, movie_id, movie_url]
        total_collect_item.append(item)
    print(f"看过电影数量：{len(total_collect_item)},看过电影列表：{total_collect_item}")
    return total_collect_item


def parse_comment_detail_url(comment_url):
    """
    获取评论详情页地址
    :param comment_url: 评论页的url
    :return:
    """
    comment_url_list = [comment_url, comment_url + '?start=10']  # 获取2页的评论
    for url in comment_url_list:
        header_comment = {
            'Host': 'www.douban.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': cookie
        }
        html_commment = requests.get(url=url, headers=header_comment).content.decode()
        html_c = etree.HTML(html_commment)
        try:
            comment_detail_url = html_c.xpath("//*[@class='review-list chart ']/div/div/div/h2/a/@href")
        except:
            comment_detail_url = None
        global comment_detail_url_list
        comment_detail_url_list += comment_detail_url
    print(comment_detail_url_list)
    return comment_detail_url_list


def parse_comment_detail_content(cmmment_detail_url):
    """
    获取评论详情页数据
    :param cmmment_detail_url: 详情页url
    :return:
    """
    html_commment_detail = requests.get(url=cmmment_detail_url, headers=common_header).content.decode()
    html_c_d = etree.HTML(html_commment_detail)
    cmmment_content = html_c_d.xpath("//*[@id='review-content']//text()")
    try:
        user_url = html_c_d.xpath("//div[@class='main']/a/@href")[0]
    except:
        user_url = None
    try:
        user_id = re.findall(".*people/(.*)/", user_url)[0] if len(re.findall(".*people/(.*)/", user_url)) > 0 else ''
    except:
        user_id = ''

    total_content_item = []
    item = [user_id, user_url, cmmment_detail_url, cmmment_content]
    print(item)
    total_content_item.append(item)
    return total_content_item


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
    # 第一步获主页的url，获取people的url
    print('--------第一步获starturl--------')
    for url in get_start_url_list(1):
        print('--------第二步获people的url--------')
        parse_people_url(url)

    # 第二步获取个人主页数据，并保存后续要用到的url
    for url in people_url_list:
        print('--------第二步获取个人主页数据--------')
        data = parse_people(url)
        time.sleep(random.randint(3, 5))
        save_data('3', data)
    print(f"看过电影地址个数：{len(collect_movie_url_list)},看过电影地址列表：{collect_movie_url_list}")

    # 第三步获取看过电影数据并保存
    for collect_url in collect_movie_url_list:
        data = parse_collect_movie(collect_url)
        save_data('1', data)
        time.sleep(random.randint(3, 8))

    # 第四步获取评论页地址
    for url in comment_url_list:
        print('--------第三步获取评论页地址--------')
        parse_comment_detail_url(url)
        time.sleep(random.randint(13, 16))

    # 第五步获取评论页详情
    for url in comment_detail_url_list:
        print('--------第四步获取评论页详情--------')
        data = parse_comment_detail_content(url)
        time.sleep(random.randint(8, 16))
        save_data('2', data)


if __name__ == '__main__':
    # get_index_url_list(25)
    # get_people_url('https://movie.douban.com/subject/27668250/comments?start=480&limit=20&sort=new_score&status=P')
    main()
