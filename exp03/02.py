# editor : XiaoHei
# time : 2022/10/15 11:11

import pandas as pd

eloss = pd.read_csv('ele_loss.csv', sep=',', encoding='gb18030')
ealarm = pd.read_csv('alarm.csv', sep=',', encoding='gb18030')
detail1 = pd.read_csv('ele_loss.csv', sep=',', encoding='gbk', index_col=0)
print('线损数据表的形状为：', detail1.shape)
detail2 = pd.read_csv('alarm.csv', sep=',', encoding='gbk', index_col=0)
print('用电量趋势与线路警告的形状：', detail2.shape)
## 数据类型转换，存储部分数据
eloss['ID'] = eloss['ID'].astype('str')
ealarm['date'] = ealarm['date'].astype('str')
data = pd.merge(eloss, ealarm, left_on='ID',
                right_on='date', how='inner')
print(data)
print('两张表合并之后的大小为：', data.shape)
