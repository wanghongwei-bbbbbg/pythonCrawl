# editor : XiaoHei
# time : 2022/9/11 14:58
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from datetime import datetime
import baostock as bs
from keras.models import Sequential
from keras.layers import Dense, LSTM
import tensorflow.compat.v2 as tf


sns.set_style('whitegrid')
plt.style.use("fivethirtyeight")
# 修改此处，让其图中能正常显示中文--已改
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False


def get_data(code):
    end = datetime.now()
    start = datetime(end.year - 1, end.month, end.day).strftime('%Y-%m-%d')
    end = end.strftime('%Y-%m-%d')
    # 登陆系统
    lg = bs.login()
    # 获取沪深A股历史K线数据
    rs_result = bs.query_history_k_data_plus(
        code,
        fields="date,open,high,low,close,volume",
        start_date=start,
        end_date=end,
        frequency="d",
        adjustflag="3")
    df_result = rs_result.get_data()
    # 退出系统
    bs.logout()
    df_result['date'] = df_result['date'].map(
        lambda x: datetime.strptime(x, '%Y-%m-%d'))
    _res = df_result.set_index('date')
    res = _res.applymap(lambda x: float(x))
    return res


# 将下列四只股票替换成和自己学号相关的
liquor_list = ['sh.600121', 'sh.600971',
               'sz.000552', 'sh.600397']
# '郑州煤电', '恒源煤电', '靖远煤电', '安源煤业'
company_name = ['zhengzhou', 'hengyuan', 'jingyuan', 'anyuan']
zh_company_name = ['郑州煤电', '恒源煤电', '靖远煤电', '安源煤业']
# 这里可以仿照上一句增加一条语句，以便后面将图里的英文标题改成中文标题--已增加
# for name, code in zip(company_name, liquor_list):
#     exec(f"{name}=get_data(code)")
#     # 仿照上一句，增加一句，将刚获取的数据保存到{name}.csv文件
#     exec(f"{name}.to_csv(name+'.csv')")
# 增加一个循环，在循环体里从{name}.csv 文件读取数据保存到{name}里。
for name in company_name:
    exec(f"{name}=pd.read_csv(name+'.csv')")
    exec(f"{name}['date'] = {name}['date'].map("
         f"lambda x: datetime.strptime(x, '%Y-%m-%d'))\n"
         f"_res = {name}.set_index('date')\n"
         f"{name} = _res.applymap(lambda x: float(x)) ")

# 需要批量赋值的变量名称
company_list = [zhengzhou, hengyuan, jingyuan, anyuan]
for company, com_name in zip(company_list, company_name):
    company['company_name'] = com_name
# 将四支股票数据进行纵向合并
df = pd.concat(company_list, axis=0)
df.tail(10)
print("纵向合并后的数据：")
print(df)

# 获取历史收盘价
plt.figure(figsize=(15, 6))
plt.subplots_adjust(top=1.25, bottom=1.2)

for i, company in enumerate(company_list, 1):
    plt.subplot(2, 2, i)
    company['close'].plot()
    plt.ylabel('close')
    plt.xlabel(None)
    # 修改下面一句代码，结合前面的提示，将图里的英文标题改成中文标题
    # plt.title(f"Closing Price of {company_name[i - 1]}")
    plt.title(f"{zh_company_name[i - 1]}收盘价")
plt.tight_layout()
plt.show()

plt.figure(figsize=(15, 7))
plt.subplots_adjust(top=1.25, bottom=1.2)
for i, company in enumerate(company_list, 1):
    plt.subplot(2, 2, i)
    company['volume'].plot()
    plt.ylabel('volume')
    plt.xlabel(None)
    # 修改下面一句代码，结合前面的提示，将图里的英文标题改成中文标题
    # plt.title(f"Sales Volume for {company_name[i - 1]}")
    plt.title(f"{zh_company_name[i - 1]}成交量")
plt.tight_layout()
plt.show()

# 设置移动天数
ma_day = [10, 20, 50]
for ma in ma_day:
    for company in company_list:
        column_name = f"MA for {ma} days"
        company[column_name] = company['close'].rolling(ma).mean()
# 现在继续绘制所有额外的移动平均线。
fig, axes = plt.subplots(nrows=2, ncols=2)
fig.set_figheight(8)
fig.set_figwidth(15)
# 修改斜体字部分，改用循环实现
for i, company in enumerate(company_list, 1):
    if i <= 2:
        row = 0
        col = i - 1
    else:
        row = 1
        col = i - 3
    company[['close', 'MA for 10 days', 'MA for 20 days', 'MA for 50 days']].plot(ax=axes[row, col])
    axes[row, col].set_title(f"{zh_company_name[i - 1]}移动平均线")
    axes[row, col].tick_params(axis='x', labelrotation=30)
    axes[row, col].set_xlabel("date")

fig.tight_layout()
plt.show()

for company in company_list:
    company['Daily Return'] = company['close'].pct_change()
print("添加日回报后的数据:")
print(company_list)
# 画出日收益率
fig, axes = plt.subplots(nrows=2, ncols=2)
fig.set_figheight(8)
fig.set_figwidth(15)
# 修改斜体字部分，改用循环实现
for i, company in enumerate(company_list, 1):
    if i <= 2:
        row = 0
        col = i - 1
    else:
        row = 1
        col = i - 3

    company['Daily Return'].plot(ax=axes[row, col], legend=True, linestyle='--', marker='o')
    axes[row, col].set_title(f"{zh_company_name[i - 1]}平均日回报率")
    axes[row, col].tick_params(axis='x', labelrotation=30)
    axes[row, col].set_xlabel("date")

fig.tight_layout()
plt.show()

# 注意这里使用了dropna()来处理缺失值，否则seaborn无法读取NaN值
plt.figure(figsize=(12, 7))
for i, company in enumerate(company_list, 1):
    plt.subplot(2, 2, i)
    sns.distplot(company['Daily Return'].dropna(), bins=100, color='purple')
    plt.ylabel('占比(概率)')
    plt.xlabel('日回报率')
    plt.title(f'{zh_company_name[i - 1]}日回报率')
# 也可以这样绘制
plt.tight_layout()
plt.show()

index = zhengzhou.index
closing_df = pd.DataFrame()
for company, company_n in zip(company_list, zh_company_name):
    temp_df = pd.DataFrame(index=company.index,
                           data=company['close'].values,
                           columns=[company_n])
    closing_df = pd.concat([closing_df, temp_df], axis=1)
# 看看数据
closing_df.head()

# 下面是计算当前元素与先前元素的相差百分比，即日回报
liquor_rets = closing_df.pct_change()
liquor_rets.head()
# 可以在后面加fig.suptitle()函数设置标题。
sns.jointplot(x='郑州煤电', y='郑州煤电',
              data=liquor_rets, kind='scatter',
              color='seagreen')
plt.suptitle('郑州煤电自身日收益相关性')
# 可以在后面加fig.suptitle()函数设置标题。
plt.show()

sns.jointplot(x='郑州煤电', y='恒源煤电',
              data=liquor_rets, kind='scatter')
plt.suptitle('郑州煤电和恒源煤电日收益相关性')
plt.show()

# 分析四支股票日收益相关性（pairplot+采用默认图形属性）
# 可以在后面加fig.suptitle()函数设置标题。
sns.pairplot(liquor_rets, kind='reg')
plt.suptitle('四支股票日收益相关性（pairplot+采用默认图形属性）')
plt.show()

# 通过命名为returns_fig来设置我们的图形，
# 在DataFrame上调用PairPLot
# 下面是分析四支股票日收益相关性(kde+散点图+直方图)
return_fig = sns.PairGrid(liquor_rets.dropna())
# 使用map_upper，我们可以指定上面的三角形是什么样的。
# 可以对return_fig调用fig.suptitle()函数设置标题。
return_fig.map_upper(plt.scatter, color='purple')
return_fig.fig.suptitle('四支股票日收益相关性(kde+散点图+直方图)')
# 我们还可以定义图中较低的三角形，
# 包括绘图类型(kde)或颜色映射(blueppurple)
return_fig.map_lower(sns.kdeplot, cmap='cool_d')
# 最后，我们将把对角线定义为每日收益的一系列直方图
return_fig.map_diag(plt.hist, bins=30)
plt.show()

# 下面是分析四支股票收盘价相关性(kde+散点图+直方图)
returns_fig = sns.PairGrid(closing_df)
# 可以对return_fig调用fig.suptitle()函数设置标题。
returns_fig.fig.suptitle('四支股票收盘价相关性(kde+散点图+直方图)')
returns_fig.map_upper(plt.scatter, color='purple')
returns_fig.map_lower(sns.kdeplot, cmap='cool_d')
returns_fig.map_diag(plt.hist, bins=30)
plt.show()

# 让我们用sebron来做一个每日收益的快速相关图
# 参考平均日回报率部分修改下面代码，将两幅独立的图作为子图画在同一个图
plt.figure(figsize=(12, 7))
# 日回报的快速相关图
plt.subplot(1, 2, 1)
sns.heatmap(liquor_rets.corr(),
            annot=True, cmap='summer')
plt.title("日回报的快速相关图")
# 每日收盘价的快速相关图
plt.subplot(1, 2, 2)
sns.heatmap(closing_df.corr(),
            annot=True, cmap='summer')
plt.title("每日收盘价的快速相关图")
plt.tight_layout()
plt.show()

# 让我们首先将一个新的DataFrame定义为原始liquor_rets的 DataFrame的压缩版本
rets = liquor_rets.dropna()
area = np.pi * 20
plt.figure(figsize=(10, 7))
plt.scatter(rets.mean(), rets.std(), s=area)
plt.xlabel('预期回报', fontsize=18)
plt.ylabel('风险', fontsize=18)
plt.title("预期回报图与风险相关图")


for label, x, y in zip(rets.columns, rets.mean(), rets.std()):
    if label == '安源煤业':  # 最后一只股票
        xytext = (-50, -50)
    else:
        xytext = (50, 50)
    plt.annotate(label, xy=(x, y), xytext=xytext,
                 textcoords='offset points',
                 ha='right', va='bottom', fontsize=15,
                 arrowprops=dict(arrowstyle='->',
                                 color='gray',
                                 connectionstyle='arc3,rad=-0.3'))
plt.show()

# for循环获取股价，并生成预测即可
for index_num, company in enumerate(company_list, 1):
    # 获取股票报价
    df = company.loc[:, ['open', 'high', 'low', 'close', 'volume']]
    df.head()

    plt.figure(figsize=(16, 6))
    plt.title(f'{zh_company_name[index_num - 1]}历史收盘价', fontsize=20)
    plt.plot(df['close'])
    # plt.xticks(range(0, len(df['close']), 45), rotation=30)
    plt.gcf().subplots_adjust(bottom=0.25)
    plt.xlabel('日期', fontsize=18)
    # 根据ticker的功能改变第一个为初始的数据，第二个则为距离

    plt.ylabel('收盘价 RMB (￥)', fontsize=18)
    plt.show()

    # 创建一个只有收盘价的新数据帧
    data = df.filter(['close'])
    # 将数据帧转换为numpy数组
    dataset = data.values
    # 获取要对模型进行训练的行数
    training_data_len = int(np.ceil(len(dataset) * .95))
    # 数据标准化
    from sklearn.preprocessing import MinMaxScaler

    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(dataset)
    # 创建训练集，训练标准化训练集
    train_data = scaled_data[0:int(training_data_len), :]
    # 将数据拆分为x_train和y_train数据集
    x_train = []
    y_train = []
    for i in range(60, len(train_data)):
        x_train.append(train_data[i - 60:i, 0])
        y_train.append(train_data[i, 0])
        if i <= 61:
            print(x_train)
            print(y_train)
    # 将x_train和y_train转换为numpy数组
    x_train, y_train = np.array(x_train), np.array(y_train)
    # Reshape数据
    x_train = np.reshape(x_train, (x_train.shape[0], x_train.shape[1], 1))

    # 建立LSTM模型
    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], 1)))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))
    # 编译模型
    model.compile(optimizer='adam', loss='mean_squared_error')
    # 训练模型
    model.fit(x_train, y_train, batch_size=1, epochs=1)

    # 创建测试数据集
    # 创建一个新的数组，包含从索引的缩放值
    test_data = scaled_data[training_data_len - 60:, :]
    # 创建数据集x_test和y_test
    x_test = []
    y_test = dataset[training_data_len:, :]
    for i in range(60, len(test_data)):
        x_test.append(test_data[i - 60:i, 0])
    # 将数据转换为numpy数组
    x_test = np.array(x_test)
    # 重塑的数据
    x_test = np.reshape(x_test, (x_test.shape[0], x_test.shape[1], 1))
    # 得到模型的预测值
    predictions = model.predict(x_test)
    predictions = scaler.inverse_transform(predictions)
    # 得到均方根误差(RMSE)
    rmse = np.sqrt(np.mean(((predictions - y_test) ** 2)))
    # 将训练数据、实际数据集预测数据可视化。
    train = data[:training_data_len]
    valid = data[training_data_len:]
    valid['Predictions'] = predictions
    plt.figure(figsize=(16, 6))
    plt.title(f'{zh_company_name[index_num - 1]}预测模型')
    plt.xlabel('日期', fontsize=18)
    plt.ylabel('收盘价 RMB (￥)', fontsize=18)
    plt.plot(train['close'])
    plt.plot(valid[['close', 'Predictions']])

    plt.gcf().subplots_adjust(bottom=0.25)

    plt.legend(['训练价格', '实际价格', '预测价格'])

    plt.show()
    # 按照同样方法完成其他三支股票的收盘价预测
