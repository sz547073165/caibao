import json
import datetime
import pandas as pd

f = open("north_cash_flow_data.txt")
data_json_str = ''
for line in f:
    data_json_str += line

data_json = dict(json.loads(data_json_str))
mmdd = '0210'
yyyy = '2021'

df = pd.DataFrame(columns=['shares','date','1','3','5','7','9'])

for code in data_json:
    biandong = data_json.get(code).get('biandong',None)
    if biandong == None:
        continue
    if biandong.get(mmdd,None) == None:
        continue

    biandong_l = []
    mmdd_l = []
    count_d = 1 # 天数
    count_0 = 0 # 小于0的数量
    count_1 = 0 # 大于0的数量
    s = {}

    for i in range(0,20):
        yyyymmdd_tmp = yyyy+mmdd
        dt = datetime.datetime.strptime(yyyymmdd_tmp, "%Y%m%d")
        out_date = (dt + datetime.timedelta(days=-(i))).strftime("%Y%m%d")
        bian = biandong.get(out_date[4:8],None)
        if bian != None:
            mmdd_l.append(out_date[4:8])
            biandong_l.append(bian)
            if bian>0 :
                count_1+=1
            elif bian<0:
                count_0+=1

            if i+1==1:
                s['1']=count_1/count_d
            elif i+1 == 3:
                s['3'] = count_1/count_d
            elif i+1 ==5:
                s['5'] = count_1 / count_d
            elif i+1==7:
                s['7'] = count_1 / count_d
            elif i+1==9:
                s['9'] = count_1 / count_d

            s['shares'] = code
            s['date'] = mmdd
            if s.get('1',None) ==None:
                s['1'] =0
            if s.get('3',None) == None:
                s['3'] = 0
            if s.get('5',None) == None:
                s['5'] = 0
            if s.get('7',None) == None:
                s['7'] = 0
            if s.get('9',None) == None:
                s['9'] = 0
            count_d+=1
    if s['1'] ==1 and s['1']>=s['3']and s['3']>=s['5'] and s['5']>=s['7'] and s['7']>=s['9']:
        df = df.append([s],ignore_index=True)
    # print(code)
# print()
writer = pd.ExcelWriter('/Users/zhangmin/Documents/data_shares/北向资金建仓追踪.xlsx')
df.to_excel(writer)
writer.save()