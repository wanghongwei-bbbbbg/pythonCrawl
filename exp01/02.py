# editor : XiaoHei
# time : 2022/10/19 19:48

import urllib
import requests
from lxml import etree
import os


class TianTangTuPian(object):
    def __init__(self):
        pass

    def get_requests(self, url):
        headers = {
            "User-Agent": "Mozilla / 5.0(Windows NT 10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome/106.0.0.0 Safari/537.36 Edg/106.0.1370.47",
            "cookie":"t=49d0af84054bb4137cd10facc1a00afd; r=7382; Hm_lpvt_c13cf8e9faf62071ac13fd4eafaf1acf=1666269989; Hm_lvt_a0c29956538209f8d51a5eede55c74f9=1666180557,1666269990; Hm_lpvt_a0c29956538209f8d51a5eede55c74f9=1666269990"
        }
        response = requests.get(url=url, headers=headers)
        return response

    def parse_html_1(self, response):
        item_list = list()
        html_ = etree.HTML(response.content.decode())
        li_list = html_.xpath("//ul[contains(@class,'ali')]/li")
        print(li_list)

        for li in li_list:
            item = dict()  # 空字典
            title = li.xpath('./div/a/img/@alt')
            item['title'] = title[0] if title else None
            href = li.xpath('./div/a/img/@src')
            href = urllib.parse.urljoin(base=response.url, url=href[0] if href else None)
            item['href'] = href
            print(item['href'])
            item_list.append(item)
        return item_list

    def schedule(self, blocknum, blocksize, totalsize):
        per = 100.0 * blocknum * blocksize / totalsize
        if per > 100:
            per = 100
        print("当前下载进度：%d" % per)

    def save_image(self, item_list):
        print(item_list)
        if os.path.exists(path='./Image'):
            pass
        else:
            os.mkdir(path='./Image')
        for item in item_list:
            print("---")
            title = item['title']
            href = item['href']

            opener = urllib.request.build_opener()
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1941.0 Safari/537.36')]
            urllib.request.install_opener(opener)

            urllib.request.urlretrieve(url=href, filename='./Image/{}.jpg'.format(title), reporthook=self.schedule)
            print("写入{}成功".format(title))

    def run(self):
        first_url = "https://www.ivsky.com/tupian/ziranfengguang/"
        response_ = self.get_requests(url=first_url)
        item_list = self.parse_html_1(response_)
        self.save_image(item_list)


if __name__ == "__main__":
    obj = TianTangTuPian()
    obj.run()
