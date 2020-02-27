# !/usr/bin/env python
# -*- coding:utf-8 -*-
# author:心蓝
# 全书网 小说爬虫
import requests
import re  # 内库，标准库


class NovelSpider:
    """全书网，小说爬虫"""

    def __init__(self):
        self.session = requests.Session()  # 下载器

    def get_novel(self, url):  # 主逻辑
        """下载小说"""
        # 下载小说的首页面 html
        index_html = self.download(url, encoding='gbk')
        # 小说的 标题
        title = re.findall(r'"article_title">(.*?)<', index_html)[0]
        # 提取章节信息，url 网址
        novel_chapter_infos = self.get_chapter_info(index_html)
        # 创建一个 文件 小说名.txt
        fb = open('%s.txt' % title, 'w')
        # 下载章节信息 循环
        for chapter_info in novel_chapter_infos:
            # 写章节 标题
            fb.write('%s\n' % chapter_info[1])
            # 下载 章节
            content = self.get_chapter_content(chapter_info[0])
            # 写章节 内容
            fb.write(content)
            fb.write('\n')
            print(chapter_info)
        fb.close()

    def download(self, url, encoding):
        """下载 页面信息 html源码"""
        response = self.session.get(url)
        response.encoding = encoding
        html = response.text
        return html

    def get_chapter_info(self, index_html):
        """ 提取，章节信息 """
        div = re.findall(
            r'<DIV class="clearfix dirconone">.*?</DIV>', index_html, re.S)[0]
        info = re.findall(
            r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>', div)
        return info

    def get_chapter_content(self, chapter_url):
        """下载 章节的内容"""
        chapter_html = self.download(chapter_url, encoding='gbk')
        content = re.findall(
            r'<script type="text/javascript">style5\(\);</script>(.*?)<script', chapter_html, re.S)[0]
        # 清洗 数据
        content = content.replace('&nbsp;', '')
        content = content.replace('<br />', '')
        # 替换换行
        content = content.replace('\r\n', '')
        return content


if __name__ == '__main__':

    novel_url = 'http://www.quanshuwang.com/book/0/551'
    spider = NovelSpider()  # 实例化
    spider.get_novel(novel_url)
