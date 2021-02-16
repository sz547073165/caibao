import requests
import random
import code_list
import time
import pandas
import taobao

user_agent = [
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52"
]

# 'User-Agent': random.choice(user_agent),  # 浏览器头部
# 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', # 客户端能够接收的内容类型
# 'Accept-Language': 'en-US,en;q=0.5', # 浏览器可接受的语言
# 'Connection': 'keep-alive', # 表示是否需要持久连接


url_p1 = 'http://basic.10jqka.com.cn/api/stock/export.php?export=diy&type=report&code='
url_p2 = '&userid=177763131&cache=a3aa4c400773b0e8ce899590065689d8'

code_list = code_list.code_list
code_list_len = len(code_list)
code_list_len_done = 3950

path = 'caibao_file/'

s = requests.Session()


# for key,value in jar.items():
# 	print(key + '=' + value)

HEADER = {
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cache-Control': 'max-age=0',
    'Connection': 'keep-alive',#'close', #'keep-alive',
    # 'Cookie': cookie,
    'Host': 'basic.10jqka.com.cn',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36',
}

taobao1 = taobao.TaoBao()

for i in range(code_list_len_done, code_list_len + 1):
    code_name = code_list[i - 1]
    code = code_name.split('_')[0]
    name = code_name.split('_')[1]
    url = url_p1 + code + url_p2
    filename = code_name + '.xls'
    code_list_len_done += 1

    HEADER['referer'] = url
    s.cookies = taobao1.read_cookies()
    s.headers = HEADER
    r = s.get(url=url)
    taobao1.set_cookies(r.cookies)
    with open(path + filename, 'wb') as code:
        code.write(r.content)

    print(url)
    print('已完成：' + str(code_list_len_done) + '/' + str(code_list_len))
    second = int(random.uniform(4, 6))
    print('等待：' + str(second) + '秒')
    time.sleep(second)  # 随机等待2～5秒

    print('s.cookies')
    for key, value in s.cookies.items():
        print(key + '=' + value)

    print('r.cookies')
    for key, value in r.cookies.items():
        print(key + '=' + value)

print('end...')
