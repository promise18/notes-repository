# PyQuery

强大又灵活的网页解析库。如果你觉得正则写起来太麻烦，BeautifulSoup语法太难记，如果你熟悉jQuery的语法，那么PyQuery就是你的绝佳选择。

PyQuery 是 Python 仿照 jQuery 的严格实现。语法与 jQuery 几乎完全相同，所以不用再去费心去记一些奇怪的方法了。

*官网地址：http://pyquery.readthedocs.io/en/latest/*

官方文档：<http://pyquery.readthedocs.io/>

*jQuery参考文档：* http://jquery.cuishifeng.cn/

CSS选择器： <http://www.w3school.com.cn/css/index.asp>

## 初始化

初始化的时候一般有三种传入方式：传入字符串，传入url,传入文件

### 字符串初始化

~~~python
html = '''
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html) # doc即为pyquery对象
print(doc('li'))
~~~

结果：

```
<div>
    <ul>
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
<class 'pyquery.pyquery.PyQuery'>
<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
```

这里我们可以知道上述代码中的doc其实就是一个pyquery对象，我们可以通过doc可以进行元素的选择，其实这里就是一个css选择器，所以CSS选择器的规则都可以用。

直接doc(标签名)就可以获取所有的该标签的内容，

如果想要获取class 则doc('.classname'),如果是id则doc('#idname')。

### URL初始化

~~~python
from pyquery import PyQuery as pq
doc = pq(url='http://www.baidu.com')
print(doc('head'))
~~~

### 文件初始化

我们在pq()这里可以传入url参数也可以传入文件参数，当然这里的文件通常是一个html文件，例如：pq(filename='index.html')

~~~python
from pyquery import PyQuery as pq
doc = pq(filename='demo.html')
print(doc('li'))
~~~

## 基本CSS选择器

~~~python
html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
print(doc('#container .list li'))
~~~

结果：

```
<li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
```

这里我们需要注意的一个地方是doc('#container .list li')，这里的三者之间的并不是必须要挨着，只要是层级关系就可以,下面是常用的CSS选择器方法：

![img](D:\笔记\爬虫\2爬虫学习\06PyQuery.assets\997599-20170602224304383-1430515174.png)

## 查找元素

###  子元素

find（常用），children

~~~python
html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list') # 选中class为list的内容
print(type(items)) # <class 'pyquery.pyquery.PyQuery'>
print(items)
lis = items.find('li') # 选择item中所有li标签的内容
print(type(lis))
print(lis)
~~~

通过pyquery找到结果其实还是一个pyquery对象，可以继续查找。

上述代码中的items.find('li') 则表示查找ul里的所有的li标签。

当然这里通过children可以实现同样的效果,并且通过.children方法得到的结果也是一个pyquery对象，如：

~~~python
lis = items.children()
print(type(lis))
print(lis)
~~~

同时在children里也可以用CSS选择器

~~~python
lis = items.children('.active')
print(lis)
~~~

### 父标签

parent,parents

通过parent可以找到父元素的内容，例子如下：

~~~python
html = '''
<div id="container">
    <ul class="list">
         <li class="item-0">first item</li>
         <li class="item-1"><a href="link2.html">second item</a></li>
         <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
         <li class="item-1 active"><a href="link4.html">fourth item</a></li>
         <li class="item-0"><a href="link5.html">fifth item</a></li>
     </ul>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
container = items.parent() # 找父元素
print(type(container))
print(container)
~~~

通过parents方法可以找到祖先节点的内容，例子如下：

~~~python
from pyquery import PyQuery as pq
doc = pq(html)
items = doc('.list')
parents = items.parents() # 找祖先元素
print(type(parents)) 
print(parents)
~~~

结果：最前面的是祖先节点的信息，最后才是父节点的信息

```
<class 'pyquery.pyquery.PyQuery'>
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div><div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
```

同样我们通过parents查找的时候也可以添加css选择器来进行内容的筛选：

~~~python
parent = items.parents('.wrap')
print(parent)
~~~

### 兄弟元素

siblings

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')
print(li)
print(li.siblings())
~~~

代码中doc('.list .item-0.active') 中的.tem-0和.active是紧挨着的，所以表示的是并的关系，这样满足条件的就剩下一个了：third item的那个标签了。

它的兄弟元素即为其他四个。

同样我们通过.parents查找的时候也可以添加css选择器来进行内容的筛选

~~~python
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.list .item-0.active')
print(li.siblings('.active'))
~~~

## 遍历

### 单个元素

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
</div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
lis = doc('li').items()
print(type(lis))
for li in lis:
    print(li)
~~~

结果：

```
<class 'generator'>
<li class="item-0">first item</li>
             
<li class="item-1"><a href="link2.html">second item</a></li>
             
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-1 active"><a href="link4.html">fourth item</a></li>
             
<li class="item-0"><a href="link5.html">fifth item</a></li>
```

## 获取信息

pyquery对象.attr(属性名)
pyquery对象.attr.属性名

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a)
print(a.attr('href')) # 获取属性
print(a.attr.href) # 获取属性
~~~

结果：

~~~
<a href="link3.html"><span class="bold">third item</span></a>
link3.html
link3.html
~~~

### 获取文本

通过.text()获取文本

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
a = doc('.item-0.active a')
print(a)
print(a.text())
~~~

结果：

~~~
<a href="link3.html"><span class="bold">third item</span></a>
third item
~~~

### 获取HTML

我们通过.html()的方式可以获取当前标签所包含的html信息

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
print(li.html())
~~~

结果：

```
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<a href="link3.html"><span class="bold">third item</span></a>
```

## DOM操作

### addClass、removeClass

熟悉前端操作的话，通过这两个操作可以添加和删除属性

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.removeClass('active')
print(li)
li.addClass('active')
print(li)
~~~

### att、css

同样的我们可以通过attr给标签添加和修改属性，如果之前没有该属性则是添加，如果有则是修改。
我们也可以通过css添加一些css属性，这个时候，标签的属性里会多一个style属性

~~~python
html = '''
<div class="wrap">
    <div id="container">
        <ul class="list">
             <li class="item-0">first item</li>
             <li class="item-1"><a href="link2.html">second item</a></li>
             <li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             <li class="item-1 active"><a href="link4.html">fourth item</a></li>
             <li class="item-0"><a href="link5.html">fifth item</a></li>
         </ul>
     </div>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
li = doc('.item-0.active')
print(li)
li.attr('name', 'link')
print(li)
li.attr('name','a')
print(li)
li.css('font-size', '14px')
print(li)
~~~

结果

```
<li class="item-0 active"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0 active" name="link"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0 active" name="a"><a href="link3.html"><span class="bold">third item</span></a></li>
             
<li class="item-0 active" name="a" style="font-size: 14px"><a href="link3.html"><span class="bold">third item</span></a></li>
             
```

  ### remove

有时候我们获取文本信息的时候可能并列的会有一些其他标签干扰，这个时候通过remove就可以将无用的或者干扰的标签直接删除，从而方便操作

~~~python
html = '''
<div class="wrap">
    Hello, World
    <p>This is a paragraph.</p>
 </div>
'''
from pyquery import PyQuery as pq
doc = pq(html)
wrap = doc('.wrap')
print(wrap.text())
wrap.find('p').remove()
print(wrap.text())
~~~

其他DOM方法：<http://pyquery.readthedocs.io/en/latest/api.html>

