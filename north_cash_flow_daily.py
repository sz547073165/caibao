import datetime
import pymongo
import hgst
import code_list
import time

my_client = pymongo.MongoClient('localhost:27017')
db = my_client['d_shares']
collection = db['c_north_cash_flow_daily']

code_list = code_list.code_list
date_str = '20210219'
date_str_l = []
doc_delete_l = []
for i in range(0, 40):
    dt = datetime.datetime.strptime(date_str, "%Y%m%d")
    out_date = (dt + datetime.timedelta(days=-(i))).strftime("%Y-%m-%d") + 'T00:00:00'
    date_str_l.append(out_date)
for key in code_list:
    if key[0:2] not in ['60', '00']:
        continue
    # os.system('killall Safari')
    code = key
    name = code_list[key]

    x = collection.find_one({'SCODE': code, 'HDDATE': date_str_l[1]})
    if x is None:
        response = hgst.daily(code)
        if response == [] or response == None:
            continue
        collection.insert_many(response)

    print(code + ' ' + name)

    # 去重部分
    for date in date_str_l:
        tar = {'SCODE': code, 'HDDATE': date}
        num = collection.count_documents(tar)
        if num in (0, 1):
            continue

        doc_l = collection.find(tar)
        for i in range(1, num):
            doc_delete_l.append(doc_l[i]['_id'])
    time.sleep(0.1)
collection.delete_many({'_id': {'$in': doc_delete_l}})
print('已删除：' + str(len(doc_delete_l)))
