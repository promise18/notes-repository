#encoding: utf-8

from scrapy import cmdline

# cmdline.execute("scrapy crawl qsbk_spider".split())等价于下面
cmdline.execute(["scrapy",'crawl','qsbk_spider'])