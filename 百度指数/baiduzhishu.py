import requests
import execjs

from constants import headers, js, data_url, uniqid_url

keys = ["all", "pc", "wise"]


class BaiDuIndex(object):

    def __init__(self):
        self.js_handler = self.get_js_handler()
        self.session = self.get_session()

    def decrypt(self, key, data):
        # 若因环境问题无法运行，替换此方法即可
        return self.js_handler.call('decrypt', key, data)

    def do_request(self, url):
        return self.session.get(url)

    def parse(self, response, uniqid):
        result = []
        data_dict = response.get("data").get("userIndexes")[0]
        for key in keys:
            result.append({key: self.decrypt(uniqid, data_dict.get(key).get("data"))})
        return result

    def get_baidu_index(self, keyword):
        response = self.do_request(data_url.format(keyword)).json()
        uniqid = self.do_request(uniqid_url.format(response.get("data").get("uniqid"))).json().get("data")
        return self.parse(response, uniqid)

    @staticmethod
    def get_js_handler():
        return execjs.compile(js)

    @staticmethod
    def get_session():
        session = requests.session()
        session.headers = headers
        session.verify = False
        return session


if __name__ == '__main__':
    baidu = BaiDuIndex()
    print(baidu.get_baidu_index("王者荣耀"))
