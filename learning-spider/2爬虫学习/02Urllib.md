# Urllib库详解

官方文档地址：<https://docs.python.org/3/library/urllib.html>

## 什么是urllib

Urllib是Python内置的HTTP请求库：

urllib.request			 请求模块
urllib.error 				异常处理模块
urllib.parse 			   url解析模块
urllib.robotparser 	 robots.txt解析模块 (用的较少)

## Urlopen

urllib.request.urlopen(url, data=None, [timeout, ]*, cafile=None, capath=None, cadefault=False, context=None)

~~~python
import urllib.request
# 向百度发出请求并返回响应
response = urllib.request.urlopen('http://www.baidu.com')
print(response.read().decode('utf-8'))
~~~

urlopen一般常用的有三个参数，它的参数如下：
urllib.requeset.urlopen(url,data,timeout)
response.read()可以获取到网页的内容，如果没有read()，将返回如下内容：

```python
<http.client.HTTPResponse object at 0x000001E716F6ADD8>
```

### data使用

~~~python
import urllib.parse
import urllib.request

data = bytes(urllib.parse.urlencode({'word': 'hello'}), encoding='utf8')
response = urllib.request.urlopen('http://httpbin.org/post', data=data)
print(response.read())
~~~

这里就用到urllib.parse，通过bytes(urllib.parse.urlencode())可以将需要post的数据转换放到urllib.request.urlopen的data参数中。这样就完成了一次post请求。
如果我们要传递数据就是用post请求方式进行请求，如果没有data参数就是get请求方式。

### timeout使用

在某些网络情况不好或者服务器端异常的情况会出现请求慢的情况，或者请求异常，所以这个时候我们需要给请求设置一个超时时间，而不是让程序一直在等待结果。

~~~python
import urllib.request

response = urllib.request.urlopen('http://httpbin.org/get', timeout=1)
print(response.read())
~~~

将timeout设为0.1，运行程序会提示：

```python
URLError: <urlopen error timed out>
```

因此捕获异常：

~~~python
import socket
import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://httpbin.org/get', timeout=0.1)
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout):
        print('TIME OUT')
~~~

## 响应

### 响应类型

```python
import urllib.request

response = urllib.request.urlopen('https://www.python.org')
print(type(response))
```

结果：<class 'http.client.HTTPResponse'>

### 状态码、响应头

我们可以通过response.status、response.getheaders().response.getheader("server")，获取状态码以及头部信息。
response.read()获得的是响应体的内容

```python
import urllib.request

response = urllib.request.urlopen('https://www.python.org')
print(response.status)
print(response.getheaders())
print(response.getheader('Server'))
print(response.read().decode('utf-8'))
```

结果：

200
[('Server', 'nginx'), ('Content-Type', 'text/html; charset=utf-8'), ('X-Frame-Options', 'DENY'), ('Via', '1.1 vegur'), ('Via', '1.1 varnish'), ('Content-Length', '48260'), ('Accept-Ranges', 'bytes'), ('Date', 'Fri, 05 Jul 2019 08:59:20 GMT'), ('Via', '1.1 varnish'), ('Age', '955'), ('Connection', 'close'), ('X-Served-By', 'cache-iad2120-IAD, cache-hnd18730-HND'), ('X-Cache', 'HIT, HIT'), ('X-Cache-Hits', '2, 1244'), ('X-Timer', 'S1562317160.403277,VS0,VE0'), ('Vary', 'Cookie'), ('Strict-Transport-Security', 'max-age=63072000; includeSubDomains')]
nginx

上述的urlopen只能用于一些简单的请求，因为它无法添加一些header信息，如果后面写爬虫我们可以知道，很多情况下我们是需要添加头部信息去访问目标站的，这个时候就用到了urllib.request。

## Request

有很多网站为了防止程序爬虫爬网站造成网站瘫痪，会需要携带一些headers头部信息才能访问，最常见的有user-agent参数。

例子

~~~python
import urllib.request

request = urllib.request.Request('https://python.org')
response = urllib.request.urlopen(request)
print(response.read().decode('utf-8'))
~~~

和上面直接用urlopen方式效果一致。

给请求添加头部信息，从而定制自己请求网站是时的头部信息

~~~python
from urllib import request, parse # 导入模块

url = 'http://httpbin.org/post'
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    'Host': 'httpbin.org'
}
dict = {
    'name': 'zhaofan'
}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, headers=headers, method='POST')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
~~~

另一种方式

~~~python
from urllib import request, parse

url = 'http://httpbin.org/post'
dict = {
    'name': 'Germey'
}
data = bytes(parse.urlencode(dict), encoding='utf8')
req = request.Request(url=url, data=data, method='POST')
req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)')
response = request.urlopen(req)
print(response.read().decode('utf-8'))
~~~

（可以第一种方式比较好）

## Handler

### 代理ProxyHandler

通过urllib.request.ProxyHandler()可以设置代理,网站它会检测某一段时间某个IP 的访问次数，如果访问次数过多，它会禁止你的访问,所以这个时候需要通过设置代理来爬取数据

~~~python
import urllib.request

proxy_handler = urllib.request.ProxyHandler({
    'http': 'http://127.0.0.1:9743',
    'https': 'https://127.0.0.1:9743'
})
opener = urllib.request.build_opener(proxy_handler)
response = opener.open('http://httpbin.org/get')
print(response.read())
~~~

### cookie:HTTPCookiProcessor

cookie中保存中我们常见的登录信息，有时候爬取网站需要携带cookie信息访问,这里用到了http.cookijar，用于获取cookie以及存储cookie

~~~python
import http.cookiejar, urllib.request # 导入模块
cookie = http.cookiejar.CookieJar()
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
for item in cookie:
    print(item.name+"="+item.value)
~~~

同时cookie可以写入到文件中保存，有两种方式http.cookiejar.MozillaCookieJar和http.cookiejar.LWPCookieJar()，当然你自己用哪种方式都可以。

1. http.cookiejar.MozillaCookieJar()方式

~~~python
import http.cookiejar, urllib.request
filename = "cookie.txt"
cookie = http.cookiejar.MozillaCookieJar(filename)# 第一种方式
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)
~~~

2. http.cookiejar.LWPCookieJar()方式

~~~python
import http.cookiejar, urllib.request
filename = 'cookie.txt'
cookie = http.cookiejar.LWPCookieJar(filename) # 第二种方式
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
cookie.save(ignore_discard=True, ignore_expires=True)
~~~

同样的如果想要通过获取文件中的cookie获取的话可以通过load方式，当然用哪种方式写入的，就用哪种方式读取。

~~~python
import http.cookiejar, urllib.request
cookie = http.cookiejar.LWPCookieJar()
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
handler = urllib.request.HTTPCookieProcessor(cookie)
opener = urllib.request.build_opener(handler)
response = opener.open('http://www.baidu.com')
print(response.read().decode('utf-8'))
~~~

## 异常处理

~~~python
from urllib import request, error
try:
    response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.URLError as e:
    print(e.reason)
~~~

上述代码访问的是一个不存在的页面，通过捕捉异常，我们可以打印异常错误

这里有两个异常错误：
URLError,HTTPError，HTTPError是URLError的子类

URLError里只有一个属性：reason,即抓异常的时候只能打印错误信息，类似上面的例子

HTTPError里有三个属性：code,reason,headers，即抓异常的时候可以获得code,reson，headers三个信息，例子如下：

~~~python
from urllib import request, error

try:
    response = request.urlopen('http://cuiqingcai.com/index.htm')
except error.HTTPError as e:
    print(e.reason, e.code, e.headers, sep='\n')
except error.URLError as e:
    print(e.reason)
else:
    print('Request Successfully')
~~~

同时，e.reason其实也可以在做深入的判断，例子如下：

~~~python
import socket

from urllib import error,request

try:
    response = request.urlopen("http://www.pythonsite.com/",timeout=0.001)
except error.URLError as e:
    print(type(e.reason)) # <class 'socket.timeout'>
    if isinstance(e.reason,socket.timeout):
        print("time out")
~~~

## URL解析

### urlparse

urllib.parse.urlparse(urlstring, scheme='', allow_fragments=True)

~~~python
from urllib.parse import urlparse

result = urlparse('http://www.baidu.com/index.html;user?id=5#comment')
print(type(result), result)
~~~

结果：

```
<class 'urllib.parse.ParseResult'> ParseResult(scheme='http', netloc='www.baidu.com', path='/index.html', params='user', query='id=5', fragment='comment')
```

这里就是可以对你传入的url地址进行拆分。

同时我们是可以指定协议类型：

~~~python
from urllib.parse import urlparse

result = urlparse('www.baidu.com/index.html;user?id=5#comment', scheme='https')
print(result)
~~~

结果：

```
ParseResult(scheme='https', netloc='', path='www.baidu.com/index.html', params='user', query='id=5', fragment='comment')
```

这样拆分的时候协议类型部分就会是你指定的部分，当然如果你的url里面已经带了协议，你再通过scheme指定的协议就不会生效。

### urlunparse

功能和urlparse的功能相反，它是用于拼接，例子如下：

~~~python
from urllib.parse import urlunparse

data = ['http','www.baidu.com','index.html','user','a=123','commit']
print(urlunparse(data))
~~~

结果：`http://www.baidu.com/index.html;user?a=6#comment`

### urljoin

这个的功能其实是做拼接的，例子如下：

~~~python
from urllib.parse import urljoin

print(urljoin('http://www.baidu.com', 'FAQ.html'))
print(urljoin('http://www.baidu.com', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html'))
print(urljoin('http://www.baidu.com/about.html', 'https://cuiqingcai.com/FAQ.html?question=2'))
print(urljoin('http://www.baidu.com?wd=abc', 'https://cuiqingcai.com/index.php'))
print(urljoin('http://www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com', '?category=2#comment'))
print(urljoin('www.baidu.com#comment', '?category=2'))
~~~

结果：

~~~tex
http://www.baidu.com/FAQ.html
https://cuiqingcai.com/FAQ.html
https://cuiqingcai.com/FAQ.html
https://cuiqingcai.com/FAQ.html?question=2
https://cuiqingcai.com/index.php
http://www.baidu.com?category=2#comment
www.baidu.com?category=2#comment
www.baidu.com?category=2
~~~

从拼接的结果我们可以看出，拼接的时候后面的优先级高于前面的url

### urlencode

这个方法可以将字典转换为url参数，例子如下

~~~python
from urllib.parse import urlencode

params = {
    "name":"zhaofan",
    "age":23,
}
base_url = "http://www.baidu.com?"

url = base_url+urlencode(params)
print(url)
~~~

结果` http://www.baidu.com?name=germey&age=2`