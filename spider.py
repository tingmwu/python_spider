import re   # 内置模块 正则表达式
import requests     #

# 1.url
url = 'http://c.tieba.baidu.com/p/3545864332'

# 2.模拟浏览器请求资源
wb_data = requests.get(url).text
# print(wb_data)

# 3.正则表达式解析网页
res = re.compile(r'src="(.+?.jpg)"')    # 符合正则表达式返回到列表
reg = re.findall(res, wb_data)
print(reg)

# 4.保存到本地
num = 0
for i in reg:
    # print(i)

    a = requests.get(i)
    f = open(r'E:\py\pachong\fox\%s.jpg' % num, 'wb')  # 以二进制写入
    f.write(a.content)
    f.close()
    num += 1
    print('第%s张下载完毕' % num)


{
    'types': 'search',
    'count': '10',
    'source': 'kugou',
    'pages': '1',
    'name': '告白气球',
    'cache': '9a94264bceaad353ef72684c2f01bb76'
}

{'types': 'search',
'count': '20',
'source': 'kugou',
'pages': '1',
'name': '告白气球'}

{
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Host': 'v1.itooi.cn',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
    'Upgrade-Insecure-Requests': '1'
}
