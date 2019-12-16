import requests
from lxml import html
import csv
import time
import random
import re

etree = html.etree
# 爬取的地址，如果比较多，可以写个函数，返回best_url_list
best_url_list = [
    'https://movie.douban.com/review/best/?start=20',
    'https://movie.douban.com/review/best/?start=20',
    'https://movie.douban.com/review/best/?start=40',
    'https://movie.douban.com/review/best/?start=60',
    'https://movie.douban.com/review/best/?start=80'
]

# 现在用全局变量存放需要用到url，也可以将url存在文件里，方便下次使用
people_url_list = []
comment_url_list = []
comment_detail_url_list = []


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
    # c.writerow(['user_name', 'user_url', 'user_id', 'movie_star', 'movie_name', 'movie_url', 'movie_id', 'user_lacation', 'user_sign', 'user_wish_label'])
    for i in data_list:
        c.writerow(i)


def parse_best(url):
    """
    获取主页数据，并修改people_url_list的值
    :param url:
    :return:
    """
    header = {
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1575853469%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIpN0ksKn_tQZJCMT1Hid-RafFbps-o0MBxW2HiLwgSG%26wd%3D%26eqid%3De612e673004758c6000000045ded9d9a%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.184410278.1573005299.1575622972.1575853471.6; __utmc=30149280; __utmz=30149280.1575853471.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; _pk_id.100001.8cb4=88b4639602988da6.1575853469.1.1575853484.1575853469.; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; __utmb=30149280.3.10.1575853471'
    }
    html = requests.get(url=url, headers=header).content.decode()
    html = etree.HTML(html)  # 获取element 类型的html

    div_temp_list = html.xpath("//*[@class='main review-item']")

    total_items = []  # 存放best页面数据的列表

    for i in div_temp_list:
        user_name = i.xpath(".//a[@class='name']/text()")[0]
        user_url = i.xpath(".//a[@class='name']/@href")[0]
        user_id = re.findall(r'\d+', user_url)[0] if len(re.findall(r'\d+', user_url)) > 0 else ''
        movie_star = i.xpath(".//span/@title") if len(i.xpath(".//span/@title")) > 0 else ''
        movie_name = i.xpath(".//img/@title")[0]
        movie_url = i.xpath(".//a[@class='subject-img']//@href")[0]
        movie_id = re.findall(r'\d+', movie_url)[0]

        item = [user_id, user_url, user_name, movie_id, movie_name, movie_star, movie_url]
        print(item)
        total_items.append(item)

        global people_url_list
        people_url_list.append(user_url)

    return total_items


def parse_people(people_url):
    """
    获取个人主页数据，并修改全局comment_url_list
    注意，这里要把header里的cookie参数加进去，需求登录
    :param people_url:
    :return:
    """
    user_url = people_url
    user_id = re.findall(r'\d+', user_url)[0] if len(re.findall(r'\d+', user_url)) > 0 else ''
    header_people = {
        'Host': 'www.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1575853469%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIpN0ksKn_tQZJCMT1Hid-RafFbps-o0MBxW2HiLwgSG%26wd%3D%26eqid%3De612e673004758c6000000045ded9d9a%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.184410278.1573005299.1575622972.1575853471.6; __utmc=30149280; __utmz=30149280.1575853471.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; _pk_id.100001.8cb4=88b4639602988da6.1575853469.1.1575853484.1575853469.; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; __utmb=30149280.3.10.1575853471'
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
    print(comment_url_list)

    # 获取看过电影页面，获取标签
    try:
        all_url = html_p.xpath("//*[@id='movie']/h2/span/a/@href")
        """[https://movie.douban.com/people/1019579/do,
        https://movie.douban.com/people/1019579/wish,
        https://movie.douban.com/people/1019579/collect]"""
        for i in all_url:
            if 'collect' in i:
                user_collect_url = i
        header = {
            'Host': 'movie.douban.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1575853469%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIpN0ksKn_tQZJCMT1Hid-RafFbps-o0MBxW2HiLwgSG%26wd%3D%26eqid%3De612e673004758c6000000045ded9d9a%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.184410278.1573005299.1575622972.1575853471.6; __utmc=30149280; __utmz=30149280.1575853471.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; _pk_id.100001.8cb4=88b4639602988da6.1575853469.1.1575853484.1575853469.; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; __utmb=30149280.3.10.1575853471'
        }
        html_sign = requests.get(url=user_collect_url, headers=header).content.decode()
        html_s = etree.HTML(html_sign)
        user_wish_label = html_s.xpath("//*[@id='content']/div[2]/div[2]/ul/li/a/@title")
    except:
        user_wish_label = ''

    total_people_item = []
    item = [user_id, user_url, user_lacation, user_sign, user_wish_label]
    print(item)
    total_people_item.append(item)
    return total_people_item


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
            'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1575853469%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIpN0ksKn_tQZJCMT1Hid-RafFbps-o0MBxW2HiLwgSG%26wd%3D%26eqid%3De612e673004758c6000000045ded9d9a%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.184410278.1573005299.1575622972.1575853471.6; __utmc=30149280; __utmz=30149280.1575853471.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; _pk_id.100001.8cb4=88b4639602988da6.1575853469.1.1575853484.1575853469.; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; __utmb=30149280.3.10.1575853471'
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
    header_comment = {
        'Host': 'movie.douban.com',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Cookie': 'bid="P6c5c7SdD3w"; ll="118172"; gr_user_id=fcd78f58-405d-4b35-a899-3b329e1bf917; _vwo_uuid_v2=D56EE26105876EE3AC3D4478816AA711B|4954256576cb3089bb2eed5430b1344a; viewed="30348491_2000732_30353486"; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1575853469%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DIpN0ksKn_tQZJCMT1Hid-RafFbps-o0MBxW2HiLwgSG%26wd%3D%26eqid%3De612e673004758c6000000045ded9d9a%22%5D; _pk_ses.100001.8cb4=*; __utma=30149280.184410278.1573005299.1575622972.1575853471.6; __utmc=30149280; __utmz=30149280.1575853471.6.5.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmt=1; dbcl2="166993767:SvDhHe+fb6A"; ck=ZUnE; _pk_id.100001.8cb4=88b4639602988da6.1575853469.1.1575853484.1575853469.; push_noty_num=0; push_doumail_num=0; __utmv=30149280.16699; __utmb=30149280.3.10.1575853471'
    }
    html_commment_detail = requests.get(url=cmmment_detail_url, headers=header_comment).content.decode()
    html_c_d = etree.HTML(html_commment_detail)
    cmmment_content = html_c_d.xpath("//*[@id='review-content']//text()")
    try:
        user_url = html_c_d.xpath("//div[@class='main']/a/@href")[0]
    except:
        user_url = None
    try:
        user_id = re.findall(r'\d+', user_url)[0] if len(re.findall(r'\d+', user_url)) > 0 else ''
    except:
        user_id = ''

    total_content_item = []
    item = [user_id, user_url, cmmment_detail_url, cmmment_content]
    print(item)
    total_content_item.append(item)
    return total_content_item


def main():
    # 第一步获取主页数据
    for url in best_url_list:
        print('--------第一步获取主页数据--------')
        data = parse_best(url)
        time.sleep(random.randint(2, 3))
        save_data('1', data)

    # 第二步获取个人主页数据
    for url in people_url_list:
        print('--------第二步获取个人主页数据--------')
        data = parse_people(url)
        time.sleep(random.randint(3, 5))
        save_data('3', data)

    # 第三步获取评论页地址
    for url in comment_url_list:
        print('--------第三步获取评论页地址--------')
        parse_comment_detail_url(url)
        time.sleep(random.randint(3, 6))

    # 第四步获取评论页详情
    for url in comment_detail_url_list:
        print('--------第四步获取评论页详情--------')
        data = parse_comment_detail_content(url)
        time.sleep(random.randint(6, 10))
        save_data('2', data)


if __name__ == '__main__':
    main()
    # parse_comment_detail_url('https://www.douban.com/people/163694915/reviews')
    # parse_comment_detail_content('https://movie.douban.com/review/12075884/')
