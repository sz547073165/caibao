import pandas as pd
import os
import code_list

# 引资模型处理

p = '/Users/zhangmin/Documents/同花顺资产负债表'

targe_col = ['时间',
             '应付票据及应付账款','预收款项','合同负债','其他流动负债',
             '短期借款','衍生金融负债','一年内到期的非流动负债','长期借款','应付债券',
             '实收资本','资本公积']
f = []
g = []
column_name = {0: '时间',
1:'股票代码', 2:'股票名称',
3: '上下游指数', 4: '金融债指数', 5: '上下金融比',6: '经营性负债', 7: '金融性负债', 8: '股东入资',
               9: '应付票据及应付账款', 10: '预收款项', 11: '合同负债', 12: '其他流动负债',
               13: '短期借款', 14: '衍生金融负债', 15: '一年内到期的非流动负债', 16: '长期借款', 17: '应付债券',
               18: '实收资本', 19: '资本公积',

               }
df_total = pd.DataFrame(columns=column_name)
df_total.rename(columns=column_name, inplace=True)
aa = df_total.columns.tolist()
aa.insert(3,'时间1')
aa.insert(7,'时间2')
df_total = df_total.reindex(columns =aa)
# print(df_total)

code_list = code_list.code_list
# code_name_d = {}
# for co in code_list:
#     code_name_d[str(co.split('_',1)[0])] = str(co.split('_',1)[1])

for root, dirs, files in os.walk(p):
    # 当前目录路径
    # print(root)
    # 当前路径下所有子目录
    # print(dirs)
    # 当前路径下所有非目录子文件
    # print(files)
    f = files

for t in f:
    g.append(t.split('_', 1)[0])
c = len(f)
for filename in f:
    if filename == '.DS_Store':
        continue
    pf = p + '/' + filename
    # print(pf)

    df = pd.read_excel(pf).T
    # print(df)

    code = filename.split('_', 1)[0]
    name = code_list.get(code)

    line_1 = df.iloc[0]
    column_name_tmp = {}
    for index in range(0,len(line_1)):
        col = line_1[index]
        a =0
        for i in targe_col:
            a = col.find(i)
            if a>=0 :
                column_name_tmp[index] = i
                break
        if a == -1 :
            column_name_tmp[index] = line_1[index]
    # 重命名column
    df.rename(columns=column_name_tmp, inplace=True)
    df = df.drop(['Unnamed: 0'], axis=0)

    # 判断是否有目标列，没有的话默认0填充
    for i in targe_col:
        if i not in df.columns:
            df[i] = 0

    df['股票代码'] = code
    df['股票名称'] = name

    # 替换"--"字符串为""
    def replacestr(x):
        if x == '--':
            return int(x.replace('--', '0'))
        else:
            return x

    df = df.applymap(replacestr)
    df.sort_values('时间',inplace=True)

    df['经营性负债'] = (df['应付票据及应付账款'] + df['预收款项'] + df['合同负债'] + df['其他流动负债']) / 100000000
    df['金融性负债'] = (df['短期借款'] + df['衍生金融负债'] + df['一年内到期的非流动负债'] + df['长期借款'] + df['应付债券']) / 100000000
    df['股东入资'] = (df['实收资本'] + df['资本公积']) / 100000000
    df['上下游指数'] = df['经营性负债'] / (df['经营性负债'] + df['股东入资'])
    df['金融债指数'] = df['金融性负债'] / (df['金融性负债'] + df['股东入资'])
    df['上下金融比'] = df['经营性负债'] / (df['经营性负债'] + df['金融性负债'])

    # 向下填充nan值
    df['上下游指数'] = df['上下游指数'].fillna(method='ffill')
    df['金融债指数'] = df['金融债指数'].fillna(method='ffill')
    df['上下金融比'] = df['上下金融比'].fillna(method='ffill')

    df_new = pd.DataFrame()

    for i in range(0,len(column_name)):
        if i ==0:
            continue
        elif i == 3:
            df_new['时间1'] = df['时间']
        elif i == 6:
            df_new['时间2'] = df['时间']
        col = column_name[i]
        df_new[col] = df[col]

    df_total = df_total.append(df_new, ignore_index=True)
    # print(df_total)
    # print(filename)

    c -= 1
    if c % 300 == 0:
        print(c)

    # 单个存储
    # writer = pd.ExcelWriter('引资模型/' + code +'_'+ name +'.xlsx')
    # df_new.to_excel(writer)
    # writer.save()

# 整合存储
# df_total.drop('时间')
writer = pd.ExcelWriter('/Users/zhangmin/Documents/data_shares/引资战略模型.xlsx')
df_total.to_excel(writer)
writer.save()

print('end')
