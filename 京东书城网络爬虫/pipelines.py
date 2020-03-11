# -*- coding: utf-8 -*-

# pipelines文件中主要用来对爬取到的数据进行后续处理
# 这里主要用来验证爬取的数据和写入数据库
# 导入链接数据库的包
import pymysql
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class JingdongPipeline(object):
    def process_item(self, item, spider):
        '''

        :param item: 爬取文件的所有字段对象
        :param spider: 爬虫
        :return: item
        '''
        # 创建数据库链接
        # 已经在MYsql数据库中创建了名为：dd的数据库
        conn = pymysql.connect(host="127.0.0.1", port=3306, user="root", passwd="1115101321",
                               db="dd", charset="utf8")
        cur = conn.cursor()
        # 设置编码格式，执行数据库操作
        cur.execute("set names utf8")
        # 遍历爬取的数据
        # 只要书名不为空就遍历所有数据
        for i in range(len(item["title"])):
            # 由于在爬虫文件中就已经取出列表中的单个商品号
            # 所以返回的只是一个字符串
            thisid = item["thisid"]
            # 其余的字段返回的都是列表，所以需要取出第一个元素
            # 作为字符串，再写入数据库的表中
            title = item["title"][0]
            cd_link = item["cd_link"][0]
            shop = item["shop"][0]
            shoplink = item["shoplink"][0]
            price = item["price"][0]
            comment = item["comment"][0]
            com_count = item["com_count"][0]
            # com_context=""
            # for j in range(0,len(item["com_context"])):
            #     com_context=com_context+item["com_context"][j]
            # 只要书名不为空，那么就执行sql语句
            if (len(title)):
                # 在dd数据库中已经创建了名为：books2的表用来存放爬取的所有数据
                sql = "insert into books2 values('" + thisid + "','" + title + "','" + cd_link + "','" + price + "','" + comment + "','" + com_count + "','" + shop + "','" + shoplink + "')"
                # 发送SQL语句
                conn.query(sql)
                # 提交，不然无法保存新建或者修改的数据
                conn.commit()
                # 查看当前爬取的数据
                print("----------------------------------------------")
                print("商品ID：" + thisid)
                print("商品名：" + title)
                print("商品链接：" + cd_link)
                print("商品价格：" + price)
                print("商品好评度：" + comment)
                print("商品评论数：" + com_count)
                print("商品店家：" + shop)
                print("商品店家连接：" + shoplink)
                print("\n")
            # 如果书名为空就不执行sql语句
            else:
                pass
        # 最后关闭所有与数据库的链接
        cur.close()
        conn.close()
        return item
