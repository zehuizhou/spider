import requests
import csv

index_url = 'https://api.eol.cn/gkcx/api/?access_token=&admissions=&central=&department=&dual_class=&f211=&f985=&is_dual_class=&keyword=&page={}&province_id=13&request_type=1&school_type=&signsafe=&size=20&sort=view_total&type=&uri=apigkcx/api/school/hotlists'

header = {
    'Accept': 'application/json, text/plain, */*',
    'Content-Type': 'application/json;charset=UTF-8',
    'Host': 'api.eol.cn',
    'Origin': 'https://gkcx.eol.cn',
    'Referer': 'https://gkcx.eol.cn/school/search?province=%E6%B2%B3%E5%8C%97',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
}

school_id_list = []
specialtyline_url_list = []


def school_spider(url):
    """
    获取学校数据
    :param url: 地址
    :return:
    """
    school_item_lsit = []

    for page_number in range(1, 8):
        result = requests.post(url=url.format(page_number), headers=header).json()
        item_list = result['data']['item']
        for i in item_list:
            school_id = i['school_id']
            name = i['name']
            province_name = i['province_name']
            level_name = i['level_name']
            rank = i['rank']
            type_name = i['type_name']
            rank_type = i['rank_type']

            global school_id_list
            global specialtyline_url_list
            # item是要存的字段
            item = [school_id, name, province_name, level_name, rank, type_name, rank_type]
            school_item_lsit.append(item)

            school_id_list.append(school_id)

            # 获取所需的专业分数线地址，注意地址中有两个{}，下面的“specialtyline_url_old.format(school_id, year)”代码进行了加工
            specialtyline_url_old = 'https://api.eol.cn/gkcx/api/?access_token=&local_province_id=13&page=1&school_id={}&signsafe=&size=1000&uri=apidata/api/gk/score/special&year={}'
            years = ['2014', '2015', '2016', '2017', '2018']  # 爬取的5种年份
            for year in years:
                specialtyline_url = specialtyline_url_old.format(school_id, year)
                specialtyline_url_list.append(specialtyline_url)

    print(f"学校数据列表：{school_item_lsit}")
    print(f"学校个数：{len(school_id_list)},学校id列表：{school_id_list}")
    print(f"：学校专业分数线specialtyline_url_list个数：{len(specialtyline_url_list)},学校专业分数线url列表：{specialtyline_url_list}")
    return school_item_lsit


def specialtyline_spider(specialtyline_url):
    """
    获取专业分数线数据
    :param specialtyline_url:
    :return:
    """
    result = requests.post(url=specialtyline_url, headers=header).json()
    item_list = result['data']['item']

    specialtyline_item_list = []
    for i in item_list:
        average = i['average']
        dual_class_name = i['dual_class_name']
        local_batch_name = i['local_batch_name']
        local_province_name = i['local_province_name']
        local_type_name = i['local_type_name']
        max = i['average']
        min = i['average']
        min_section = i['min_section']
        name = i['name']
        proscore = i['proscore']
        school_id = i['school_id']
        special_id = i['special_id']
        spname = i['spname']
        year = i['year']
        # item是要存的字段
        item = [average, dual_class_name, local_batch_name, local_province_name, local_type_name, max, min, min_section,
                name, proscore, school_id, special_id, spname, year]
        specialtyline_item_list.append(item)
    print(f"专业个数：{len(specialtyline_item_list)}")
    print(f"专业列表：{specialtyline_item_list}")
    return specialtyline_item_list


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
    # 第一步获取学校数据
    data = school_spider(index_url)
    save_data('school', data)

    # 第二步获取专业分数线数据
    for url in specialtyline_url_list:
        data = specialtyline_spider(url)
        # 把每次获取到的数据追加到csv
        save_data('specialtyline', data)

if __name__ == '__main__':
    main()
