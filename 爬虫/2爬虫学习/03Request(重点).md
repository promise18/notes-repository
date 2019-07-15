# 什么是Requests

Requests是用python语言基于urllib编写的，采用的是Apache2 Licensed开源协议的HTTP库
urllib是非常不方便的，而Requests它会比urllib更加方便，可以节约我们大量的工作。requests是python实现的最简单易用的HTTP库，建议爬虫使用requests库。

# Request用法详解

## 实例引入（乱码问题）

```python
import requests

response  = requests.get("https://www.baidu.com")
print(type(response)) 
print(response.status_code) # 状态码
print(type(response.text)) 
print(response.text) # 网页内容（会出现乱码）
print(response.cookies) # cookie信息
print(response.content) # 网页内容（二进制文件）
print(response.content.decode("utf-8")) #（解决乱码）
```

这里有个问题需要注意一下：
很多情况下的网站如果直接response.text会出现乱码的问题，所以使用response.content，这样返回的数据格式是二进制格式，然后通过decode()转换为utf-8，这样就解决了通过response.text直接返回显示乱码的问题.

请求发出后，Requests 会基于 HTTP 头部对响应的编码作出有根据的推测。当你访问 response.text 之时，Requests 会使用其推测的文本编码。你可以找出 Requests 使用了什么编码，并且能够使用 response.encoding 属性来改变它.如：

```python
response =requests.get("http://www.baidu.com")
response.encoding="utf-8"
print(response.text)
```

**不管是通过response.content.decode("utf-8)的方式还是通过response.encoding="utf-8"的方式都可以避免乱码的问题发生，如果上面无法解决还有：

```
response.encoding = 'gbk'
```

或者

```
response.content.decode("gbk")
```

## 各种请求方式

```python
import requests
requests.post("http://httpbin.org/post")
requests.put("http://httpbin.org/put")
requests.delete("http://httpbin.org/delete")
requests.head("http://httpbin.org/get")
requests.options("http://httpbin.org/get")
```

# 请求

## 基本Get请求

~~~python
import requests

response = requests.get('http://httpbin.org/get')
print(response.text)
~~~

### 带参数的GET请求

```python
import requests

response = requests.get("http://httpbin.org/get?name=zhaofan&age=23")
print(response.text)
```

如果我们想要在URL查询字符串传递数据，通常我们会通过httpbin.org/get?key=val方式传递。Requests模块允许使用params关键字传递参数，以一个字典来传递这些参数，例子如下：

~~~python
import requests
data = {
    "name":"zhaofan",
    "age":22
}
response = requests.get("http://httpbin.org/get",params=data)
print(response.url)
print(response.text)
~~~

上述两种的结果是相同的，通过params参数传递一个字典内容，从而直接构造url
注意：第二种方式通过字典的方式的时候，如果字典中的参数为None则不会添加到url上

### 解析json

~~~python
import requests
import json

response = requests.get("http://httpbin.org/get")
print(type(response.text))
print(response.json()) # 解析json，json字符串转换成字典或者列表
print(json.loads(response.text))# 效果和上一行一样
print(type(response.json()))
~~~

结果：

```
<class 'str'>
{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.22.0'}, 'origin': '218.2.216.27, 218.2.216.27', 'url': 'https://httpbin.org/get'}
{'args': {}, 'headers': {'Accept': '*/*', 'Accept-Encoding': 'gzip, deflate', 'Host': 'httpbin.org', 'User-Agent': 'python-requests/2.22.0'}, 'origin': '218.2.216.27, 218.2.216.27', 'url': 'https://httpbin.org/get'}
<class 'dict'>
```

从结果可以看出requests里面集成的json其实就是执行了json.loads()方法，两者的结果是一样的。

### 获取二进制文件

在上面提到了response.content，这样获取的数据是二进制数据，同样的这个方法也可以用于下载图片以及
视频资源

~~~python
import requests

response = requests.get("https://github.com/favicon.ico")
print(type(response.text), type(response.content)) # <class 'str'> <class 'bytes'>
print(response.text) # 乱码
print(response.content) # 二进制文件
~~~

~~~python
import requests

response = requests.get("https://github.com/favicon.ico")
with open('favicon.ico', 'wb') as f: # fileopen方法，命名传入图片的名称，wb：写模式
    f.write(response.content)
    f.close()
~~~

### 添加headers（用户代理）

和前面urllib模块一样，我们同样可以定制headers的信息，如当我们直接通过requests请求知乎网站的时候，默认是无法访问的。

因为访问知乎需要头部信息，这个时候我们在谷歌浏览器里输入chrome://version,就可以看到用户代理，将用户代理添加到头部信息。

![1562378994308](D:\笔记\爬虫\2爬虫学习\03Request(重点).assets\1562378994308.png)

Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36

~~~python
import requests
headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    'cookies':''
}
response =requests.get("https://www.zhihu.com",headers=headers)

print(response.text)
~~~

这样就可以访问了。

## 基本post请求

通过在发送post请求时添加一个data参数，这个data参数可以通过字典构造成，这样对于发送post请求就非常方便。

~~~python
import requests

data = {
    "name":"zhaofan",
    "age":23
}
response = requests.post("http://httpbin.org/post",data=data)
print(response.text)
~~~

同样的在发送post请求的时候也可以和发送get请求一样通过headers参数传递一个字典类型的数据。

~~~python
import requests

data = {'name': 'germey', 'age': '22'}
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'
}
response = requests.post("http://httpbin.org/post", data=data, headers=headers)
print(response.json())
~~~

# 响应

### response属性

~~~python
import requests

response = requests.get('http://www.jianshu.com')
print(type(response.status_code), response.status_code)
print(type(response.headers), response.headers)
print(type(response.cookies), response.cookies)
print(type(response.url), response.url)
print(type(response.history), response.history)
~~~

结果：

```
<class 'int'> 200
<class 'requests.structures.CaseInsensitiveDict'> {'Server': 'Tengine', 'Content-Type': 'text/html; charset=utf-8', 'Transfer-Encoding': 'chunked', 'Connection': 'keep-alive', 'Date': 'Sat, 06 Jul 2019 02:25:05 GMT', 'Vary': 'Accept-Encoding', 'X-Frame-Options': 'DENY', 'X-XSS-Protection': '1; mode=block', 'X-Content-Type-Options': 'nosniff', 'ETag': 'W/"94175227640b91f9d2362484d07ebc04"', 'Cache-Control': 'max-age=0, private, must-revalidate', 'Set-Cookie': 'locale=zh-CN; path=/', 'X-Request-Id': 'a694ced7-2224-4f60-b49f-52a55689471b', 'X-Runtime': '0.010714', 'Strict-Transport-Security': 'max-age=31536000; includeSubDomains; preload', 'Content-Encoding': 'gzip', 'Via': 'cache45.l2cm12-6[20,0], cache14.cn1080[86,0]', 'Timing-Allow-Origin': '*', 'EagleId': '755bb22215623799053826610e'}
<class 'requests.cookies.RequestsCookieJar'> <RequestsCookieJar[<Cookie locale=zh-CN for www.jianshu.com/>]>
<class 'str'> https://www.jianshu.com/
<class 'list'> [<Response [301]>]
```

### 状态码判断

~~~python
import requests

response = requests.get('http://www.jianshu.com/hello.html')
exit() if not response.status_code == requests.codes.not_found else print('404 Not Found')
~~~

~~~python
import requests

response = requests.get('http://www.jianshu.com')
exit() if not response.status_code == 200 else print('Request Successfully')
~~~

~~~python
100: ('continue',),
101: ('switching_protocols',),
102: ('processing',),
103: ('checkpoint',),
122: ('uri_too_long', 'request_uri_too_long'),
200: ('ok', 'okay', 'all_ok', 'all_okay', 'all_good', '\\o/', '✓'),
201: ('created',),
202: ('accepted',),
203: ('non_authoritative_info', 'non_authoritative_information'),
204: ('no_content',),
205: ('reset_content', 'reset'),
206: ('partial_content', 'partial'),
207: ('multi_status', 'multiple_status', 'multi_stati', 'multiple_stati'),
208: ('already_reported',),
226: ('im_used',),

# Redirection.
300: ('multiple_choices',),
301: ('moved_permanently', 'moved', '\\o-'),
302: ('found',),
303: ('see_other', 'other'),
304: ('not_modified',),
305: ('use_proxy',),
306: ('switch_proxy',),
307: ('temporary_redirect', 'temporary_moved', 'temporary'),
308: ('permanent_redirect',
      'resume_incomplete', 'resume',), # These 2 to be removed in 3.0

# Client Error.
400: ('bad_request', 'bad'),
401: ('unauthorized',),
402: ('payment_required', 'payment'),
403: ('forbidden',),
404: ('not_found', '-o-'),
405: ('method_not_allowed', 'not_allowed'),
406: ('not_acceptable',),
407: ('proxy_authentication_required', 'proxy_auth', 'proxy_authentication'),
408: ('request_timeout', 'timeout'),
409: ('conflict',),
410: ('gone',),
411: ('length_required',),
412: ('precondition_failed', 'precondition'),
413: ('request_entity_too_large',),
414: ('request_uri_too_large',),
415: ('unsupported_media_type', 'unsupported_media', 'media_type'),
416: ('requested_range_not_satisfiable', 'requested_range', 'range_not_satisfiable'),
417: ('expectation_failed',),
418: ('im_a_teapot', 'teapot', 'i_am_a_teapot'),
421: ('misdirected_request',),
422: ('unprocessable_entity', 'unprocessable'),
423: ('locked',),
424: ('failed_dependency', 'dependency'),
425: ('unordered_collection', 'unordered'),
426: ('upgrade_required', 'upgrade'),
428: ('precondition_required', 'precondition'),
429: ('too_many_requests', 'too_many'),
431: ('header_fields_too_large', 'fields_too_large'),
444: ('no_response', 'none'),
449: ('retry_with', 'retry'),
450: ('blocked_by_windows_parental_controls', 'parental_controls'),
451: ('unavailable_for_legal_reasons', 'legal_reasons'),
499: ('client_closed_request',),

# Server Error.
500: ('internal_server_error', 'server_error', '/o\\', '✗'),
501: ('not_implemented',),
502: ('bad_gateway',),
503: ('service_unavailable', 'unavailable'),
504: ('gateway_timeout',),
505: ('http_version_not_supported', 'http_version'),
506: ('variant_also_negotiates',),
507: ('insufficient_storage',),
509: ('bandwidth_limit_exceeded', 'bandwidth'),
510: ('not_extended',),
511: ('network_authentication_required', 'network_auth', 'network_authentication'),
~~~

# 高级操作

## 文件上传

构造一个字典，通过file参数传递

~~~python
import requests

files = {'file': open('favicon.ico', 'rb')} # 读操作
response = requests.post("http://httpbin.org/post", files=files)
print(response.text)
~~~

## 获取cookie

~~~python
import requests

response = requests.get("https://www.baidu.com")
print(response.cookies)
for key, value in response.cookies.items():
    print(key + '=' + value)
~~~

## 会话维持

### 模拟登陆

下面这种方法是错误的，因为这种方式是两次requests请求之间是独立的。

~~~python
import requests

requests.get('http://httpbin.org/cookies/set/number/123456789')
response = requests.get('http://httpbin.org/cookies')
print(response.text)
~~~

正确的做法是通过创建一个session对象，两次请求都通过这个对象访问。

~~~python
import requests
s = requests.Session()
s.get("http://httpbin.org/cookies/set/number/123456")
response = s.get("http://httpbin.org/cookies")
print(response.text)
~~~

## 证书验证

现在的很多网站都是https的方式访问，所以这个时候就涉及到证书的问题

~~~python
import requests
from requests.packages import urllib3
urllib3.disable_warnings() # 消除警告信息
response = requests.get('https://www.12306.cn', verify=False)# 不需要证书
print(response.status_code)
~~~

当然也可以通过cert参数放入证书路径

~~~python
import requests

response = requests.get('https://www.12306.cn', cert=('/path/server.crt', '/path/key'))
print(response.status_code)
~~~

如果代理需要设置账户名和密码,只需要将字典更改为如下：

~~~python
proxies = {
"http":"http://user:password@127.0.0.1:9999"
}
~~~

## 代理设置

~~~python
import requests

proxies= {
    "http":"http://127.0.0.1:9999",
    "https":"http://127.0.0.1:8888"
}
response  = requests.get("https://www.baidu.com",proxies=proxies)
print(response.text)
~~~

如果代理需要设置账户名和密码,只需要将字典更改为如下：

~~~python
import requests

proxies = {
    "http": "http://user:password@127.0.0.1:9743/", # 传用户名，密码
}
response = requests.get("https://www.taobao.com", proxies=proxies)  
print(response.status_code)
~~~

如果你的代理是通过socks这种方式则需要`pip install "requests[socks]"`

~~~python
import requests

proxies = {
    'http': 'socks5://127.0.0.1:9742',
    'https': 'socks5://127.0.0.1:9742'
}
response = requests.get("https://www.taobao.com", proxies=proxies)
print(response.status_code)
~~~

## 超时设置

使用timeout参数设置超时的时间

~~~python
import requests
from requests.exceptions import ReadTimeout
try:
    response = requests.get("http://httpbin.org/get", timeout = 0.5)
    print(response.status_code)
except ReadTimeout:
    print('Timeout')
~~~

## 认证设置

通过auth来进行认证。（auth=HTTPBasicAuth('user', '123')写起来比较麻烦）

~~~python
import requests

r = requests.get('http://120.27.34.24:9001', auth=('user', '123'))
print(r.status_code)
~~~

## 异常处理

RequestException继承IOError,
HTTPError，ConnectionError,Timeout继承RequestionException
ProxyError，SSLError继承ConnectionError
ReadTimeout继承Timeout异常

~~~python
import requests
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
try:
    response = requests.get("http://httpbin.org/get", timeout = 0.5)
    print(response.status_code)
except ReadTimeout:
    print('Timeout')
except ConnectionError:
    print('Connection error')
except RequestException:
    print('Error')
~~~

关于reqeusts的异常在这里可以看到详细内容：<http://cn.python-requests.org/zh_CN/latest/_modules/requests/exceptions.html#RequestException>
所有的异常都是在requests.excepitons中。