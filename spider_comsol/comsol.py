import requests
import re
import random
import time
import urllib


class VideoSpider:

    '''comsol学习视频爬虫'''

   def __init__(self):
        self.session = requests.Session()  # 下载器

    # 主逻辑
    def get_videos(self, url):
        # 获取视频播放地址
        video_urls = self.get_video_urls(url)
        print(video_urls)
        self.save_video_urls(video_urls)
        # self.download()
        # u = 'https://embedwistia-a.akamaihd.net/deliveries/d142d107901cc712757870a1c2fdc1985a520b67.bin'
        # r = self.get_html(u)
        # res = re.compile('(.*?).ts')
        # reg = re.findall(res, r)
        # print(reg)

    # 获取html3
    def get_html(self, url):
        user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:64.0) Gecko/20100101 Firefox/64.0',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 10.0; WOW64; Trident/7.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; InfoPath.3; Creative AutoUpdate v1.41.09)'
        ]
        headers = {"User-Agent": random.choice(user_agents)}
        try:
            res = requests.get(url, headers=headers)
            res.raise_for_status()
            time.sleep(random.random())
            res.encoding = res.apparent_encoding
            html = res.text
            # print(html)
            return html
        except:
            return '产生异常'

    # 获取网页中视频的访问地址
    def get_video_urls(self, comsol_url):
        # 访问COMSOL视频网站
        html = self.get_html(comsol_url)
        # print(html)
        # re解析html
        res = re.compile('<li><a href="/video/(.*?)">(.*?)</a></li>')
        video_urls = re.findall(res, html)
        # print(video_urls)
        return video_urls
        # print(url_reg)

    def save_video_urls(self, video_urls):
        # 保存视频链接地址
        for video_url in video_urls:
            url = f'http://cn.comsol.com/video/{video_url[0]}'
            title = video_url[1]
            # print(video_title)
            # print(video_url)
            with open('url.csv', 'a+') as fp:
                # fp.write(title + '：\t' + url + '\n')
                fp.write(f'{title} ：\t{url}\n')

    # 下载视频
    def download(self):
        url = 'https://embedwistia-a.akamaihd.net/deliveries/d142d107901cc712757870a1c2fdc1985a520b67.bin'
        urllib.request.urlretrieve(url, 'test.bin')


if __name__ == '__main__':
    demo = VideoSpider()
    comsol_url = 'http://cn.comsol.com/video/introduction-to-tutorial-videos-cn?utm_source=WechatFollowers&utm_campaign=cn_wechat_Q1_2018&utm_medium=Demail&utm_content=29'
    demo.get_videos(comsol_url)
