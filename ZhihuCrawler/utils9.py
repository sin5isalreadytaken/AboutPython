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
tableitem = "agree_xusong_pulasi_x"
agreeid = 42813278

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
        "User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:41.0) Gecko/20100101 Firefox/41.0',
        "Referer": "http://www.zhihu.com/",
        'Host': 'www.zhihu.com',
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
def getVoters(ans_id):
    source_url = Zhihu + '/answer/' +str(ans_id) +'/voters_profile'
    source = s.get(source_url, headers=headers)
    content = source.content
    data = json.loads(content.decode())   # 包含总赞数、一组点赞者的信息、指向下一组点赞者的资源等的数据
    total = data['paging']['total']   # 总赞数
    # 通过分析，每一组资源包含10个点赞者的信息（当然，最后一组可能少于10个），所以需要循环遍历
    nextsource_url = source_url     # 从第0组点赞者开始解析
    num = 0
    while nextsource_url!=Zhihu:
        try:
            nextsource = s.get(nextsource_url, headers=headers)
        except:
            time.sleep(2)
            nextsource = s.get(nextsource_url, headers=headers)
        nextcontent = nextsource.content
        nextdata = json.loads(nextcontent.decode())
        for each in nextdata['payload']:
            num += 1
            print(num);
            try:
                soup = BeautifulSoup(each, 'lxml')
                tag = soup.a
                title = tag['title']    # 点赞者的用户名
                sign = soup.span.string
                href = 'http://www.zhihu.com' + str(tag['href'])    # 点赞者的地址
                list = soup.find_all('li')
                votes = list[0].string  # 点赞者获取的赞同
                tks = list[1].string  # 点赞者获取的感谢
                ques = list[2].string  # 点赞者提出的问题数量
                ans = list[3].string  # 点赞者回答的问题数量
                string = title + '  ' + href + '  ' + votes + tks + ques + ans + sign
                # storeScore(title, href, sign)
                print(string)
            except:
                txt3 = '有点赞者的信息缺失'
                print(txt3)
                continue
            storeScore(title, href, sign)
        # 解析出指向下一组点赞者的资源
        nextsource_url = Zhihu + nextdata['paging']['next']

if __name__ == '__main__':
    login()
    getVoters(agreeid)
