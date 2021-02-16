import webbrowser

from pykeyboard.mac import PyKeyboard

import code_list
import time
import random
from selenium import webdriver
import os

# 同花顺财报下载器

f = []
g = {}

# zcfz = '/Users/zhangmin/Documents/data_shares/同花顺资产负债表'
# xjll = '/Users/zhangmin/Documents/data_shares/同花顺现金流量表'
lrb = '/Users/zhangmin/Documents/data_shares/同花顺利润表'

for root, dirs, files in os.walk(lrb):
    # 当前目录路径
    # print(root)
    # 当前路径下所有子目录
    # print(dirs)
    # 当前路径下所有非目录子文件
    # print(files)
    f = files

for t in f:
    g[t.split('_', 1)[0]] = t

print(len(g))
# url_p1 = 'http://basic.10jqka.com.cn/api/stock/export.php?export=debt&type=report&code='
# url_p1 = 'http://basic.10jqka.com.cn/api/stock/export.php?export=cash&type=report&code='
url_p1 = 'http://basic.10jqka.com.cn/api/stock/export.php?export=benefit&type=report&code='
# url_p2 = '&userid=177763131&cache=a3aa4c400773b0e8ce899590065689d8'

code_list = code_list.code_list
code_list_len = len(code_list)
code_list_len_done = len(g)
k = PyKeyboard()

for key in code_list:
    # os.system('killall Safari')
    code = key
    name = code_list[key]
    url = url_p1 + code  # + url_p2

    # if code[0:1] not in ['0', '6']:
    #     continue
    if g.get(code, None) is None:
        webbrowser.open(url)
        print(code + '_' + code_list[key])
        code_list_len_done += 1
        print('已完成：' + str(code_list_len_done) + '/' + str(code_list_len))
        second = int(random.uniform(4, 6))
        print('等待：' + str(second) + '秒')
        time.sleep(second)  # 随机等待2～5秒

        k.press_key('Command')  # –按住alt键
        time.sleep(1)
        k.tap_key('w')  # –点击tab键
        # time.sleep(1)
        k.release_key('Command')  # –松开alt键
        # time.sleep(1)

        # k.press_key('Command')  # –按住alt键
        # time.sleep(1)
        # k.tap_key('w')  # –点击tab键
        # time.sleep(1)
        # k.release_key('Command')  # –松开alt键
        # time.sleep(1)

        second = int(random.uniform(6, 7))
        print('等待：' + str(second) + '秒')
        time.sleep(second)  # 随机等待2～5秒
