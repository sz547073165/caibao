import code_list
from bs4 import BeautifulSoup
import requests
import re
import json
import pandas as pd
import time

HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',#'close', #'keep-alive',
    # 'Cookie': cookie,
    # 'Host': 'basic.10jqka.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}

code_list = code_list.code_list
url_path1 = 'http://www.gzyuwan.com/echarts.php?code='


f = open("north_cash_flow_data.txt")
data_json_str = ''
for line in f:
    data_json_str += line

data_json = dict(json.loads(data_json_str))
d = '0210'

for key in code_list:
    if key[0:2] not in ['60','00']:
        continue
    # os.system('killall Safari')
    code = key
    name = code_list[key]

    target_ = data_json.get(code, None)
    if target_ == None:
        target_ = {code: {}}
        data_json[code] = {}

    try:
        if target_['bili'].get(d,None) != None:
            if target_['gujia'].get(d,None) != None:
                if target_['biandong'].get(d,None) != None:
                    continue
    except:
        pass

    url = url_path1 + code
    response = requests.get(url,headers = HEADER)

    soup = BeautifulSoup(response.content)
    # 获取包含echarts数据的元素
    tag = soup.body.find_all('script')[2]

    # 处理横坐标数据，也就是时间数据
    d_timeData_list = []
    td_tmp = re.findall('timeData = \[.+\]', str(tag))[0].split('[',1)[1].split(']',1)[0].split(',')
    for td in td_tmp:
        d_timeData_list.append(td.split('\'')[1])
    # 判断是否有数据，没有数据表示不是沪股通、深股通
    if d_timeData_list[0] == '':
        continue

    a = re.findall('option = {.+}',str(tag).replace('\n',''))[0].split('=',1)[1].replace(' ','')
    a = re.findall('\[[\d.,-]+\]',a)
    # 持股比例
    d_bili_list = a[0].replace('[','').replace(']','').split(',')
    # 股价
    d_gujia_list = a[1].replace('[','').replace(']','').split(',')
    # 变动金额，单位万
    d_biandong_list = a[2].replace('[','').replace(']','').split(',')

    df = pd.DataFrame()
    df['date'] = d_timeData_list
    df['bili'] = d_bili_list
    df['gujia'] = d_gujia_list
    df['biandong'] = d_biandong_list
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

    for row in df.iterrows():
        row = dict(row[1])
        target_ = data_json.get(code,None)
        if target_==None:
            target_ = {code:{}}
            data_json[code] = {}

        target_bili = target_.get('bili',None)
        if target_bili == None:
            target_bili = {}
        target_bili[row['date']] = row['bili']

        target_gujia = target_.get('gujia',None)
        if(target_gujia == None):
            target_gujia = {}
        target_gujia[row['date']] = row['gujia']

        target_biandong = target_.get('biandong',None)
        if(target_biandong == None):
            target_biandong = {}
        target_biandong[row['date']] = row['biandong']

        data_json[code]['bili'] = target_bili
        data_json[code]['gujia'] = target_gujia
        data_json[code]['biandong'] = target_biandong
    print(code + name)
        # print(data_json)

    # with open('north_cash_flow_data.txt', 'wb') as code:
    #     code.write(json.dumps(data_json))

    f = open('north_cash_flow_data.txt', 'w')
    f.write(json.dumps(data_json))
    f.close()

    time.sleep(0.01)
    # print(a)
