import json
import re
import requests
import code_list
import pymongo
from bs4 import BeautifulSoup
import pandas as pd

HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',  # 'close', #'keep-alive',
    # 'Cookie': cookie,
    # 'Host': 'basic.10jqka.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}

my_client = pymongo.MongoClient('localhost:27017')
d_shares = my_client['d_shares']
c_north_cash_flow = d_shares['c_north_cash_flow']

db_list = my_client.list_database_names()
print(db_list)

code_list = code_list.code_list
url_path1 = 'http://www.gzyuwan.com/echarts.php?code='

for key in code_list:
    if key[0:2] not in ['60', '00']:
        continue
    # os.system('killall Safari')
    code = key
    name = code_list[key]

    x = c_north_cash_flow.find_one({'code': code})
    if x is not None:
        continue

    url = url_path1 + code
    response = requests.get(url, headers=HEADER)

    soup = BeautifulSoup(response.content)
    # 获取包含echarts数据的元素
    tag = None
    try:
        tag = soup.body.find_all('script')[2]
    except:
        continue

    # 处理横坐标数据，也就是时间数据
    d_timeData_list = []
    td_tmp = re.findall('timeData = \[.+\]', str(tag))[0].split('[', 1)[1].split(']', 1)[0].split(',')
    for td in td_tmp:
        d_timeData_list.append(td.split('\'')[1])
    # 判断是否有数据，没有数据表示不是沪股通、深股通
    if d_timeData_list[0] == '':
        continue

    a = re.findall('option = {.+}', str(tag).replace('\n', ''))[0].split('=', 1)[1].replace(' ', '')
    a = re.findall('\[[\d.,-]+\]', a)
    # 持股比例
    d_bili_list = a[0].replace('[', '').replace(']', '').split(',')
    # 股价
    d_gujia_list = a[1].replace('[', '').replace(']', '').split(',')
    # 变动金额，单位万
    d_biandong_list = a[2].replace('[', '').replace(']', '').split(',')

    df = pd.DataFrame()
    df['date'] = d_timeData_list[::-1]
    df['bili'] = d_bili_list[::-1]
    df['gujia'] = d_gujia_list[::-1]
    df['biandong'] = d_biandong_list[::-1]
    try:
        df['bili'] = df['bili'].astype('float64')
    except:
        pass
    try:
        df['gujia'] = df['gujia'].astype('float64')
    except:
        pass
    try:
        df['biandong'] = df['biandong'].astype('float64')
    except:
        pass

    last_date = ''
    yyyy = 2021
    l = []
    for row in df.iterrows():
        row = dict(row[1])
        north_cash_flow = {}
        date = row['date']
        bili = row['bili']
        gujia = row['gujia']
        biandong = row['biandong']
        if date > last_date and last_date != '':
            yyyy -= 1
        last_date = date
        north_cash_flow['code'] = code
        north_cash_flow['name'] = name
        north_cash_flow['date'] = str(yyyy) + date
        north_cash_flow['bili'] = bili
        north_cash_flow['gujia'] = gujia
        north_cash_flow['biandong'] = biandong

        l.append(north_cash_flow)

        # x = c_north_cash_flow.find_one({'code':code,'date':str(yyyy) + date})
        # if x == None:
        #     x = c_north_cash_flow.insert_one(north_cash_flow)
        # else:
        #     x = c_north_cash_flow.update_one(x,{'$set':north_cash_flow})

    # 批量插入
    if l != []:
        c_north_cash_flow.insert_many(l)
    print(code + ' ' + name)
