#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-26 21:19:59
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import threading
import tool
import os

urls = {'http://02.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.ybmqrw.mod.rar':'', 'http://02.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar': ''}
cur_dir = os.getcwd()
if not os.path.exists('test'):
    os.mkdir('test')
threads = []
for url in urls:
    str = url.split('.')[-1]
    file_name = str[-3] + str[-2] + '.' + str[-1]
    path = f'{cur_dir}\\test\\{file_name}'
    urls[url] = path
    t = threading.Thread(target = tool.download, args = (url, path))
    threads.append(t)

for i in range(len(urls)):
    print(f'线程：{i}')
    threads[i].start()


