# editor : XiaoHei
# time : 2022/10/21 10:36

# page_key_info.py
import re


class PageKeyInfo():
    """传入的参数为response产生的原始字符串"""

    def __init__(self, html_str):
        """初始化参数"""
        self.html_str = html_str

    def __info_str(self, html_str):
        """将传入的html_str分解，提取有用的内容"""
        html_ = re.findall(
            r'<code class=\"pagelet_html\"id=\"pagelet_html_frs-list/pagelet/thread_list\"style=\"display:none;\">(.*?)</code>',
            html_str, re.S)[0]
        return html_

    def __get_usefulinfo_by_one(self, ul_one):
        one_tiezi_info = dict()
        # 获取标题和地址
        title_and_href = re.findall(r'j_th_tit ">.*?<a rel="noreferrer"href = "(.*?)"title = "(.*?) target="_blank"',
                                    ul_one, re.S)
        title_and_href = title_and_href[0] if len(title_and_href) > 0 else None
        if title_and_href:
            title_href_ = "https://tieba.baidu.com" + title_and_href[0]
            title_ = title_and_href[1]
        else:
            title_href_ = None
            title_ = None
        # 获取作者和作者id
        author_name = re.findall(r'<span class="tb_icon_author ".*?title="主题作者: (.* ?)"', ul_one, re.S)
        author_name = author_name[0] if len(author_name) > 0 else None
        author_id = re.findall(r'title="主题作者.*?".*?data-field=\'{"user_id":(.*?)}\' >', ul_one, re.S)
        author_id = author_id[0] if len(author_id) > 0 else None
        author_home = re.findall(r'class="frs-author-name j_user_card "href = "(.*?)"target = "_blank" > ',
                                 ul_one, re.S)
        author_home = "https://tieba.baidu.com" + author_home[0] if len(author_home) > 0 else None
        # 取内容
        content = re.findall(r'<div class="threadlist_absthreadlist_abs_onlyline">(.*?)</div>', ul_one, re.S)
        content = content[0] if len(content) > 0 else None
        image = re.findall(r'bpic="(.*?)" class="threadlist_pic j_m_pic',
                           ul_one, re.S)
        # 将数据存放在字典中
        one_tiezi_info["title"] = title_
        one_tiezi_info["title_href"] = title_href_
        one_tiezi_info["author_name"] = author_name
        one_tiezi_info["author_id"] = author_id
        one_tiezi_info['author_home'] = author_home
        one_tiezi_info['content'] = content
        one_tiezi_info['image'] = image
        return one_tiezi_info


    def __ul_content(self, html_):
        # 获取当前主题页的所有列表
        ul_content_list = re.findall(r'li class=\" j_thread_list '
                                     r'clearfix\"(.*?)<li class=\" j_thread_list clearfix\"', html_, re.S)
        return ul_content_list


    def __get_content(self, html_):
        item_list = list()
        # 获取包含所有单块帖子的列表
        ul_content_list = self.__ul_content(html_)
        for ul_one in ul_content_list:
            item = self.__get_usefulinfo_by_one(ul_one)
            item_list.append(item)
        return item_list


    def run(self):
        # 处理字符串
        __html_ = self.__info_str(self.html_str)
        # 处理关键字段
        __item_list = self.__get_content(__html_)
        return __item_list
