# -*- coding: utf-8 -*-

'''
数据挖掘文件
'''
# 导入URL包，接收网页请求的模块
import urllib.request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
# 导入items的爬取字段文件
from jingdong.items import JingdongItem
# 导入正则表达式的包
import re


# 爬虫类
class JdSpider(CrawlSpider):
    # 设置当前爬虫文件名为“jd”
    name = 'jd'
    # 这是允许爬取网页的域名
    # 本爬虫爬取的是京东商城
    allowed_domains = ['jd.com']
    # 设置爬虫第一次爬取的网页链接
    start_urls = ['https://list.jd.com/list.html?cat=1713,3287,3797&page=1&sort=sort_rank_asc&trans=1&JL=6_0_0#J_main']
    # 设置相应的规则和回调函数
    # allow是用正则表达式来提取网页的关键信息，匹配所有商品详情页面链接
    # 这里提取的是商品ID号；
    # callback是回调函数，就是爬取下一商品再次调用的函数
    rules = (
        Rule(LinkExtractor(allow='//item.jd.com/.*?.html'), callback='parse_item', follow=True),
    )

    # 设置代理IP地址
    proxy_addr = "122.237.104.9:80"

    # 代理服务器函数
    def use_proxy(self, url, proxy_addr):
        '''
        因为，同一个IP在短时间内过多地爬取京东商品信息会把本地IP禁掉
        所以，需要通过免费的代理服务器去爬取信息
        如果代理服务器不能用，则使用本地IP爬取信息
        :param url:爬取网页的链接
        :param proxy_addr:代理服务器IP地址
        :return:爬取文件的所有字段对象
        '''
        # 首先需要把爬虫伪装成浏览器，就是浏览器伪装技术
        # 只要加上头文件的"User-Agent"就可以伪装成功
        # 这里是搜狗浏览器的头文件
        headers = ("User-Agent",
                   "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        # 设置代理服务器协议及IP
        proxy = urllib.request.ProxyHandler({"http": proxy_addr})
        # 封装代理IP或请求头
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        # 添加头文件
        opener.addheaders = [headers]
        # 使用install_opener将配置好的proxy安装到全局环境中，
        # 这样所有的urllib.urlopen都会自动使用代理
        urllib.request.install_opener(opener)

        # 打开url链接，并读取内容
        # 这里使用utf-8编码格式把读取的网页内容个data
        data = urllib.request.urlopen(url).read().decode("utf-8", "ignore")
        return data

    #回调函数
    def parse_item(self, response):
        '''
        回调函数：主要用来爬取商品信息
        :param response:获取响应
        :return:爬取文件的所有字段对象
        '''
        # 设置异常抛出
        try:
            # 首先创建爬取字段的对象
            item = JingdongItem()
            # i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
            # i['name'] = response.xpath('//div[@id="name"]').extract()
            # i['description'] = response.xpath('//div[@id="description"]').extract()
            # 返回响应的链接
            # 获取当前爬取的网址,既是商品详情页面的网址
            thisurl = response.url
            # print(thisurl)
            # 正则表达式:判断是不是一个商品网页，匹配的是商品号
            # 使用懒惰模式只匹配一个ID号
            pat = 'item.jd.com/(.*?).html'
            # 查找当前网页中有没有该商品号，返回第一个匹配的字符串的匹配对象
            x = re.search(pat, thisurl)
            # 只要不为空就表示有，表示获取了匹配的对象
            if x:
                # 经过网页源文件的分析以下信息是直接可从源文件中得到的
                # 商品ID、商品名、商品链接、店家名、店家链接
                # 得到第一件商品的id号
                item["thisid"] = thisid = re.compile(pat).findall(thisurl)[0]
                # 由于在网页源文件中已经有以下字段，
                # 所以，可以通过响应的xpath表达式来匹配出html中的各种信息
                # 商品名称
                item["title"] = title = response.xpath('//html/head/title/text()').extract()
                # 商品链接
                item["cd_link"] = cd_link = response.xpath('//html/head/link[@rel="canonical"]/@href').extract()
                # 商品店家
                item["shop"] = shop = response.xpath('//div[@class="name"]/a/@title').extract()
                # 商品店家链接
                item["shoplink"] = shoplink = response.xpath('//div[@class="name"]/a/@href').extract()
                # print(title,shop,shoplink)

                # 以下商品信息需要通过抓包获取url链接
                # 再通过正则表达式来匹配出我们需要的字段
                # 价格连接：前面''里面的都是固定的，知识最后商品ID的不同
                priceurl = 'https://p.3.cn/prices/mgets?skuIds=J_' + str(thisid)
                # 好评度和评论数连接：前面''里面的都是固定的，知识商品ID的不同
                commenturl = "https://sclub.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98vv41915&productId=" + str(
                    thisid) + "&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&fold=1"
                # print(priceurl)
                # print(commenturl)

                # 通过代理服务器获取网页的内容
                # 把有价格的网页信息取出来
                pricedata = self.use_proxy(priceurl, JdSpider.proxy_addr)
                # pricedata = urllib.request.urlopen(priceurl).read().decode("utf-8", "ignore")
                # 把有好评度,评论的网页信息取出来
                commentdata = self.use_proxy(commenturl, JdSpider.proxy_addr)
                # commentdata = urllib.request.urlopen(commenturl).read().decode("utf-8", "ignore")
                # 以下信息是要抓包获取的
                # 设置正则表达式
                # 价格
                pricepat = '"p":"(.*?)"'
                # 通过正则表达式在价格网页中匹配出信息
                item["price"] = price = re.compile(pricepat).findall(pricedata)
                # 好评度
                commentpat = 'goodRateShow":(.*?),'
                # 通过正则表达式在评论网页中匹配出信息
                item["comment"] = comment = re.compile(commentpat).findall(commentdata)
                # 评论数
                com_countpat = 'commentCount":(.*?),'
                # 通过正则表达式在评论网页中匹配出信息
                item["com_count"] = com_count = re.compile(com_countpat).findall(commentdata)
                # 打印出所有匹配的信息看有没有错误
                # 只有当商品名称和价格都爬取到才打印
                if (len(title) and len(price)):
                    print("----------------------------------------------")
                    print("商品ID：" + thisid)
                    print("商品名：" + title[0])
                    print("商品链接：" + cd_link[0])
                    print("商品价格：" + price[0])
                    print("商品好评度：" + comment[0])
                    print("商品评论数：" + com_count[0])
                    print("商品店家：" + shop[0])
                    print("商品店家连接：" + shoplink[0])
                    print("\n")
                else:
                    pass
            else:
                pass
            return item
        # 如果出现异常就打印出来
        except Exception as e:
            print(e)
