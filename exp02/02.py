# editor : XiaoHei
# time : 2022/10/13 10:02
import datetime

import numpy
import numpy as np
from numpy import ptp


def date2str(nowDate):
    nowDate = str(nowDate, 'GBK')
    return datetime.datetime.strptime( \
        nowDate, "%Y/%m/%d").date().weekday() + 1


(days, closing_price, high_price, low_price, volume) = numpy.loadtxt('stock.csv', unpack=True,
                                                                     delimiter=',', usecols=(1, 2, 3, 4, 11),
                                                                     converters={1: date2str})
print("closing_price的类型是：", type(closing_price))
print("closing_price的维数是：", closing_price.shape)
print("closing_price元素个数是：", closing_price.size)
print("closing_price's avg 是：", numpy.mean(closing_price))
print("closing_price's median 是：", numpy.median(closing_price))
print("中位数所在位置的索引是：%d" % np.where(closing_price == 23.95))
print("closing_price's var 是：", numpy.var(closing_price))
print("--------------------------")
print("最高价's highest 是：", max(high_price))
print("最低价's lowest 是：", min(low_price))
print("中间值是：", (min(low_price) + max(high_price)) / 2)
print("----------价格波动-------------")
high_range = ptp(high_price)
print("该股票最高价的波动范围是：", high_range)
low_range = ptp(low_price)
print("该股票最低价的波动范围是：", low_range)
print("----------计算成交量加权平均价-------------")
vwap = np.average(closing_price, weights=volume)
print("该股票的成交量加权平均值是：%.2f" % vwap)
t = np.arange(closing_price.shape[0])  # shape[0]是一个一维数组value是行数
print(t)
twap = np.average(closing_price, weights=t)
print("该股票的时间加权平均值是：%.2f" % twap)
print("----------周末效应分析-------------")
for i in range(days.size):
    print("发生交易的天数是星期%d,当天收盘价是%f" \
          % (days[i], closing_price[i]))
print("----------计算每个交易日的平均收盘价----------")
price_avg = np.zeros(5)  # 定义包含5个元素的数组price_avg
for i in range(1, 6):
    index = np.where(days == i)
    price = np.take(closing_price, index)
    price_avg[i - 1] = np.mean(price)
    print('星期', i, '的平均收盘价是：', price_avg[i - 1])
