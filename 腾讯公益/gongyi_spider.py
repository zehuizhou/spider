import requests
from lxml import html
import csv
import datetime
import json

etree = html.etree

# 全局的cookie，如果cookie过期了就修改下
cookie = 'pgv_pvi=5671963648; pgv_pvid=6382757760; RK=PFrtiq0NER; ptcz=5208263401e5f54b61c96ac84e969534d84ed2f16cb174cbd23372bbdb8e22da; pac_uid=0_fc2abde7eca45; XWINDEXGREY=0; eas_sid=a1n5N7s1J930V6C6T3Q7z9y0v8'
# 通用的header
common_header = {'authority': 'scdn.gongyi.qq.com',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
                 'Accept': '*/*',
                 'Cookie': cookie,
                 'referer': 'https://gongyi.qq.com/succor/detail.htm?id=5528',
                 'path': '/json_data/data_detail/28/detail.5528.js',
                 'method': 'GET',
                 'scheme': 'https'
                 }


def content_spider(url):
    index = requests.get(url=url, headers=common_header).content.decode()
    index = index.replace('_CallbackSearch(', '')[:-1]
    index = json.loads(index, encoding="utf-8")
    plist = index['plist']

    data_list = []

    for p in plist:
        id = p['id']
        # 获取详情页数据
        detail_url = 'https://scdn.gongyi.qq.com/json_data/data_detail/{}/detail.{}.js'
        detail = requests.get(url=detail_url.format(int(id[-2:]), id), headers=common_header).content.decode()
        detail = detail.replace(f'_cb_fn_proj_{id}(', '')[:-2]
        detail = json.loads(detail)

        title = detail['base']['title']  # 标题
        summary = detail['base']['summary']  # 项目简介
        needMoney = float(detail['base']['needMoney'])/100  # 筹款目标
        startTime = detail['base']['startTime']  # 筹款开始时间
        endTime = detail['base']['endTime']  # 筹款结束时间
        # eOrgName = detail['base']['eOrgName']  # 执行方(和下面重复了，不存)

        obtainMoney = detail['base']['donate']['obtainMoney']  # 捐款金额（不存）
        donateNum = detail['base']['donate']['donateNum']  # 捐款人数
        quota_money = detail['base']['donate']['quota_money']  # 企业捐配
        try:
            recvedMoney = float(obtainMoney) - float(quota_money)  # 已筹金额
        except:
            recvedMoney = ''
        try:
            percent = str((float(recvedMoney)/float(needMoney))*100) + '%'  # 捐款进度
        except:
            percent = ''

        eOrgName = detail['base']['eOrgName']  # 执行方
        pName = detail['base']['pName']  # 发起方
        fundName = detail['base']['fundName']  # 公募支持

        desc = detail['detail']['desc']  # 捐助说明（不存）
        html = etree.HTML(desc)
        desc_text = html.xpath("string(//*)")  # 捐助说明，纯文本
        word_number = len(desc_text)  # 字数
        img_number = len(html.xpath("//img"))  # 图片张数

        is_execution_plan = '是' if '执行计划' in desc else '否'
        is_project_budget = '是' if '项目预算' in desc else '否'
        is_whoweare = '是' if '我们是谁' in desc else '否'
        is_executive_ability = '是' if '执行能力说明' in desc else '否'
        is_donation_feedback = '是' if '捐赠回馈' in desc else '否'
        is_bill = '是' if '票据' in desc else '否'

        try:
            process = detail['detail']['process']
            date_list = []
            for p in process:
                date = p['create_time']
                date_array = datetime.datetime.fromtimestamp(date)
                date = date_array.strftime("%Y-%m-%d %H:%M:%S")
                date_list.append(date)
            date_list = '，'.join(date_list)  # 项目进度时间
        except:
            date_list = ''

        data = [id, title, summary, needMoney, startTime, endTime,
                donateNum, percent, quota_money, recvedMoney,
                eOrgName, pName, fundName,
                desc_text, word_number, img_number, date_list,
                is_execution_plan, is_project_budget, is_whoweare, is_executive_ability, is_donation_feedback, is_bill
                ]
        print(data)
        data_list.append(data)

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


if __name__ == '__main__':
    for i in range(1, 60):
        print(f'正在获取第{i}页数据')
        start_url = 'https://ssl.gongyi.qq.com/cgi-bin/WXSearchCGI?ptype=stat&s_status=3&jsoncallback=_CallbackSearch&s_status=3&s_tid=&s_puin=&s_fid=&s_key=图书馆&p={}'.format(i)
        data = content_spider(start_url)
        save_data('data', data)
