# editor : XiaoHei
# time : 2022/10/14 10:20

import numpy as np
import matplotlib.pyplot as plt

# 实训1 分析1996~2015年人口数据特征间的关系
# 使用numpy库读取人口数据
data = np.load('populations.npz', allow_pickle=True)
print(data.files)  # 查看文件中的数组
print(data['data'])
print(data['feature_names'])

plt.rcParams['font.sans-serif'] = 'SimHei'  # 设置中文显示
name = data['feature_names']  # 提取其中的feature_names数组，视为数据的标签
values = data['data']  # 提取其中的data数组，视为数据的存在位置

p1 = plt.figure(figsize=(12, 12))  # 确定画布大小
pip1 = p1.add_subplot(2, 1, 1)  # 创建一个两行一列的子图并开始绘制
# 在子图上绘制散点图
plt.scatter(values[0:20, 0], values[0:20, 1], marker='8', color='red')
plt.ylabel('总人口（万人）')
plt.legend('年末')
plt.title('1996~2015年末与各类人口散点图')

pip2 = p1.add_subplot(2, 1, 2)  # 绘制子图2
plt.scatter(values[0:20, 0], values[0:20, 2], marker='o', color='yellow')
plt.scatter(values[0:20, 0], values[0:20, 3], marker='D', color='green')
plt.scatter(values[0:20, 0], values[0:20, 4], marker='p', color='blue')
plt.scatter(values[0:20, 0], values[0:20, 5], marker='s', color='purple')
plt.xlabel('时间')
plt.ylabel('总人口（万人）')
plt.xticks(values[0:20, 0])
plt.legend(['男性', '女性', '城镇', '乡村'])

# 在子图上绘制折线图
p2 = plt.figure(figsize=(12, 12))
p1 = p2.add_subplot(2, 1, 1)
plt.plot(values[0:20, 0], values[0:20, 1], color='r', linestyle='--', marker='8')
plt.ylabel('总人口（万人）')
plt.xticks(range(0, 20, 1), values[range(0, 20, 1), 0], rotation=45)  # rotation设置倾斜度
plt.legend('年末')
plt.title('1996~2015年末总与各类人口折线图')

p2 = p2.add_subplot(2, 1, 2)
plt.plot(values[0:20, 0], values[0:20, 2], 'y-')
plt.plot(values[0:20, 0], values[0:20, 3], 'g-.')
plt.plot(values[0:20, 0], values[0:20, 4], 'b-')
plt.plot(values[0:20, 0], values[0:20, 5], 'p-')
plt.xlabel('时间')
plt.ylabel('总人口（万人）')
plt.xticks(values[0:20, 0])
plt.legend(['男性', '女性', '城镇', '乡村'])

# 显示图片
plt.show()
