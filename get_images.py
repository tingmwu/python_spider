from bs4 import BeautifulSoup
import requests
import urllib.request
import re
import os
import time
import random
from fake_useragent import UserAgent


class SpiderImages:
    # 装饰器 获取函数运行时间
    def deco(func):
        def wrapper(*args, **kwargs):
            star_time = time.time()
            func(*args, **kwargs)
            end_time = time.time()
            msecs = (end_time - star_time)
            print('time is %d ms' % msecs)

        return wrapper
    ''' 获取网站中图片并下载 '''
    # 主逻辑
    @deco
    def get_images(self, main_url, page_n):
        # 获取主页html
        main_html = self.download_html(main_url)
        # print(main_html)

        # 解析出主页中所包含的图片集链接地址
        chapt_urls = self.get_chapt_urls(main_html)
        # print(chapt_urls)

        # 遍历章节链接
        for chapt_url in chapt_urls:
            url = chapt_url[0]
            title = chapt_url[1]
            title = re.sub('[\/:*?"<>|]', '_', title)    # 将title中的违反命名规范的符号替换
            if os.path.exists('images\%s'%title):
                print('跳过%s'%title)
                continue
            # 获取每一个章节链接的html
            html = self.download_html(url)

            # 提取图片链接
            image_urls = self.get_image_url1(html)

            # 下载图片到指定新建文件夹
            os.mkdir(r'images\%s' % title)
            self.download_image(image_urls, title, page_n)

        # html = self.download_html(url)
        # # print(html)
        # urls = self.get_image_url1(html)
        # # print(type(urls))
        # self.download_image(urls)

    # 解析主页html 获取每一个部分的url
    def get_chapt_urls(self, main_html):
        # print(main_html)
        res = re.compile('a href="(.*?).html" class="card-img-hover" '
                         'title="(.*?)"', re.M)
        reg = re.findall(res, main_html)
        # print(reg[0])

        return reg

    # 访问并下载下载html源码
    def download_html(self, url):
        user_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
                       'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; Creative AutoUpdate v1.41.09)'
                       ]
        # user_agents = UserAgent()
        headers = {"User-Agent": random.choice(user_agents)}
        # headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        res = requests.get(url, headers=headers)
        time.sleep(random.random())
        html = res.text
        return html

    # 解析出图片地址 正则表达式方法
    def get_image_url1(self, html):
        res = re.compile('img src="(.*?).jpg"')
        reg = re.findall(res, html)

        return reg

    # 解析图片地址  beautifulsoup对象方法
    def get_image_url2(self, html):
        # 创建beautifulsoup对象 解析网页
        soup = BeautifulSoup(html, 'html.parser')
        # print(type(soup))
        imags = soup.find_all('img')
        return soup

    # 下载图片
    def download_image(self, urls, path='test', page_n=1):
        count = 0
        for url in urls:
            # url = url.find('img src=')
            # print(url)
            count += 1
            print('正在下载第%s页中%s中第%s张图片' % (page_n, path, count))

            urllib.request.urlretrieve(url, 'images\%s\%s.jpg' % (path, count))
            time.sleep(random.random())  # 暂停0.ji秒，时间区间：[0,1]


    def next_page(self, first_page_url, page):
        # main_html = self.download_html(first_page_url)
        page_str = '?p=%s#tab_anchor'%page
        page_url = first_page_url + page_str
        return page_url







if __name__ == '__main__':
    # main_url = 'https://www.zcool.com.cn/'
    page_random = range(1, 10)
    main_url = 'https://www.zcool.com.cn/'
    for page_n in page_random:
        demo = SpiderImages()
        page_url = demo.next_page(main_url, page_n)
        demo.get_images(page_url, page_n)
        print('第%s页图片下载完毕' % page_n)
    print('图片下载完毕')
