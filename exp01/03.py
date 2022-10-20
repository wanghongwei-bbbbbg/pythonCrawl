# editor : XiaoHei
# time : 2022/10/19 20:36

from urllib import request
from urllib import parse
from urllib import error
from http import cookiejar
import re
from pprint import pprint
import time
import random
import json


class JdPhoneInfo(object):
    def __init__(self, key_word):
        self.key_word = key_word

    def get_url(self, key_word, page_num, page_count):
        url_list = list()

        url_base = "https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&page=2&s=30"

        if page_num < page_count:
            info = {
                "keyword": key_word,
                "page": page_num + 1,
                "s": page_num * 30,
            }

        url_ = "s_new.php?" + parse.urlencode(info)
        url = parse.urljoin(base=url_base, url=url_)
        url_list.append(url)
        page_num += 1
        return url_list

    def parse_info(self, html_str):
        """获取整页的响应信息，包括page_count,page_current"""

        page_info = dict()
        # 获取页面总数
        page_count = re.compile(r'page_count:\"(.*?)\"', re.S).findall(html_str)
        page_info["page_count"] = int(page_count[0]) if page_count else None
        # 获取页面当页数
        page_current = re.compile(r'page:"(.*?)",page_count', re.S).findall(html_str)
        page_info["page_current"] = int(page_current[0]) if page_count else None
        # 获取所有的产品信息
        page_info["product_list"] = list()
        product_info_list = re.compile(r'class="p-img"(.*?)class="p-icons"',
                                       re.S).findall(html_str)
        ## 获取单个产品的信息
        for one_product_info in product_info_list:
            info = dict()
            # 获取标题及链接
            str_ = re.compile(r'p-name p-name-type-2(.*?)</div>', re.S).findall(one_product_info)[0]
            title = re.compile(r'em>(.*?)</em>', re.S).findall(str_)
            info["title"] = re.sub(r'\n|\t|\s|(<.*?>)', '', title[0]).strip() if title else None
            href = re.compile(r'href="(.*?)"', re.S).findall(str_)
            info["href"] = "https:" + href[0] if href else None

            # 获取价格
            str_ = re.compile(r'class="p-price"(.*?)</div>', re.S).findall(one_product_info)[0]
            price = re.compile(r'i>(.*?)</i>', re.S).findall(str_)
            info["price"] = price[0] if price else None
            # 获取图片
            info["pic_info"] = list()
            img_list = re.compile(r'class="ps-item">(.*?)</li>', re.S).findall(one_product_info)
            for img in img_list:
                pic_info_ = dict()
                pic_title = re.compile(r'title="(.*?)">', re.S).findall(img)
                pic_info_["pic_title"] = pic_title[0] if pic_title else None
                pic_href = re.compile(r'data-lazy-img="(.*?)"', re.S).findall(img)
                pic_info_["pic_href"] = "https:" + pic_href[0] if pic_href else "---"
                info["pic_info"].append(pic_info_)
            # 获取评价连接
            info["comment_href"] = info["href"] + "#comment"
            # 获取售卖店铺及链接
            info["store"] = dict()
            str_ = re.compile(r'class="p-shop"(.*?)</div>', re.S).findall(one_product_info)[0]
            shop_name = re.compile(r'title="(.*?)"', re.S).findall(str_)
            info["store"]["shop_name"] = shop_name[0] if shop_name else None
            shop_href = re.compile(r'href="(.*?)"', re.S).findall(str_)
            info["store"]["shop_href"] = "https:" + shop_href[0] if shop_href else None
            # 将单个产品添加到产品列表
            page_info["product_list"].append(info)
            print(title, '添加完成')
        return page_info

    def get_request(self, first_url, url=None, url_index_num=None, url_list=None):
        # 构造cookie_handler和https_handler处理器
        cookjar_ = cookiejar.CookieJar()
        cookie_handler = request.HTTPCookieProcessor(cookjar_)
        https_handler = request.HTTPSHandler()
        opener = request.build_opener(cookie_handler, https_handler)
        request.install_opener(opener)
        use_agent = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,likeGecko) Chrome / 83.0.4103.61Safari / 537.36"
        if url_list is not None:
            request_ = request.Request(url=url)
            request_.add_header("User-Agent", use_agent)
            if url_index_num == 0:
                request_.add_header(key="referer", val=first_url)
            else:
                request_.add_header(key="referer", val=url_list[url_index_num - 1])
        else:
            # Request实例
            request_ = request.Request(url=first_url)
            # 添加header
            request_.add_header("User-Agent", use_agent)
        response_ = request.urlopen(request_)
        return response_

    def save_content(self, info):
        with open("jindong_phone_info.json", 'a+', encoding='utf8') as f:
            f.write(json.dumps(info, ensure_ascii=False, indent=2))
            f.write(json.dumps(",", ensure_ascii=False, indent=2))
            print("当前写入url", info["page_current"])

    def run(self):
        first_url = "https://search.jd.com/Search?keyword={}".format(parse.quote(self.key_word))
        # 获取页面的总页数
        ## 请求第一页
        first_response_html = self.get_request(first_url=first_url).read().decode()
        ## 提取信息
        page_info = self.parse_info(first_response_html)  # page_info接收一个字典
        # 保存内容
        self.save_content(page_info)
        # 获取构造的所有url
        url_list = self.get_url(self.key_word, page_num=page_info["page_current"], page_count=page_info["page_count"])
        for url in url_list:
            response_html = self.get_request(first_url=first_url, \
                                             url=url, url_list=url_list,
                                             url_index_num=url_list.index(url)).read().decode()
            page_info = self.parse_info(response_html)
            # 保存内容
            self.save_content(page_info)
            num = random.uniform(1, 2)
            print('保存内容')
            time.sleep(num)


if __name__ == "__main__":
    # key_word = input("请输入关键字:")
    key_word = "手机"
    print("本程序将采集以下信息:标题及连接，价格，图片，评价连接，售卖店铺及链接")
    obj = JdPhoneInfo(key_word)
    obj.run()
