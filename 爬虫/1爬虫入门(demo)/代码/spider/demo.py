import requests
import re
# 下载一个网页
url = 'http://www.jingcaiyuedu.com/book/15205.html'
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
}
# 模拟浏览器发送http请求
response = requests.get(url, headers=headers)
print(response.status_code)
# 编码方式
# response.encoding = "utf-8"
# 网页源码
html = response.content.decode('utf-8')
# 小说的名称
title = re.findall(r'<meta property="og:title" content="(.*?)"/>',html)[0]
print(title)
# 获取每一章的信息（章节，url）
dl = re.findall(r'<dl class="panel-body panel-chapterlist">.*?</dl>', html, re.S)[1]  # 列表
chapter_info_list = re.findall(r'href="(.*?)">(.*?)<',  dl)


# 新建一个文件，保存小说的内容
# with open('%s.txt' % title) as f:
# 循环每一章节，分别取下载
fb = open('%s.txt' % title,'w',encoding='utf-8')
for chapter_info in chapter_info_list:
    # chapter_title = chapter_info[1]
    # chapter_url = chapter_info[0]
    chapter_url,chapter_title = chapter_info
    chapter_url = "http://www.jingcaiyuedu.com%s" % chapter_url
    # print(chapter_url)
    # 下载章节内容
    chapter_response = requests.get(chapter_url,headers= headers)
    # print(chapter_response.status_code)
    chapter_response.encoding = 'utf-8'
    chapter_html = chapter_response.text
    # print(chapter_html)
    # 提取章节内容
    chapter_content= re.findall(r'<div class="panel-body" id="htmlContent">(.*?)</div>', chapter_html,re.S)[0]
    print("状态码：%d。正在提取:%s" % (chapter_response.status_code,chapter_title))
    # print(chapter_content)
    #  清洗数据
    chapter_content = chapter_content.replace(' ','')
    chapter_content = chapter_content.replace('&nbsp;','')
    chapter_content = chapter_content.replace('<br/>','')

    # # 持久化
    fb.write(chapter_title)
    fb.write(chapter_content)
    fb.write('\n')




