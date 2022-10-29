# editor : XiaoHei
# time : 2022/10/29 20:05

import numpy as np
import matplotlib.pyplot as plt

data = np.load('populations.npz', allow_pickle=True)  # 读入数据
print(data['data'])  # 输出数据文件中的data数组
name = data['feature_names']  # 提取其中的feature_names数组，视为数据的标签
values = data['data']  # 提取其中的data数组，视为数据的存在位置
plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
label1 = ['男性', '女性']  # 标签
label2 = ['城镇', '乡村']
ex = [0.01, 0.01]  # 饼图：设定各项距离圆心n个半径

# 1.直方图
p1 = plt.figure(figsize=(12, 12))  # 设置画布大小
# 子图1
a1 = p1.add_subplot(2, 2, 1)
plt.bar(range(2), values[19, 2:4], width=0.5, color='orange')
plt.ylabel('人口（万人）')
plt.ylim(0, 80000)  # 设置当前图形y轴的范围
plt.xticks(range(2), label1)  # 指定x轴刻度的数目与取值
plt.title('1996年男、女人口数直方图')

# 子图2
b1 = p1.add_subplot(2, 2, 2)
plt.bar(range(2), values[0, 2:4], width=0.5, color='red')
plt.ylabel('人口（万人）')
plt.ylim(0, 80000)
plt.xticks(range(2), label1)
plt.title('2015年男、女人口数直方图')

# 子图3
c1 = p1.add_subplot(2, 2, 3)
plt.bar(range(2), values[19, 4:6], width=0.5, color='orange')
plt.xlabel('类别')
plt.ylabel('人口（万人）')
plt.ylim(0, 90000)
plt.xticks(range(2), label2)
plt.title('1996年城、乡人口数直方图')

# 子图4
d1 = p1.add_subplot(2, 2, 4)
plt.bar(range(2), values[0, 4:6], width=0.5, color='red')
plt.xlabel('类别')
plt.ylabel('人口（万人）')
plt.ylim(0, 90000)
plt.xticks(range(2), label2)
plt.title('2015年城、乡人口数直方图')
plt.savefig('1996、2015年各类人口直方图.png')  # 保存图片

# 2.饼图
p2 = plt.figure(figsize=(8, 8))
# 子图1
a2 = p2.add_subplot(2, 2, 1)
plt.pie(values[19, 2:4], explode=ex, labels=label1, colors=['pink', 'crimson'], autopct='%1.1f%%')
plt.title('1996年男、女人口数饼图')

# 子图2
b2 = p2.add_subplot(2, 2, 2)
plt.pie(values[0, 2:4], explode=ex, labels=label1, colors=['PeachPuff', 'skyblue'], autopct='%1.1f%%')
plt.title('2015年男、女人口数饼图')

# 子图3
c2 = p2.add_subplot(2, 2, 3)
plt.pie(values[19, 4:6], explode=ex, labels=label2, colors=['pink', 'crimson'], autopct='%1.1f%%')
plt.title('1996年城、乡人口数饼图')

# 子图4
d2 = p2.add_subplot(2, 2, 4)
plt.pie(values[0, 4:6], explode=ex, labels=label2, colors=['PeachPuff', 'skyblue'], autopct='%1.1f%%')
plt.title('2015年城、乡人口数饼图')
plt.savefig('1996、2015年各类人口饼图.png')

# 3.箱线图
p3 = plt.figure(figsize=(10, 10))
plt.boxplot(values[0:20, 1:6], notch=True, labels=['年末', '男性', '女性', '城镇', '乡村'], meanline=True)
plt.xlabel('类别')
plt.ylabel('人口（万人）')
plt.title('1996~2015年各特征人口箱线图')
plt.savefig('1996`2015年各特征人口箱线图.png')

# 显示
plt.show()