# editor : XiaoHei
# time : 2022/10/20 21:29
import requests
import json


class QiushibaikeSpider():
    def __init__(self):
        self.url = 'https://www.qiushibaike.com/text/?page={}'
        self.headers = {
            'user-agent': 'Mozilla/5.0 (Linux; Android 5.0; SM-G900PBuild / LRX21T) AppleWebKit'
                          ' / 537.36(KHTML, likeGecko) Chrome / '
                          '81.0.4044.122 MobileSafari / 537.36',
        }

    def get_url_list(self):
        url_lists = list()
        for num in range(12):
            url_lists.append(self.url.format(num + 1))
        return url_lists

    def get_response_content_lists(self, url_lists):
        response_content_lists = list()
        for url in url_lists:
            ret = requests.get(url, headers=self.headers).content.decode()
            ret_dict = json.loads(ret)
            # json.dumps(): 将Python数据编码（转换）为JSON数据；
            # json.loads(): 将JSON数据转换（解码）为Python数据;
            # json.dump(): 将Python数据编码并写入JSON文件；
            # json.load(): 从JSON文件中读取数据并解码。

            # print(ret_dict[0]['data']['content'])
            content = list()
            for num in range(1, 25):
                ret_ = ret_dict[num]['data']['content']
                print(ret_)
                content.append(ret_)
            response_content_lists.append(content)
        return response_content_lists

    def save_file(self, ret):
        len_num = len(ret)
        content_list = list()
        for i in ret:
            for j in i:
                content = j
                with open('糗事百科的{}个段子.txt'.format(len_num * 24), 'a+', encoding="utf8") as f:
                    f.write("*" * 20 + "\n" + content + '\n' * 5)
        print("保存成功，请查看")

    def run(self):
        # 获取url列表
        url_lists = self.get_url_list()
        print(len(url_lists))
        # 获取content
        response_content_lists = self.get_response_content_lists(url_lists)
        # 存入文件
        self.save_file(response_content_lists)


if __name__ == '__main__':
    obj = QiushibaikeSpider()
    obj.run()
