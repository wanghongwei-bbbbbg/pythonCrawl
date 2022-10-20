# editor : XiaoHei
# time : 2022/10/13 11:04

import numpy as np
import matplotlib.pyplot as plt


# 对于none值，使用数学方法，找到合理的值
def bisec(dataArray):
    for index in range(0, len(dataArray)):
        if np.isnan(dataArray[index]):
            dataArray[index] = 0.5 * \
                               (dataArray[index - 1] + \
                                dataArray[index + 1])


def inMixData2float(org_array, new_array):
    for index in range(0, len(org_array)):
        item = org_array[index]
        if item != '':
            item = float(item)
        else:
            item = None
        new_array[index] = item


def defectsCop(data_array, threshold):
    for index in range(0, len(data_array)):
        item = data_array[index]
        if item >= float(threshold):
            item = None
        data_array[index] = item


# 因为有空值，所以当成字符串处理，后续转成float
(temperature_str, humidity_str, gas_str, co_str) = np.loadtxt('ug_detect.csv', usecols=(1, 2, 3, 4), \
                                                              skiprows=1, delimiter=',', dtype=type, unpack=True)
print("读取出的数组是temperature_str：\n", temperature_str)

print(temperature_str.dtype)
temperature = np.ndarray(len(temperature_str))
for i in range(0, len(temperature_str)):
    item = temperature_str[i]
    if item != '':
        item = float(item)
    else:
        item = None
    temperature[i] = item

for index in range(0, len(temperature)):
    item = temperature[index]
    if item >= 500.0:
        item = None
    temperature[index] = item

print(temperature)
# 绘制数据图，数据可视化
t = np.arange(len(temperature))
plt.plot(t, temperature)
plt.plot(t, temperature, 'pr')
plt.show()

print("使用numpy处理其他指标")
humidity = np.ndarray(len(humidity_str))
gas = np.ndarray(len(gas_str))
co = np.ndarray(len(co_str))
inMixData2float(humidity_str, humidity)
defectsCop(humidity, 200)
inMixData2float(gas_str, gas)
defectsCop(gas, 100)
inMixData2float(co_str, co)
defectsCop(co, 100)
bisec(humidity)
bisec(gas)
bisec(co)

print("井下的湿度是：\n", humidity)
print("井下的瓦斯气体浓度是：\n", gas)
print("井下的一氧化碳浓度是：\n", co)

print("保存处理后的湿度数据文件。")
np.savetxt('ug_humidity.csv', humidity, delimiter=',', fmt='%.2f')
print("保存处理后的瓦斯浓度数据文件。")
np.savetxt('ug_gas.csv', \
           gas,
           delimiter=',', \
           fmt='%.2f')
print("保存处理后的一氧化碳浓度数据文件。")
np.savetxt('ug_co.csv', \
           co,
           delimiter=',', \
           fmt='%.2f')
