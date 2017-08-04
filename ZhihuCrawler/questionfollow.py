#coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import pymysql
import globalValue

global agreeid
global tableitem
tableitem = "agree_jiesensitansen_nanqiaozi_d"
agreeid =19429186

def storeScore(user, userlink, sign):
    try:
        conn = pymysql.connect(user=globalValue.MySQLRoot, password=globalValue.MySQLPassword, host=globalValue.MySQLHost, db=globalValue.MySQLDatabase)
        cur = conn.cursor()
    except:
        print('db conn error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    try:
        cur.execute("INSERT INTO " + globalValue.MySQLTableName + "(user,userlink,signature) VALUES(%s,%s,%s)", (user.encode("utf-8"),userlink.encode("utf-8"),sign.encode("utf-8")))
        conn.commit()
    except:
        pass
    try:
        cur.execute("UPDATE score SET " + tableitem + " = 1 WHERE userlink = '" + userlink + "'")
        conn.commit()
    except:
        pass
    try:
        cur.close()
        conn.close()
    except:
        pass

def login():
    url = "http://www.zhihu.com"
    loginURL = "http://www.zhihu.com/login/phone_num"

    global headers
    headers= {
        'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Cache-Control':'max-age=0',
        'Connection':'keep-alive',
        'Cookie':'_zap=9875862c-f4e1-43e7-a675-69fe63576e38; d_c0="AJBCcM2uKAuPTivasHQzkhuysFwbCQTX1xk=|1484488738"; q_c1=a2b6c25948d34d44802f3c37b905e56a|1484488739000|1484488739000; _xsrf=e948554456f33835f900ed5d23d21240; _zap=2c8eaf7c-1fcf-4487-81ea-5f92a1278472; capsion_ticket="2|1:0|10:1484569225|14:capsion_ticket|44:ZjUzZTBkMWZkNmQyNDRlOGJjNTJmMTVkMTZiMzRkYzI=|40b83c9e1c0a9b000ef8aa72703f2ceffe5f9aec56fe4518dae6588a0f1e9710"; l_cap_id="ZjExYzM4ZTQxOTg1NDE1MmEyYjIwYzA5MWI2OWQ1MjY=|1484638052|24ce3a3c37acd0406d72a8ea94b4765ae4e599bf"; cap_id="ZWRlNjM1OTAxZjQzNGY1Yjg1M2U2YTk2NDQwNjRmNDA=|1484638052|cca29ae750fa0041a1709e5a50600a9ca0728026"; r_cap_id="YTFiMGZlN2Q5NDRkNGQyMWIwN2RkNjAzYzIwM2Q5ODk=|1484638052|69e75ddfc705a07b7051bbe838837b46ce7cc2a5"; login="YTU5MjM4OThkMzA1NDhmZDk2ZGIyNGExNTNkZjBmMzY=|1484638274|65e97a30c880932e08fc6877987fa35accf5806f"; aliyungf_tc=AQAAAKCFrEHotAcAwp2ee1QcJX2i4wqk; s-q=%E7%94%B7%E5%A5%B3%E7%BA%AF%E5%8F%8B%E8%B0%8A; s-i=9; sid=7lg0qiog; s-t=autocomplete; __utmt=1; z_c0=Mi4wQU1DQ1RfQlE1Z2NBa0VKd3phNG9DeGNBQUFCaEFsVk5RbFdsV0FCUEppTVZiVjgxOWJtREt4dmROOFhkd3pCOTF3|1484894462|d14ae384b8bb56ef98086b9d37e91f168152a235; __utma=51854390.436030167.1484642258.1484823346.1484892295.8; __utmb=51854390.38.9.1484893805256; __utmc=51854390; __utmz=51854390.1484892295.8.8.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=51854390.100-1|2=registration_date=20150408=1^3=entry_date=20150408=1',
        'Host':'www.zhihu.com',
        'Referer':'https://www.zhihu.com/question/19731263?rf=21394005',
        'Upgrade-Insecure-Requests':'1',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
    }

    data = {
        'phone_num': '13175349550',
        'password': 'sin5zhihu',
        'rememberme': "true",
    }

    global s
    s = requests.session()
    global xsrf
    if os.path.exists("cookiefile"):
        with open("cookiefile") as f:
            cookie = json.load(f)
        s.cookies.update(cookie)
        reql = s.get(url, headers=headers)
        soup = BeautifulSoup(reql.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')
    else:
        req = s.get(url, headers=headers)
        print(req)

        soup = BeautifulSoup(req.text, "html.parser")
        xsrf = soup.find('input', {'name': '_xsrf', 'type': 'hidden'}).get('value')

        data['_xsrf'] = xsrf

        timestamp = int(time.time() * 1000)
        captchaURL = 'http://www.zhihu.com/captcha.gif?=' + str(timestamp)
        print(captchaURL)

        with open('zhihucaptcha.gif', 'wb') as f:
            captchaREQ = s.get(captchaURL, headers=headers)
            f.write(captchaREQ.content)
        loginCaptcha = input('input captcha:\n').strip()
        data['captcha'] = loginCaptcha
        print(data)
        loginREQ = s.post(loginURL, headers=headers, data=data)
        if not loginREQ.json()['rememberme']:
            print(s.cookies.get_dict())
            with open('cookiefile', 'w') as f:
                json.dump(s.cookies.get_dict(), f)
        else:
            print('login fail')

Zhihu = 'http://www.zhihu.com'
def getQuestionFollowers(que_id):
    source_url = Zhihu + '/question/' +str(que_id) +'/followers'
    source = s.get(source_url, headers=headers)
    content = source.content
    print(content)
    data = json.loads(content.decode())   # 包含总赞数、一组点赞者的信息、指向下一组点赞者的资源等的数据
    print(data)
    total = data['paging']['total']   # 总赞数
    # 通过分析，每一组资源包含10个点赞者的信息（当然，最后一组可能少于10个），所以需要循环遍历
    # nextsource_url = source_url     # 从第0组点赞者开始解析
    # num = 0
    # while nextsource_url!=Zhihu:
    #     try:
    #         nextsource = s.get(nextsource_url, headers=headers)
    #     except:
    #         time.sleep(2)
    #         nextsource = s.get(nextsource_url, headers=headers)
    #     nextcontent = nextsource.content
    #     nextdata = json.loads(nextcontent.decode())
    #     for each in nextdata['payload']:
    #         num += 1
    #         print(num);
    #         try:
    #             soup = BeautifulSoup(each, 'lxml')
    #             tag = soup.a
    #             title = tag['title']    # 点赞者的用户名
    #             sign = soup.span.string
    #             href = 'http://www.zhihu.com' + str(tag['href'])    # 点赞者的地址
    #             list = soup.find_all('li')
    #             votes = list[0].string  # 点赞者获取的赞同
    #             tks = list[1].string  # 点赞者获取的感谢
    #             ques = list[2].string  # 点赞者提出的问题数量
    #             ans = list[3].string  # 点赞者回答的问题数量
    #             string = title + '  ' + href + '  ' + votes + tks + ques + ans + sign
    #             # storeScore(title, href, sign)
    #             print(string)
    #         except:
    #             txt3 = '有点赞者的信息缺失'
    #             print(txt3)
    #             continue
    #         storeScore(title, href, sign)
    #     # 解析出指向下一组点赞者的资源
    #     nextsource_url = Zhihu + nextdata['paging']['next']

if __name__ == '__main__':
    login()
    getQuestionFollowers(19731263)
