#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-26 15:51:39
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import requests
from bs4 import BeautifulSoup
import re
import random
import urllib
import os
import download


def get_html(url):
    r = requests.get(url)
    # print(r.status_code)
    html = r.text
    # print(html)
    return html

def bsoup(html):
    # BeautifulSoup 方法
    soup = BeautifulSoup(html, 'html.parser')
    tag = soup.find_all('a')
    return tag

def get_mood_menu_urls(html):
    # 正则方法
    res = re.compile('<a href="(.*?)" target="_blank" title="饥荒(.*?)">.*?MOD</a>')
    reg = re.findall(res, html)
    urls = reg
    return urls

def get_download_url(html):
    res = "<li><a href='(.*?)' target='_blank' ><em></em>电信.*?服务器</a></li>"
    reg = re.findall(res, html)
    download_url = random.choice(reg)
    # print(url)
    return download_url

def download(download_url, path):
    urllib.request.urlretrieve(download_url, path)


def get_mood(url):
    # 主逻辑
    # print('hello')
    main_html = get_html(url)
    # print(main_html)
    mood_menu_urls = get_mood_menu_urls(main_html)
    for i in mood_menu_urls:
        title = i[1]
        url = i[0]
        # print(title)
        # print(url)
        downdemo_html = get_html(url)
        download_url = get_download_url(downdemo_html)

        cur_dir = os.getcwd()
        if not os.path.exists('mood'):
            os.mkdir('mood')
        file_type = url.split('.')[-1]
        path = f'{cur_dir}\\mood\\{title}.{file_type}'
        if os.path.isfile(path):
            print(f'已存在{title}')
        else:
            print(f'正在下载{title}')
            # download(download_url, path)
            download.download(download_url, path)
            print(f'已下载{title}')
    print("已完成下载")


    # str = 'document.writeln("<li><a href='http://02.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar' target='_blank' ><em></em>电信01服务器</a></li><li><a href='http://03.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar' target='_blank' ><em></em>电信02服务器</a></li><li><a href='http://04.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar' target='_blank' ><em></em>电信03服务器</a></li><li><a href='http://05.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar' target='_blank' ><em></em>电信04服务器</a></li><li><a href='http://06.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar' target='_blank' ><em></em>电信05服务器</a></li><li><a href='http://07.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar' target='_blank' ><em></em>电信06服务器</a></li>")'
    # res = "<li><a href='(.*?)' target='_blank' ><em></em>电信.*?服务器</a></li>"
    # # print(title)


if __name__ == '__main__':
    url = 'http://www.yxdown.com/zt/jhmod/?baidutj'
    get_mood(url)
