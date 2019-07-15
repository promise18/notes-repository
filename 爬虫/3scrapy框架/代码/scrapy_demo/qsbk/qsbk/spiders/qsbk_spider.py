# -*- coding: utf-8 -*-
import scrapy
from qsbk.items import QsbkItem
from scrapy.http.response.html import  HtmlResponse


class QsbkSpiderSpider(scrapy.Spider): # 必须继承这个scrapy.Spider类
    name = 'qsbk_spider'  # 爬虫名字
    allowed_domains = ['qiushibaike.com']  # 允许的域名
    start_urls = ['https://qiushibaike.com/text/page/1/']  # 从哪个url开始，传递一个即可
    base_domain = "https://qiushibaike.com"

    def parse(self, response):
        # duanzidivs是SelectorList类型
        duanzidivs = response.xpath("//div[@id='content-left']/div")
        for duanzidiv in duanzidivs:
            # Selector
            author = duanzidiv.xpath(".//h2/text()").get().strip()
            content = duanzidiv.xpath(".//div[@class='content']//text()").getall()
            content = "".join(content).strip()
            item = QsbkItem(author=author, content=content)
            yield item  # 将函数变成生成器
            # 如果不用yield，可以这样
            # 定义一个items列表
            # items = []
            # items.append(item) # 向列表追加项目
            # return items
        next_url = response.xpath("//ul[@class='pagination']/li[last()]/a/@href").get()
        if not next_url:
            return
        else:
            # callback:回调，返回的时候执行什么方法
            yield scrapy.Request(self.base_domain + next_url, callback=self.parse)
