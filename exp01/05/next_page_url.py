# editor : XiaoHei
# time : 2022/10/21 10:27
# next_page_url.py
import re


class NextPageUrl():
    """传入的参数为response产生的原始字符串"""

    def __init__(self, html_str):
        """初始化参数"""
        self.html_str = html_str

    def __info_str(self, html_str):
        """将传入的html_str分解，提取有用的内容"""
        html_ = re.findall(
            r'<code class=\"pagelet_html\" id=\"pagelet_html_frs-list/pagelet/thread_list\" style=\"display:none;\">(.*?)</code>',
            html_str, re.S)[0]
        return html_

    def __parse_next_url(self, html_):

        # 提取当页下包含下一页的div
        div_content = re.findall(r'<div class=\"thread_list_bottom clearfix\">(.*?)-->', html_, re.S)[0]
        # if next_page == None:代表没有下一页
        # 由于无法直接定位，取所有的url，并放入列表
        next_url_list = re.findall(r'<a(.*?)>', div_content, re.S)
        for i in next_url_list:
            if "next pagination-item" in i: \
                    next_page_url = "https:" + re.findall(r'href="(.*?)"', i, re.S)[0]
        return next_page_url

    def run(self):
        """提供主要的对外接口"""
        __html_ = self.__info_str(self.html_str)
        __next_page_url = self.__parse_next_url(__html_)
        return __next_page_url
