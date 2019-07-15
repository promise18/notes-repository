import requests
import re
# content = requests.get('https://book.douban.com/').text
# pattern = re.compile('<li.*?cover>')
import requests
import re
content = requests.get('https://book.douban.com/').text
pattern = re.compile('<li.*?cover.*?href="(.*?)".*?title="(.*?")".*?more-meta.*?author">(.*?)</span>.*?year">(.*?)</span>.*?</li>', re.S)
results = re.findall(pattern, content)
print(results)
