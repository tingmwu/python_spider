"""
              ┏┓      ┏┓
            ┏┛┻━━━┛┻┓
            ┃      ☃      ┃
            ┃  ┳┛  ┗┳  ┃
            ┃      ┻      ┃
            ┗━┓      ┏━┛
                ┃      ┗━━━┓
                ┃  神兽保佑    ┣┓
                ┃　永无BUG！   ┏┛
                ┗┓┓┏━┳┓┏┛
                  ┃┫┫  ┃┫┫
                  ┗┻┛  ┗┻┛
"""
import threading
import time
import os
import requests


def cal_time(func):
    '''装饰器 计算运行时间'''

    def wrapper(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        msec = end_time - start_time

        print('time is %.4f' % msec)
    return wrapper


class Download:
    '''单线程和多线程下载'''

    def __init__(self):
        self.LOCK = threading.Lock()


    @cal_time
    def single_download(self, url, path):
        '''下载文件 单文件直接下载'''

        try:
            r = requests.get(url)
            r.raise_for_status()
            # r.encoding = r.apparent_encoding
        except:
            print(f'访问失败\n链接：{url}')
            return 0

        # 建立并清空文件内容
        with open(path, 'wb') as f:
            f.close()

        # 下载文件
        with open(path, 'ab') as f:
            f.write(r.content)

        print('%s 下载完成' % path)

    @cal_time
    def handler(self, start, end, url, filename):
        self.LOCK.acquire()

        headers = {'Range': 'bytes=%d-%d' % (start, end)}
        r = requests.get(url, headers=headers, stream=True)

        # 写入文件对应位置
        with open(filename, "ab") as fp:
            fp.seek(start) # 设置文件指针位置
            # var = fp.tell() # 查看当前指针位置
            fp.write(r.content)

        print(threading.current_thread().name)
        # print(time.time() - time0)  # + threading.current_thread().name)

        self.LOCK.release()

    @cal_time
    def threads_download(self, url, path, thread_num=2):
        '''下载文件 单个文件多线程下载'''

        # 建立并清空文件内容
        with open(path, 'wb') as f:
            f.close()

        total_size = int(requests.head(url).headers['Content-Length'])
        step = total_size // thread_num
        threads = []
        # tmp = []

        #  创建一个和要下载文件一样大小的文件
        # fp = open(path, "wb")
        # fp.truncate(total_size)
        # fp.close()

        # 创建线程
        for i in range(thread_num):
            start = step * i
            if i == thread_num - 1:
                end = total_size
            else:
                end = start + step
            t = threading.Thread(target=self.handler,
                                 args=(start, end, url, path))
            threads.append(t)

        # 开始线程
        for t in threads:
            # t.setDaemon(True)  # 主进程2结束时，线程也随之结束
            t.start()
            # tmp.append(t)
        t.join()

        # # 等待所有线程下载完成
        # main_thread = threading.current_thread()
        # for t in threading.enumerate():
        #     if t is main_thread:
        #         continue
        #     t.join()
        print('%s 下载完成' % path)

    @cal_time
    def block_download(self, list):
        '''多文件串行下载'''
        for (url, path) in list.items():
            self.single_download(url, path)

    @cal_time
    def file_thread(self, list):
        '''
        多文件 多线程下载
        list格式为{url：path}形式的字典
        '''
        if not os.path.exists('download'):
            os.mkdir('download')
        # file_type = url.split('.')[-1]
        # file_path = f'{os.getcwd()}\\download\\{title}.{file_type}'
        # 创建线程池
        threads = [threading.Thread(target=self.single_download, args=(url, path))
                   for (url, path) in list.items()]

        for i in threads:
            i.start()
        i.join()


def get_ftype(url):
    h = requests.head(url).headers
    file_type = h['Content-Type'].split('/')[-1]

    return file_type


if __name__ == '__main__':
    # test_list = {'https://img.zcool.cn/community/031c7925566c7ad000001cc298dd45d.jpg@260w_195h_1c_1e_1o_100sh.jpg': 'test\\1.jpg',
    #              'https://img.zcool.cn/community/01bf1e5c4c7577a801203d22c30cdc.jpg@260w_195h_1c_1e_1o_100sh.jpg': 'test\\2.jpg'}
    # if not os.path.isdir('test'):
    #     os.mkdir('test')
    # block_download(test_list)
    url = 'https://img.zcool.cn/community/01986f5c52895da801213f26707474.jpg@1280w_1l_2o_100sh.jpg'
    path = 'test\\d_test.%s' % get_ftype(url)
    d = Download()

    d.threads_download(url, path, thread_num=8)
    # d.single_download(url, path)
