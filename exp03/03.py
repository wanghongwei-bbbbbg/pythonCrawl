# editor : XiaoHei
# time : 2022/10/16 10:17

import pandas as pd
import numpy as np
detail = pd.read_csv('model.csv',encoding='gbk')

## 自定义离差标准化函数
def MinMaxScale(data):
    data = (data-data.min())/(data.max()-data.min())
    return data

## 对建模专家做离差标准化
data1 = MinMaxScale(detail['电量趋势下降指标'])
data2 = MinMaxScale(detail['线损指标'])
data3 = MinMaxScale(detail['告警类指标'])
data4 = pd.concat([data1,data2,data3])
print('离差标准化之前数据为：\n',detail[['电量趋势下降指标',
                    '线损指标','告警类指标']].head(5))
print('离差标准化之后数据为：\n',data4.head(5))

## 自定义小数定标准化函数
def DecimalScaler(data):
    data = data/10**np.ceil(np.log10(data.abs().max()))
    return data
## 小数定标准化
data9 = DecimalScaler(detail['电量趋势下降指标'])
data10 = DecimalScaler(detail['线损指标'])
data11 = DecimalScaler(detail['告警类指标'])
data12 = pd.concat([data9,data10,data11],axis=1)
print('离差标准化之前数据为：\n',detail[['电量趋势下降指标',
                    '线损指标','告警类指标']].head(5))
print('离差标准化之后数据为：\n',data12.head(5))
