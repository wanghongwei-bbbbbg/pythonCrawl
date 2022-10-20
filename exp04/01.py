# editor : XiaoHei
# time : 2022/10/14 10:20

import numpy as np
import matplotlib.pyplot as plt

data = np.load('populations.npz', allow_pickle=True)
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False


def getKeys(data):
    ks = []
    for key in data.keys():
        ks.append(key)
    return ks


keys = getKeys(data)

value = data[keys[0]][-3::-1, :]  # start:end:step,逗号用于区分维度.这里是获取所有列中倒数第三行到倒数第一行，逆序
name = data[keys[1]]
print(keys, value, name)
p1 = plt.figure(figsize=(14, 7))  # figsize – 宽度、高度（以英寸为单位）
# 子图1 散点图
ax1 = p1.add_subplot(1, 2, 1)
plt.title('1996~2015年人口数据特征间的关系散点图')
plt.xlabel('年份')
plt.ylabel('人口数（万人')
plt.xticks(range(0, 20), value[:, 0], )
plt.scatter(value[:, 0], value[:, 1], marker='o', c='r')
plt.scatter(value[:, 0], value[:, 2], marker='D', c='b')
plt.scatter(value[:, 0], value[:, 3], marker='h', c='g')
plt.scatter(value[:, 0], value[:, 4], marker='s', c='y')
plt.scatter(value[:, 0], value[:, 5], marker='*', c='c')
plt.legend(['年末总人口', '男性人口', '女性人口', '城镇人口', '乡村人口'])
plt.show()
