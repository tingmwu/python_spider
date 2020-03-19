import os
import sys
import shutil


def cmp_music():
    ''' 主逻辑 '''
    origin_path = r"F:\备份\手机备份\Music"
    diff_path = r"E:\Users\TM\Desktop\test"
    origin_list = get_music_list(origin_path)
    diff_list = get_music_list(diff_path)
    move_music(origin_list, diff_list, origin_path, diff_path)


def get_music_list(music_path):
    ''' 获取歌曲列表 '''

    music_inf = []
    files = os.listdir(music_path)
    for file in files:
        partition = os.path.splitext(file)
        if partition[-1] in ['.mp3', '.flac']:
            music_dict = {}
            music_dict['music'] = file
            music_dict['title'] = partition[0].split(' - ')[0]
            music_dict['name'] = partition[0].split(' - ')[-1]
            music_inf.append(music_dict)
    # print(music_inf)
    return music_inf


def move_music(origin_list, diff_list, origin_path, diff_path):
    num = 0
    total_size = 0
    for i in diff_list:
        if not cmp(origin_list, i):
            src_path = diff_path + "\\" + i['music']
            total_size += get_FileSize(src_path)
            num += 1
            print('正在复制: {} - {}'.format(i['title'], i['name']))
            # shutil.copy(src_path, origin_path)
    print("一共复制{}首歌".format(num))
    print("共计: {:.2f} MB".format(total_size))


def cmp(origin_list, diff_music):
    flag = False
    for i in origin_list:
        if diff_music['title'] == i['title']:
            flag = True
    return flag


def get_FileSize(file_path):
   fsize = os.path.getsize(file_path)
   fsize = fsize / float(1024 * 1024) 
   return round(fsize, 2)


if __name__ == "__main__":

    cmp_music()
