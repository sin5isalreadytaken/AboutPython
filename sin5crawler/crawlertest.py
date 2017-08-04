import urllib.request
import urllib.parse

import gzip
def ungzip(data):
    try:
# 尝试解压
        print('正在解压.....')
        data = gzip.decompress(data)
        print('解压完毕!')
    except:
        print('未经压缩, 无需解压')
    return data

import re
def getXSRF(data):
    cer = re.compile('name="_xsrf" value="(.*)"', flags = 0)
# 编译正则表达式，返回RegexObject对象，然后可以通过RegexObject对象调用match()和search()方法。
# prog = re.compile(pattern)
# result = prog.match(string)
# 跟
# result = re.match(pattern, string)
# 是等价的。
    strlist = cer.findall(data)
    return strlist[0]

import http.cookiejar
def getOpener(head):#参数为字典
#处理cookie
    cj = http.cookiejar.CookieJar()
    pro = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(pro)
    header = []#列表
    for key, value in head.items():
        elem = (key, value)#元组
        header.append(elem)
    opener.addheaders = header
    return opener#opener可以自动处理使用 opener 过程中遇到的 Cookies,自动在发出的 GET 或者 POST 请求中加上自定义的 Header

header = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36',
    'Accept-Encoding': 'gzip, deflate',
    'Host': 'www.zhihu.com',
    'DNT': '1'
}

url = 'https://www.zhihu.com'
opener = getOpener(header)
op = opener.open(url)
data = op.read()
data = ungzip(data)
# 解压
_xsrf = getXSRF(data.decode())
print(_xsrf)
url += '/login/phone_num'
id = '13051570207'
password = 'javonsears'
postDict = {
        '_xsrf':_xsrf,
        'phone_num': id,
        'password': password,
        'rememberme': 'y'
}
postData = urllib.parse.urlencode(postDict).encode('utf-8')#urllib.parse 库里的 urlencode() 函数可以把 字典 或者 元组集合 类型的数据转换成 & 连接的 str.
op = opener.open(url, postData)
data = op.read()
data = ungzip(data)

print(data.decode('unicode_escape'))

# response = urllib.request.urlopen("https://www.zhihu.com/topic/19864529/followers")
# html = response.read()
# html1 = html.decode("utf-8")
# response.close()
# print(html1)