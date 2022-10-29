# editor : XiaoHei
# time : 2022/10/21 10:32

import requests
from urllib import parse
import re
import json
from queue import Queue
from threading import Thread
import time
from settings import HEADERS
from next_page_url import NextPageUrl
from page_key_info import PageKeyInfo
from request_response import RequestResponse


class MainProcess():
    """
    接受参数：start_url,tieba_name
    """

    def __init__(self, tieba_name, url):
        self.tieba_name = tieba_name
        self.url = url.format(parse.quote(tieba_name))
        self.url_queue = Queue()
        self.rawhtml_queue = Queue()
        self.content_queue = Queue()

    def __make_url_and_rawhtml(self, url):
        """生产url和rawhtml"""
        # self.url_queue.put(url)
        html_str = RequestResponse(url).run()
        next_page_url = NextPageUrl(html_str).run()
        print(next_page_url)
        # 将html字符串放入队列
        self.rawhtml_queue.put(html_str)
        while next_page_url:
            self.url_queue.put(next_page_url)
            return self.__make_url_and_rawhtml(next_page_url)

    def __make_key_info(self):
        """消费url和rawhtml，生产content"""
        while self.url_queue.not_empty and self.rawhtml_queue.not_empty:
            # 从队列中取出一一对应的url和rawhtml
            url = self.url_queue.get()
            html_str = self.rawhtml_queue.get()
            item_list = PageKeyInfo(html_str).run()
            # 将当前页url放入相关数据中返回
            item = dict(current_page_url=url)
            item_list.append(item)
            # 将相关数据放入队列
            self.content_queue.put(item_list)
            # 显示状态
            print("开始从当前{}提取信息".format(url))
            # 队列计数减1
            self.url_queue.task_done()
            self.rawhtml_queue.task_done()

    def __save_json_file(self):
        """保存相关数据为json文件,消费content"""
        while self.content_queue.not_empty:
            # 从队列取数
            content = self.content_queue.get()
            # 构造filename
            url = content[-1]["current_page_url"]
            filename = parse.unquote(
                re.split(pattern=r'\?', string=url)[-1]) + ".json"
            with open("./jsonfiletotal/" + filename, 'w', encoding='utf8') as f:
                f.write(json.dumps(content, ensure_ascii=False, indent=4))
                print("保存" + filename + "文件成功")
            # 队列计数减1
            self.content_queue.task_done()

    def run(self):
        # 将首个url放入self.url_queue队列
        self.url_queue.put(self.url)
        # 创建线程列表
        thread_list = list()
        make_url_and_rawhtml_thread = Thread(target=self.__make_url_and_rawhtml, args=(self.url,))
        thread_list.append(make_url_and_rawhtml_thread)
        make_key_info_thread = Thread(target=self.__make_key_info)
        thread_list.append(make_key_info_thread)
        save_json_file_thread = Thread(target=self.__save_json_file)
        thread_list.append(save_json_file_thread)
        for t in thread_list:
            t.setDaemon = True
            t.start()
        # 让所有队列里内容清空
        self.url_queue.join()
        self.rawhtml_queue.join()
        self.content_queue.join()


# 测试用例
if __name__ == "__main__":
    tieba_name = "李毅"
    first_url = "https://tieba.baidu.com/f?kw={}&ie=urf-8&pn=0"
    obj = MainProcess(tieba_name, first_url)
    obj.run()
