import requests
import re
import os
import urllib
import time


def time_deco(func):

    '''装饰器 计算运行时间'''

    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        msec = end_time - start_time
        print('time is %.1f' % msec)
    return wrapper


class MoodSpider:

    '''爬取饥荒mood并下载'''

    def __init__(self):
        self.session = requests.Session()  # 下载器

    @time_deco
    def get_mood(self, url):  # 主逻辑
        html = self.get_html(url)
        # print(html)
        print('获取主页面成功!')
        mood_menu_urls = self.get_mood_urls(html)
        print('解析主页面成功!')
        # print(mood_menu_urls)
        # 逐个解析下载mood
        cur_dir = os.getcwd()
        if not os.path.exists('mood'):
            os.mkdir('mood')
        for mood_url in mood_menu_urls:
            url = mood_url[0]
            title = mood_url[1]
            # 获取mood的html
            mood_html = self.get_html(url)
            # 解析mood的html 获取mood下载界面的url
            downloaddemo_url = self.get_downloaddemo_url(mood_html)
            # print(downloaddemo_url)
            # 获取mood下载界面的html
            downloaddemo_html = self.get_html(downloaddemo_url[0])
            # print(downloaddemo_html)
            # 解析mood下载界面的html 获取mood下载的url
            download_url = self.get_download_url(downloaddemo_html)
            # print(download_url)

            # 下载mood
            cur_dir = os.getcwd()
            path = r'%s\mood\%s.zip' % (cur_dir, title)
            self.download(download_url, path)
            print(f'已下载{title}！')
            # self.downloaddemo_url

    # 获取 网页html
    def get_html(self, url):
        try:
            r = requests.get(url)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            # print(r.text)
            html = r.text
        except:
            print('访问失败')
        return html

    # 解析网页 获取每个mood的url 并存储到txt文件中
    def get_mood_urls(self, html):
        # res = re.compile('<li><a href=(.*?)>(.*?)</a></li>')
        res = re.compile("<li><a href='(.*?)'>(.*?)</a></li>")
        reg = re.findall(res, html)
        # print()
        if os.path.isfile('mood_menu.txt'):
            if os.path.getsize('mood_menu.txt') != 0:
                os.remove('mood_menu.txt')
        for url in reg:
            mood_url = url[0]
            mood_title = url[1]

            with open('mood_menu.txt', 'a+') as f:
                f.writelines(mood_title + '\t')
                f.writelines(mood_url + '\n')
                # print(mood_title)
                # print(mood_url)
        return reg

    # 解析每个mood_url 获取下载界面链接
    def get_downloaddemo_url(self, mood_html):
        res = re.compile(
            '下载地址：<a class="n1" target="_blank" href="(.*?)">点击进入</a></p>')
        reg = re.findall(res, mood_html)
        # print(reg)

        return reg

    # 解析每个mood下载界面html 获取mood下载链接
    def get_download_url(self, mood_downloaddemo_html):
        res = re.compile(
            '<a class="down2  FTP countHit" data-itemid=".*?" data-hot="true" href="(.*?)" itemprop="downloadUrl" target="_blank">FTP下载</a>')
        reg = re.findall(res, mood_downloaddemo_html)
        download_url = reg[0].replace('amp;', '')

        return download_url

    # 下载mood
    def download(self, url, path):
        if not os.path.isfile(path):
            urllib.request.urlretrieve(url, path)
        else:
            print(f"已存在{path}")
        # html = demo1.MoodSpider.get_html(url)

    def my_read_txt(txtpath, lab='\t'):
        ''' 读取txt文件 保存到多维列表'''
        str = []
        with open(txtpath, 'r') as fp:

            for line in fp.readlines():
                curline = line.strip().split(lab)
                # col = len(line)
                # print(curline)
                str.append(curline)
                # print(str)
                # for index in range(col):
                #   str[index].append(curline[index])
            return str




if __name__ == '__main__':
    demo = MoodSpider()
    demo.get_mood('https://www.gamersky.com/handbook/201702/871463_6.shtml')
