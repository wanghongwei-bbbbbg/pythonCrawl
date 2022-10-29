# editor : XiaoHei
# time : 2022/10/21 10:37

# request_response.py
import requests
from settings import HEADERS


class RequestResponse():
    """传入一个请求url,返回一个原始字符串"""

    def __init__(self, url):
        self.url = url

    def __get_resquest(self, url):
        """
        获取响应,接受一个url参数，作为通用函数
        目前设置反反爬虫策略
        返回原始的未处理的原始字符串
        """
        response = requests.get(url, headers=HEADERS)
        print("请求响应代码：", response.status_code)
        response_ = response.content.decode()
        return response_

    def run(self):
        return self.__get_resquest(self.url)
