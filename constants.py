import os
import sys
import time
import pandas as pd
import requests

# 代理ip地址 http://www.xiongmaodaili.com?invitationCode=8E31F8BE-73FA-4078-B64A-CF32280F439E 按量提取 每次1个 json格式
proxy_url = ''


def change_proxy(retry_count):
    if retry_count < 0:
        return

    result = requests.get(proxy_url).json()
    if result['msg'] == 'ok':
        ip = result['obj'][0]['ip']
        port = result['obj'][0]['port']
        proxies = {"http": "http://" + ip + ":" + port, "https": "http://" + ip + ":" + port}

        with open('pro.txt', 'w') as f:
            f.write(str(proxies))

        print(f"代理ip为更改为：{proxies}")
        return proxies
    else:
        time.sleep(1)
        print('切换代理失败，重新尝试。。。')
        change_proxy(retry_count - 1)


def save_list_dict(file_name, list_dict):
    """
    存数据到csv
    :param file_name: 文件名，不用加后缀
    :param list_dict: [{}，{}，{}...]
    :return:
    """
    path = os.path.join(os.path.dirname(sys.argv[0]), file_name + '.csv')
    flag = False if os.path.isfile(path) else True
    df = pd.DataFrame(list_dict)
    df.to_csv(path, mode='a', encoding='utf_8_sig', index=False, header=flag)

