import requests
import threading
from time import time
import json
import re


def downloadFile(URL, spos, epos, fp):
    try:
        header = {}
        header["Range"] = "bytes={}-{}".format(spos, epos)
        result = requests.get(URL, headers=header)
        fp.seek(spos)
        fp.write(result.content)
    except Exception:
        print(Exception)


def split_file(file_size):
    start_p = []
    end_p = []
    per_size = int(file_size / thread_num)
    int_size = per_size * thread_num  # 整除部分
    for i in range(0, int_size, per_size):
        start_p.append(i)
        end_p.append(i + per_size - 1)
    if int_size < file_size:  # size 不一定 n 等分，将不能等分余下的部分添加到最后一个 sub 里
        end_p[-1] = file_size
    return start_p, end_p


# 线程数量
thread_num = 30

# 需要填写的变量
url = 'https://qdall01.baidupcs.com/file/634d244eab8ee1a892ab715b9fd2c9d9?bkt' \
      '=p3-000009c8ff35f1592413eb92e4711ebcea06&fid=1875498710-250528-704979486370452&time=1547291838&sign=FDTAXGERLQBHSKfWa-DCb740ccc5511e5e8fedcff06b081203-qdwKO%2BSWaZcG73hInc2ojVOoXyY%3D&to=92&size=216018659&sta_dx=216018659&sta_cs=41576&sta_ft=zip&sta_ct=7&sta_mt=5&fm2=MH%2CYangquan%2CAnywhere%2C%2Chubei%2Cce&ctime=1489065890&mtime=1537519965&resv0=cdnback&resv1=0&vuk=1875498710&iv=-2&htype=&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=000009c8ff35f1592413eb92e4711ebcea06&sl=82640974&expires=8h&rt=sh&r=898154687&mlogid=273681965881112675&vbdid=1419757194&fin=FLCS6%EF%BC%8832%2664%EF%BC%89.zip&fn=FLCS6%EF%BC%8832%2664%EF%BC%89.zip&rtype=1&dp-logid=273681965881112675&dp-callid=0.1.1&hps=1&tsl=50&csl=78&csign=spg%2F5XPS2eYR7yeTIYLofAw%2FzHs%3D&so=0&ut=8&uter=4&serv=0&uc=2252599700&ti=8525e99dbc6685b1a4be18ba51c0b10008029b3521936ae7&by=themis'
down_file_name = 'Your file name'
# 如果该变量不填就会下载到运行程序的目录下
address = 'D:/'  # 记得最后要加斜杠

file = open(address + down_file_name, 'wb')
res = requests.head(url)
# 若有单引号替换成双引号
json_data = re.sub('\'', '\"', str(res.headers))
head_dict = json.loads(json_data)
size = int(head_dict['Content-Length'])
start_pos, end_pos = split_file(size)

tmp = []
print('start download...')
t0 = time()
for i in range(0, thread_num):
    t = threading.Thread(
        target=downloadFile,
        args=(
            url,
            start_pos[i],
            end_pos[i],
            file))
    t.setDaemon(True)  # 主进程结束时，线程也随之结束
    t.start()
    tmp.append(t)
for i in tmp:
    i.join()

file.close()
t1 = time()
total_time = t1 - t0
speed = float(size) / (1000 * total_time)
print('total_time:%.2f s' % total_time)
print('speed:%.2f KB/s' % speed)