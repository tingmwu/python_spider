import re   # 内置模块 正则表达式
import requests     #

# def get_novel_content():

# url
novel_url = 'http://www.quanshuwang.com/book/47/47863'

# 访问url
novel_data = requests.get(novel_url).content.decode('gbk')
# novel_data = requests.get()
# novel_data = novel_data.decode('gbk')

# print(novel_data)
# 3.正则表达式解析网页
res = re.compile('<li><a href="(.*?)" title="第.*?章.*?">(.*?)</a></li>')  # 符合正则表达式返回到列表
# res = '<li><a href="(.*?)" title=".*?">(.*?)</a></li>'  # 符合正则表达式返回到列表
urls = re.findall(res, novel_data)
title_res = re.compile('content="如你喜欢小说(.*?)，那么请将')
novel_title = re.findall(title_res, novel_data)

# print(urls)

for url in urls:
    # print(url)
    # print(len(url))
    # print(url[0])
    chapt_url = url[0]
    chapt_title = url[1]
    # print(chapt_url)
    # print(chapt_title)
    chapt_html_content = requests.get(chapt_url).content.decode('gbk', 'ignore')
    # print(chapt_htmlcontent)
    chapt_reg = re.compile(r'</script>&nbsp;&nbsp;&nbsp;&nbsp;(.*?)'
                           r'<script type="text/javascript">', re.S)
    chapt_content = re.findall(chapt_reg, chapt_html_content)
    # print(chapt_content)
    # print(type(chapt_content))

    # print(type(str(chapt_content[0])))
    # print(chapt_content[1])
    chapt_content = str(chapt_content[0])
    chapt_content = chapt_content.replace('<br />', '')
    chapt_content = chapt_content.replace('&nbsp;', '')
    # print(chapt_content)

    # 下载
    print('正在下载 %s'%chapt_title)
    # with open('{}.txt'.format(chapt_title), 'w') as f:
    with open('{}.txt'.format(novel_title[0]), 'a') as f:
        f.write(chapt_content+'\n')

# if __name__ == '__main__':
#     get_novel_content()
