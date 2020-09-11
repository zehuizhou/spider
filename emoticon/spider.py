# -*- coding: utf-8 -*-
import os
import logging
import requests
from parsel import Selector

# 当前目录路径
DIR_PATH = os.path.dirname(os.path.abspath(__file__))
logging.getLogger().setLevel(logging.INFO)


def spider(keyword):
    """
    爬取发表情网站的表情，并将第一页的图片下载到本地
    :param keyword: 搜索关键词
    :return: 返回列表，[{},{},{},...]
    """
    if keyword is None:
        keyword = ''
    url = 'https://www.fabiaoqing.com/search/search/keyword/{}'
    ret = requests.get(url=url.format(keyword)).content.decode()
    root = Selector(ret)
    div_list = root.xpath("//div[@class='ui segment imghover']/div[@class='searchbqppdiv tagbqppdiv']")

    need_list = []

    # 删除文件img文件夹下所有图片
    files = os.listdir(DIR_PATH + '/static/img/')
    for f in files:
        os.remove(DIR_PATH + '/static/img/' + f)

    # 保存新的图片到img文件夹
    i = 1
    for div in div_list:
        img_url = div.xpath("./a/img/@data-original").get('')
        # 如果是gif就存为gif类型
        img_name = str(i)+'.gif' if 'gif' in img_url else str(i)+'.jpg'
        item = {
            '标题': div.xpath("./a/img/@title").get(''),
            '链接': img_url,
            '图片名': img_name
        }
        # print(item)
        download(img_name=img_name, img_url=item['链接'])
        i += 1
        need_list.append(item)
    return need_list


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
        path = DIR_PATH + '/static/img/' + img_name
        fp = open(path, 'wb')
        fp.write(pic.content)
        fp.close()
        logging.warning(f'图片下载成功~~'.center(70, '-'))
    except requests.exceptions.ConnectionError:
        logging.warning('图片下载失败！！'.center(70, '-'))