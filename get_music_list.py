import requests
from bs4 import BeautifulSoup
import re
import json
import os

def get_list_url():
    url = input("请输入酷狗分享链接：")
    try:
        res = requests.get(url)
        res.raise_for_status()
        res.encoding = res.apparent_encoding
        html = res.text
        # print(html)
    except:
        print("访问错误")
    r = re.compile('<script >\n        var dataFromSmarty = (.*?),//当前页面歌曲信息.*?</script>', re.S)
    reg = re.findall(r, html)
    r_dict = json.loads(reg[0])
    music_name = set()
    for i in r_dict:
        music_name.add(i["song_name"])
    return music_name

def get_local_list():
    music_path = r'F:\备份\手机备份\Music'
    files = os.listdir(music_path)
    local_list = set()
    for f in files:
        portion = os.path.splitext(f)
        if portion[-1] in ['.mp3', '.flac']:
            local_list.add(portion[0])

    return local_list

if __name__ == '__main__':
    music_list = get_list_url()
    local_list = get_local_list()
    exist_music = set()
    # print(local_list)
    flag = 0
    for i in local_list:
        tmp = i.split(' - ')
        # print(tmp[-1])
        if tmp[0] in music_list:
            exist_music.add(tmp[0])
            flag += 1
        if tmp[-1] in music_list:
            exist_music.add(tmp[-1])
            flag += 1
    diff_set = music_list - exist_music
    with open('diff_list.txt', 'w') as fp:
        fp.close()

    for i in diff_set:
        with open('diff_list.txt', 'a', encoding='utf-8') as fp:
            fp.write(i)
            fp.write('\n')
            fp.close()