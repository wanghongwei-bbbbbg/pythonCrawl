# editor : XiaoHei
# time : 2022/9/11 14:58
import requests
import re
from lxml import etree
from pprint import pprint

bvid_url = 'https://www.bilibili.com/video/BV1T5411x7y3'
bvid = re.findall(r"video/(\S+)", bvid_url, re.S)[0]  # 提取bvid r 表示原生字符串（rawstring）
# 而使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配。

print(bvid)

oid_url = "https://api.bilibili.com/x/player/pagelist?bvid={}".format(bvid)
headers = {
    "User-Agent": 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML,like Gecko) Chrome/83.0.4103.61 Safari/537.36',
    "referer": "https://www.bilibili.com/video/BV1T5411x7y3"
}
response = requests.get(oid_url, headers=headers).content.decode()
oid = re.findall(r'"cid":(\d*),', response, re.S)[0]

print(oid)

danmu_url = "https://api.bilibili.com/x/v1/dm/list.so?oid={}".format(oid)
response = requests.get(danmu_url, headers=headers).content
html = etree.HTML(response)
d_list = html.xpath("//d/text()")
# 弹幕内容的xpath是 //d 表示多层标签中的d标签
# /text()获取的是标签直系文本
# //text()获取的是标签下所有文本
pprint(d_list)
