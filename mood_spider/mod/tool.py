#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-01-26 18:51:31
# @Author  : Your Name (you@example.org)
# @Link    : http://example.org
# @Version : $Id$

import sys
import requests
import os

# 屏蔽warning信息，因为下面verify=False会报警告信息
# requests.packages.urllib3.disable_warnings()


def signal_download(url, path):

    try:
        r = requests.get(url, stream=True)
        r.raise_for_status()
    except:
        print('访问出错')
        return 0

    total_size = int(r.headers['Content-Length'])
    temp_size = 0

    # 输出文件大小 换算成MB
    print('[文件大小]:%0.2f MB' % (total_size / 1024 / 1024))

    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                # f.flush()
                done = int(temp_size * 40 / total_size)
                demo_display = '[' + '█' * done + '  '*(40 - done) + ']'
                num_display = float(temp_size / total_size * 100)
                # print('[下载进度]:%s%.2f%%' % (demo_display, num_display), end='\r')
                print('[下载进度]:%.2f%%' % (num_display), end='\r')

                # done = int(50 * temp_size / total_size)

                # sys.stdout.write()
        print('\n')

if __name__ == '__main__':
    url='http://02.bd-pcgame.720582.com:8090//2016/Mod/Dont.Starve.59.rwpf.zhb.mod.rar'
    signal_download(url, path='test.rar')
