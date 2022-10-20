# editor : XiaoHei
# time : 2022/10/14 10:21

import numpy as np
import pandas as pd
import scipy.interpolate
from scipy.interpolate import interp1d


# 自定义列向量插值函数
# s为列向量，n为被插值的位置，k为取前后的数据个数，默认为1
def ployinterp_column(s, n, k=1):
    y = s[list(range(n - k, n)) + list(range(n + 1, n + 1 + k))]  # 取数
    y = y[y.notnull()]  # 剔除空值
    return scipy.interpolate.lagrange(y.index, list(y))(n)  # 插值并返回插值结果


detail = pd.read_csv('missing_data.csv', \
                     encoding='gbk')

print('detail每个特征缺失的数目为：\n', detail.isnull().sum())
print('detail每个特征非缺失的数目为：\n', detail.notnull().sum())

# 逐个元素判断是否需要插值
# for i in detail.columns:
#     for j in range(len(detail)):
#         if (detail[i].isnull())[j]:
#             detail[i][j] = ployinterp_column(detail[i], j)


detail.reindex(columns=['A', 'B', 'C'], fill_value=100)
print(detail)
