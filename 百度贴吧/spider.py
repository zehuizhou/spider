import string
import time
import requests
from lxml import html
import csv
import random


etree = html.etree

# 全局的cookie，如果cookie过期了就修改下
cookie = 'BAIDUID=B0B1F3D534AD44A6513406C1BB445988:FG=1; BIDUPSID=B0B1F3D534AD44A6513406C1BB445988; PSTM=1568808511; BDUSS=ZReWN2VTJmY0xXR09YWlgxZEZmVDNwRzVJRVYxaHJuMUlPZlZsWDB3Uk93UjllSVFBQUFBJCQAAAAAAAAAAAEAAAD2E6iF0ruxrcb41srLrwAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAE40-F1ONPhdcT; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; MCITY=-179%3A; H_PS_PSSID=1467_21115_30211_30625_26350_22160; delPer=0; PSINO=5'

# 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
common_header = {'Host': 'gsp0.baidu.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
                 'Cookie': cookie}


def spider(page):
    param = {"id": "utf-8", "kw": "青海大学吧", "pn": page*50}
    ret = requests.get('https://tieba.baidu.com/f', params=param).content.decode()  # 大家看到没，get可以把params参数传入
    root = etree.HTML(ret)
    target_data = []
    li_list = root.xpath("//ul[@class='threadlist_bright j_threadlist_bright']/li")
    for li in li_list:
        if page == 0 and li == li_list[0]:
            title = li.xpath("//*[@id='thread_top_list']/li/div/div[2]/div/div[1]/a/text()")[0] \
                if li.xpath("//*[@id='thread_top_list']/li/div/div[2]/div/div[1]/a/text()") else ''
        else:
            if li == li_list[0]:
                title = li.xpath("//*[@id='thread_list']/li[1]/div/div[2]/div[1]/div[1]/a/text()")[0] \
                    if li.xpath("//*[@id='thread_list']/li[1]/div/div[2]/div[1]/div[1]/a/text()") else ''
            else:
                title = li.xpath("./div/div[2]/div[1]/div[1]/a/text()")[0] \
                    if li.xpath(".//div[@class='threadlist_title pull_left j_th_tit ']/a/text()") else ''
        rep_num = li.xpath(".//span[@class='threadlist_rep_num center_text']/text()")[0] \
            if li.xpath(".//span[@class='threadlist_rep_num center_text']/text()") else ''
        date = li.xpath(".//span[@class='threadlist_reply_date pull_right j_reply_data']/text()")[0] \
            if li.xpath(".//span[@class='threadlist_reply_date pull_right j_reply_data']/text()") else ''
        new_date = ''.join([i for i in date if not i in string.whitespace])
        print([title, rep_num, new_date])
        target_data.append([title, rep_num, new_date])
    return target_data


def save_data(file_name, data_list):
    """
    保存数据
    :param file_name: 文件名，不需要加后缀
    :param data_list: 写入的值,格式：[[],[],[],[],[]]
    """
    f_name = file_name + ".csv"
    with open(f_name, "a", newline="", encoding="utf-8") as f:
        c = csv.writer(f)
        for line in data_list:
            c.writerow(line)


if __name__ == '__main__':
    for i in range(564, 881):
        data = spider(page=i)
        save_data('tieba', data)
        print(f"{i}的数据保存成功")
        time.sleep(random.randint(0, 2))
