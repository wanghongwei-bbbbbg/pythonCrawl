import requests
from queue import Queue
import json
from threading import Thread
from multiprocessing.dummy import Pool


class Txsz():
    def __init__(self):
        # 总共的数据条数
        self.count = 5573
        # 创建初始url
        self.start_url = "https://careers.tencent.com/tencentcareer/api/post/Query?&countryId=1&pageIndex={}&pageSize=10&language=zh-cn&area=cn"
        # 创建start_referer和second_referer
        self.start_referer = "https://careers.tencent.com/search.html?query=co_1&sc=1"
        self.second_referer = "https://careers.tencent.com/search.html?query=co_1&index={}&sc=1"
        """
        创建队列
        self.url_queue存放url
        self.json_queue存放所有的json
        self.content_queue存放解析的内容
        """
        self.url_referer_queue = Queue()
        self.json_queue = Queue()
        self.content_queue = Queue()

    def get_url(self):
        """
        构建爬去的url
        参数pageIndex，pageSize 变化，由count=5727设计
        url_list返回待待爬取列表
        """
        pageSize = 10
        for pageIndex in range(1, self.count // pageSize + 2):
            item = dict()
            url = self.start_url.format(pageIndex)

            if pageIndex == 1:
                referer = self.start_referer
            else:
                referer = self.second_referer.format(pageIndex)

            item["url"] = url
            item["referer"] = referer

            self.url_referer_queue.put(item)

    def get_json(self):
        """
        获取返回的json数据，原则上每条url对应一个json数据
        """
        while self.url_referer_queue.not_empty:
            """判断非空，则执行操作，否则跳出"""
            # 获取url,referer
            item = self.url_referer_queue.get()
            url = item["url"]
            referer = item["referer"]

            # 构造请求头
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36",
                "cookie": "_ga=GA1.2.275188285.1582376294; pgv_pvi=4879193088; _gcl_au=1.1.1802818219.1582376295; loading=agree",
                "referer": referer,
            }
            print("spider_url:", url)
            # 获取响应的json
            response = requests.get(url, headers=headers).content.decode()
            # 将str转化为dict
            response = json.loads(response)
            # 添加获取到的json到json_queue
            self.json_queue.put(response)
            # 队列计数减一
            self.url_referer_queue.task_done()

    def get_content(self):
        """
        分析json_queue中的单项json,并提取数据
        职位名称：RecruitPostName
        职位ID:PostId
        每个职位详情页地址：PostURL
        职位类别：CategoryName
        工作地点：LocationName
        发布时间：LastUpdateTime
        工作职责：Responsibility
        """
        while self.json_queue.not_empty:
            # 获取json
            json_ = self.json_queue.get()
            Posts = json_["Data"]["Posts"]
            for item in Posts:
                item_dict = {
                    "RecruitPostName": item["RecruitPostName"],
                    "PostId": item["PostId"],
                    "PostURL": item["PostURL"],
                    "CategoryName": item["CategoryName"],
                    "LocationName": item["LocationName"],
                    "LastUpdateTime": item["LastUpdateTime"],
                    "Responsibility": item["Responsibility"],
                }
                self.content_queue.put(item_dict)
            self.json_queue.task_done()

    def save_content(self):
        while self.content_queue.not_empty:
            item = self.content_queue.get()
            with open("tencent_social_positoon.json", "a", encoding="utf-8") as f:
                f.write(json.dumps(item, ensure_ascii=False, indent=2))
                f.write(",")
            self.content_queue.task_done()

    def run(self):
        """
        实现主要逻辑
        """
        # 创建线程列表
        thread_list = list()
        # 创建get_url方法的线程
        url_thread = Thread(target=self.get_url)
        thread_list.append(url_thread)
        # 创建get_json方法的线程
        json_thread = Thread(target=self.get_json)
        thread_list.append(json_thread)
        # 创建get_content方法的线程
        content_thread = Thread(target=self.get_content)
        thread_list.append(content_thread)
        # 创建save_content方法的线程
        save_content_thread = Thread(target=self.save_content)
        thread_list.append(save_content_thread)

        # # 创建线程池
        # pool = Pool(10)

        # def process_thread(thread_):
        #     thread_.setDaemon(True)
        #     thread_.start()

        # pool.map(process_thread,thread_list)
        for t in thread_list:
            t.daemon
            t.start()

        # 让各队列全空才退出主线程
        self.url_referer_queue.join()
        self.json_queue.join()
        self.content_queue.join()


if __name__ == "__main__":
    obj = Txsz()
    obj.run()

