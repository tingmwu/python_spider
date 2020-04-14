import requests
import json
import re
import os


```
获取GBT小组游戏空间(http: // renxufeng.ys168.com /)的所有游戏种子
```

menu_url = "http://cd.ys168.com/f_ht/ajcx/ml.aspx?cz=ml_dq&_dlmc=renxufeng&_dlmm="

menu = requests.get(menu_url).text
# print(menu)
r = re.compile('<li id="ml_(.*?)" .*?</li>')
menu_id = re.findall(r, menu)

for i in menu_id:
    detial_url = "http://cd.ys168.com/f_ht/ajcx/wj.aspx?cz=dq&mlbh={}&_dlmc=renxufeng&_dlmm=".format(
        i)
    detail_menu = requests.get(detial_url).text
    # print(detail_menu)
    r = re.compile('<li .*? href="(.*?)".*?</li>')
    detail = re.findall(r, detail_menu)
    if not os.path.isfile('game.txt'):
        with open('game.txt', 'w') as fp:
            fp.close()
    for i in detail:
        with open('game.txt', 'a') as fp:
            fp.write(i)
            fp.write('\n')
            fp.close()
