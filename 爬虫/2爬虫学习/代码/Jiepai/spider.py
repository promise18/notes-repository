import requests
from urllib.parse import urlencode
from hashlib import md5
import json
import re
import pymongo
from json.decoder import JSONDecodeError
from bs4 import BeautifulSoup
from config import *
import requests.exceptions
import os
from multiprocessing import Pool


headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
    "cookie":"tt_webid=6700384666501514764; WEATHER_CITY=%E5%8C%97%E4%BA%AC; tt_webid=6700384666501514764; UM_distinctid=16b3a846cbd726-0d1ded79290cb4-e353165-100200-16b3a846cbe17d; csrftoken=7dd3005a6428fd706d60b50612eb2231; s_v_web_id=8d604541c7793f6170b315b76f655633; __tasessionId=y53ru6gv61562652546470; CNZZDATA1259612802=1145303510-1560054529-https%253A%252F%252Fwww.baidu.com%252F%7C1562651743",
}

client = pymongo.MongoClient(MONGO_URL,connect=False)
db = client[MONGO_DB]


def get_page_index(keyword):
    data = {
        'aid': '24',
        'app_name': 'web_search',
        'offset': '20',
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'en_qc': 1,
        'cur_tab': 1,
        'pd': 'synthesis',
    }
    params = urlencode(data)
    base = 'https://www.toutiao.com/api/search/content/'
    url = base + '?' + params
    print("准备获取url")
    print(url)
    try:
        response = requests.get(url, headers=headers)
        response.encoding='utf-8'
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        print('连接失败')
        return None

def parse_page_index(text):
    data = json.loads(text)
    try:
        if data and "data" in data.keys():  # 如果获取到了data，且获取的data中的有'data'这个键名
            for item in data.get('data'):
                yield item.get('article_url')
        else:
            print("没有获取data")
    except JSONDecodeError:
        pass

def get_page_detail(url):
    try:
        if(url == None):
            pass
        else:
            response = requests.get(url,headers= headers)
            if response.status_code == 200:
                return response.text
    except ConnectionError:
        print("连接错误")
        return None

def parse_page_detail(text,url):
    soup = BeautifulSoup(text,'lxml')
    title = soup.select('title')[0].get_text()
    # print(title)
    images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
    #images_pattern = re.compile('var gallery = (.*?);', re.S)
    result = re.search(images_pattern,text)
    if result:
        data = json.loads(result.group(1).replace('\\',''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'url': url,
                'images': images
            }


def save_to_mongo(result):
    if result == None:
        pass
    elif db[MONGO_TABLE].insert(result):
        print('存储到数据库成功',result)
        return True
    return False


def download_image(url):
    try:
        if(url == None):
            pass
        else:
            print('正在下载',url)
            response = requests.get(url,headers= headers)
            if response.status_code == 200:
                save_image(response.content)
    except:
        print("请求图片出错")
        return None


def save_image(content):
    # os.getcwd():当前项目路径，md5(content).hexdigest()：存文件名
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main():
    text = get_page_index(KEYWORD)
    for url in parse_page_index(text):
        text = get_page_detail(url)
        if text:
            result = parse_page_detail(text,url)
            save_to_mongo(result)


if __name__ == '__main__':
    main()
    # pool = Pool()
    # groups = ([x * 20 for x in range(GROUP_START, GROUP_END + 1)])
    # pool.map(main, groups)
    # pool.close()
    # pool.join()
