# coding=utf-8

'''
数据分析文件
'''
# 存储和处理矩阵
import numpy
# 数据分析
import pandas
# Kmeans分析
from sklearn.cluster import KMeans
# 画图包
import matplotlib.pylab

# 首先读取指定目录下的excel文件
data = pandas.read_excel("C:\\Users\\Administrator\\Desktop\pycharm\\jingdong\\jingdong\\data\\gbk\\books1.xls",
                         sep=",",
                         encoding="gbk")
# excel会把第一行作为标题忽略(第0行0列数据)
# print(datata.values[0])
# 数值数据，结果的索引将包括计数，平均值，标准差，最小值，最大值以及较低的百分位数和50
print(data.describe())
# 不破坏原来的数据,把所有数据都重新赋值
data_new = data.values


# 画折线图的函数
def line_chart(data_new):
    '''
    画折线图
    :param data_new:二维数组数据
    :return: None
    '''
    # 方便处理，先转置
    data_T = data_new.T
    # 获得所有价格数据
    # 价格原本在第4列，转置后就是第4行
    price_data = data_T[4]
    # 得到评论数数据
    # 评论数原本在第6列，转置后就是第6行
    comment_data = data_T[6]
    # 设置横纵坐标轴名称
    matplotlib.pylab.xlabel("price")
    matplotlib.pylab.ylabel("comment count")
    # 折线图：横轴价格，纵轴评论数
    matplotlib.pylab.plot(price_data, comment_data)
    # 画出折线图
    matplotlib.pylab.show()


# 画散点图的函数
def scatter_chart(data_new):
    '''
    画散点图
    :param data_new: 二维数组数据
    :return: None
    '''
    # 方便处理，先转置
    data_T = data_new.T
    # 获得所有价格数据
    # 价格原本在第4列，转置后就是第4行
    price_data = data_T[4]
    # 得到评论数数据
    # 评论数原本在第6列，转置后就是第6行
    comment_data = data_T[6]
    matplotlib.pylab.xlabel("price")
    matplotlib.pylab.ylabel("comment count")
    # 散点图
    matplotlib.pylab.plot(price_data, comment_data, 'o')
    matplotlib.pylab.show()


# 异常值处理函数
def except_pro(data_new, pri_low, pri_upper, comm_low, comm_upper):
    '''
    异常值处理
    :param data_new:二维数组数据
    :param pri_low:价格下界
    :param pri_upper:价格上界
    :param comm_low:评论数下界
    :param comm_upper:评论数上界
    :return:处理后的二维数组数据
    '''

    # 异常值的处理由于数据太多采用了删除法
    # 数据清理和发现缺失值
    # 获得行
    row = len(data_new)
    # 获得列
    col = len(data_new[0])
    # 创建需要删除的数据的行标
    delete_row = []
    # 通过观察散点图设施价格的上下界和评论数的上下界
    for i in range(0, row):
        for j in range(0, col):
            # 价格异常处理
            if (data_new[i][4] < pri_low or data_new[i][4] > pri_upper):
                # data_new=numpy.delete(data_new,i,0)
                # 把出现异常的数据的行记录下来
                delete_row.append(i)
            if (data_new[i][6] < comm_low or data_new[i][6] > comm_upper):
                # data_new=numpy.delete(data_new, i, 0)
                delete_row.append(i)
    # print(len(data_new))
    # print(delete_row)
    # 创建处理后的数据列表
    data2_new = []
    for i in range(row):
        # 如果数据不再需要删除的行标中就加入该数据
        if (i not in delete_row):
            data2_new.append(data_new[i])
    # 转成数组
    data2_new = numpy.array(data2_new)
    return data2_new


# 折线图
line_chart(data_new)
# 散点图
scatter_chart(data_new)

# 异常值的处理：价格主要集中在1~150，评论数主要集中在10~100000
# 异常值的处理由于数据太多采用了删除法
data2_new = except_pro(data_new, 1, 150, 10, 100000)

# 删除异常之后的散点图
scatter_chart(data2_new)

# 可以看到价格主要集中在10~120，
# 评论数主要集中在200~7000
# 再一次使用删除数据
data3_new = except_pro(data2_new, 10, 120, 200, 7000)

# 处理之后的散点图
scatter_chart(data3_new)
print(len(data3_new))
# 处理最后的数据共有693

# 使用KMeans方法聚类分析
# 在10~120的价格中，把所有书籍按照评论数分为三类
# 调用python关于机器学习sklearn库中的KMeans
# 转换数据格式
data_T3 = data3_new.T
# 形成n*2的矩阵
tmp = numpy.array([data_T3[4], data_T3[6]]).T
# 设置分为3类，并训练数据
kms = KMeans(n_clusters=3)
# 并训练数据
y = kms.fit_predict(tmp)
# 将分类结果以散点图形式展示
fig = matplotlib.pylab.figure(figsize=(10, 6))
matplotlib.pylab.xlabel('price')
matplotlib.pylab.ylabel('comnum')
for i in range(0, len(y)):
    # 第一类
    if (y[i] == 0):
        # 星型红色
        matplotlib.pylab.plot(tmp[i, 0], tmp[i, 1], "*r")
    # 第二类
    elif (y[i] == 1):
        # 矩形黄色
        matplotlib.pylab.plot(tmp[i, 0], tmp[i, 1], "sy")
    # 第三类
    elif (y[i] == 2):
        # 五边形蓝色
        matplotlib.pylab.plot(tmp[i, 0], tmp[i, 1], "pb")
matplotlib.pylab.show()
