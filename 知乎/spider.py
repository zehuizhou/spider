import requests
import time
import pymssql


def spider(url):
    # 登录知乎，F12查看，复制cookie
    cookie = '_zap=6144130e-f578-46f5-bf61-7c95a4f54958; d_c0="ABCtkZGrNBCPTm4kf0OLw_a4kcO9_2BeINc=|1571192543"; _xsrf=NIfyN2b0r9QlrkUtwIyTJzP6Vfv6dwVj; __utma=51854390.1083738820.1575015824.1575015824.1575015824.1; __utmz=51854390.1575015824.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/; __utmv=51854390.100--|2=registration_date=20170227=1^3=entry_date=20170227=1; capsion_ticket="2|1:0|10:1577770557|14:capsion_ticket|44:MTkxYWQxMTY5NjFjNGQ5NGFjYTEyZTNhYjkyZDRkN2E=|a48acd0dd49731242fd18216e35e3f77e18e446dedc3f99d671af02d4d8f17fa"; z_c0="2|1:0|10:1577770590|4:z_c0|92:Mi4xUjc0OUJBQUFBQUFBRUsyUmthczBFQ2NBQUFDRUFsVk5YbXN5WGdCNWFxUlVTMVRkamtGNFhxRk1Pd1hreUE3RG13|5a1f6dc0267a4349e9ac6e6f8f7a996cf46ea1f6d50fc104491069d4112b9c52"; tst=r; q_c1=10532e0e41654b5ca1c45d3a6d186a52|1577770640000|1575015823000; Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1577772146,1577772162,1577772387,1577778762; Hm_lpvt_98beee57fd2ef70ccdd5ca52b9740c49=1577778873; KLBRSID=fb3eda1aa35a9ed9f88f346a7a3ebe83|1577778880|1577778760'

    # 通用的header，有些网址需求的Host可能不一样，所以有些网站要重新写header
    header = {'authority': 'www.zhihu.com',
              'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
              'Accept': '*/*',
              'Cookie': cookie}
    # 用来存放数据的列表
    data_list = []
    # 发起请求，获取返回的json数据
    result = requests.get(url=url, headers=header).json()
    # 解析json获取想要的数据
    totals = result['paging']['totals']  # 回答的总数
    print(f"总回答数{totals}")
    # 数据列表
    da_list = result['data']
    # 遍历数据列表，获取name、time_stamp......
    for i in da_list:
        # 知乎名称
        name = i['author']['name']
        # 编辑时间的时间戳
        time_stamp = i['updated_time']  # 页面上编辑于***
        # 时间戳转换成时间
        time_array = time.localtime(time_stamp)
        updated_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
        # 赞成数
        voteup_count = i['voteup_count']
        # 回答答案
        excerpt = i['excerpt']
        # 数据存在一个元祖里
        data = (name, updated_time, voteup_count, excerpt)
        # 把每个回答存到列表里，方便存到数据库
        data_list.append(data)
    # 把获取的数据返回
    return data_list


def creat_table():
    # 数据库要有一个叫test的数据库
    db = pymssql.connect('127.0.0.1', 'sa', '123456', 'test')  #服务器名,账户,密码,数据库名

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()

    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS zhihu")

    # 使用预处理语句创建表
    sql = """CREATE   TABLE   zhihu(
    id [int] IDENTITY (1,1) NOT NULL,
    name char(255),
    updated_time char(255),
    voteup_count char(255),
    excerpt char(5000)
    )  """

    cursor.execute(sql)  #执行sql
    db.commit()  # 提交

def save_data(data):
    db = pymssql.connect('127.0.0.1', 'sa', '123456', 'test')  #服务器名,账户,密码,数据库名

    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 保存数据到数据库的sql
    sql = "INSERT INTO zhihu(name, updated_time, voteup_count, excerpt) \
           VALUES (%s, %s, %s, %s)"
    cursor.executemany(sql, data)
    db.commit()  # 提交

if __name__ == '__main__':
    # 新建表
    creat_table()
    # offset参数从0开始，就是从第一个回答开始
    offset = 0
    # 遍历获取每个回答
    while offset < 512:
        url = 'https://www.zhihu.com/api/v4/questions/265642140/answers?include=data%5B*%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%2Cpaid_info_content%3Bdata%5B*%5D.mark_infos%5B*%5D.url%3Bdata%5B*%5D.author.follower_count%2Cbadge%5B*%5D.topics&offset={}&limit=5&sort_by=default&platform=desktop'
        # 爬数据
        data = spider(url=url.format(offset))
        # 存数据到数据
        save_data(data)
        # 打印数据
        print(data)
        # 每个请求5条数据，所以+5
        offset += 5
