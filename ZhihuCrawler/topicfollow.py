#coding=utf-8
import requests
from bs4 import BeautifulSoup
import os
import json
import time
import pymysql
import globalValue
import threading
import threadpool


global agreeid
global tableitem
tableitem = "agree_kaoyan_xiangrikuirensheng_b"
agreeid = 5409281

def store(userlink, topic):
    try:
        conn = pymysql.connect(user=globalValue.MySQLRoot, password=globalValue.MySQLPassword,
                               host=globalValue.MySQLHost, db=globalValue.MySQLDatabase)
        cur = conn.cursor()
    except:
        print('db conn error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    try:
        cur.execute("UPDATE score SET " + topic + " = 1 WHERE userlink = '" + userlink + "'")
        print(topic)
        conn.commit()
    except:
        pass
    try:
        cur.close()
        conn.close()
    except:
        pass

def getUsers():
    try:
        conn = pymysql.connect(user=globalValue.MySQLRoot, password=globalValue.MySQLPassword,
                               host=globalValue.MySQLHost, db=globalValue.MySQLDatabase)
        cur = conn.cursor()
    except:
        print('db conn error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    try:
        cur.execute('select userlink from score')
        rows = cur.fetchall()
    except:
        pass
    try:
        cur.close()
        conn.close()
        return rows
    except:
        pass

def login():
    url = "http://www.zhihu.com"
    loginURL = "http://www.zhihu.com/login/phone_num"

    global headers
    headers= {
        'Host': 'www.zhihu.com',
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, sdch, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'authorization':'Bearer Mi4wQUhCQ1ZOLW1JQXNBUU1DM3g5RG9DUmNBQUFCaEFsVk4taU9nV0FBNk1PQkN5R1d0SzhmaW5VREpyb3R3NDJiMWZn|1484405575|cd2fec2629a9320e144b34b8bab4dca147dc8890',
        'Connection':'keep-alive',
        'Host':'www.zhihu.com',
        'Referer':'https://www.zhihu.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
        'x-udid':'"AEDAt8fQ6AmPTsSrdMsSi80eikf-TVy1nZ0=|1463022809"'
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

def definetopic(userlink, topic):
    switchdict = {
        '电影':'topicfollow_dianying',
        '游戏':'topicfollow_youxi',
        'iOS 游戏':'topicfollow_iosyouxi',
        'iPhone 游戏':'topicfollow_iphoneyouxi',
        'iPad 游戏':'topicfollow_ipadyouxi',
        '运动':'topicfollow_yundong',
        '健身':'topicfollow_jianshen',
        '跑步':'topicfollow_paobu',
        '互联网':'topicfollow_hulianwang',
        '电子商务':'topicfollow_dianzishangwu',
        'iOS 应用':'topicfollow_iosyingyong',
        '豆瓣':'topicfollow_douban',
        '知乎':'topicfollow_zhihu',
        '文学':'topicfollow_wenxue',
        '小说':'topicfollow_xiaoshuo',
        '电影推荐':'topicfollow_dianyingtuijian',
        'Instagram':'topicfollow_instagram',
        '书法':'topicfollow_shufa',
        '老爸老妈浪漫史（美剧）':'topicfollow_laobalaomalangmanshimeiju',
        '练字':'topicfollow_lianzi',
        '肖申克的救赎（电影）':'topicfollow_xiaoshenkedejiushudianying',
        '蔡康永':'topicfollow_caikangyong',
        '谍影重重（电影）':'topicfollow_dieyingchongchongdianying',
        '杰森·斯坦森':'topicfollow_jiesensitansen',
        '马特.达蒙':'topicfollow_matedameng',
        '心灵捕手':'topicfollow_xinlingbushou',
        '阅读':'topicfollow_yuedu',
        'Kindle':'topicfollow_kindle',
        '读书方法':'topicfollow_dushufangfa',
        'Kindle vs. iPad':'topicfollow_kindlevsipad',
        '生活方式':'topicfollow_shenghuofangshi',
        '旅行':'topicfollow_lvxing',
        '旅游':'topicfollow_lvyou',
        '教育':'topicfollow_jiaoyu',
        '考研':'topicfollow_kaoyan',
        '复旦大学':'topicfollow_fudandaxue',
        '复旦大学研究生':'topicfollow_fudandaxueyanjiusheng',
        '资产评估师':'topicfollow_zichanpinggushi',
        '历史':'topicfollow_lishi',
        '文化':'topicfollow_wenhua',
        '经济学常识':'topicfollow_jingjixuechangshi',
        '三体（系列小说）':'topicfollow_santixiliexiaoshuo',
        '盗墓笔记（小说）':'topicfollow_daomubijixiaoshuo',
        '北京航空航天大学':'topicfollow_beihang',
        '首都经济贸易大学':'topicfollow_shoujing',
        '追风筝的人':'topicfollow_zhuifengzhengderen',
        '嫌疑人X的献身':'topicfollow_xianyirenxdexianshen',
        '注册会计师（CPA）':'topicfollow_zhucekuaijishicpa',
        '程序员':'topicfollow_chengxuyuan',
        '东野圭吾':'topicfollow_dongyeguiwu',
        '弗洛伊德':'topicfollow_fuluoyide',
        '许嵩（人物）':'topicfollow_xusongrenwu',
        '经济学':'topicfollow_jingjixue',
        '资产评估':'topicfollow_zichanpinggu',
        '投资':'topicfollow_touzi',
        '音乐':'topicfollow_yinyue',
        '影视评论':'topicfollow_yingshipinglun',
        '时空恋旅人':'topicfollow_shikonglianlvren',
        '法律':'topicfollow_falv',
        '法律常识':'topicfollow_falvchangshi',
        '自然科学':'topicfollow_zirankexue',
        '物理学':'topicfollow_wulixue',
        '量子物理':'topicfollow_liangziwuli',
        '视力保健':'topicfollow_shilibaojian',
        '星座（迷信）':'topicfollow_xingzuomixin',
        '拉马努金（Srinivasa Ramanujan）':'topicfollow_lamanvjin',
        '健康':'topicfollow_jiankang',
        '医学':'topicfollow_yixue',
        '抑郁症':'topicfollow_yiyuzheng',
        '心理':'topicfollow_xinli',
        '医学常识':'topicfollow_yixuechangshi',
        '睡眠质量':'topicfollow_shuimianzhiliang',
        '近视眼':'topicfollow_jinshiyan',
        '社交恐惧症':'topicfollow_shejiaokongjuzheng',
        '商业':'topicfollow_shangye',
        '体育':'topicfollow_tiyu',
        '科技':'topicfollow_keji',
        '宇宙学':'topicfollow_yuzhouxue',
        '相对论':'topicfollow_xiangduilun',
        '金融':'topicfollow_jinrong'
    }
    try:
        store(userlink, switchdict.get(topic))
    except:
        pass

def getTopicFollowers(userlink):
    userids = userlink.split('/')
    userid = userids[len(userids) - 1]
    source_url = 'https://www.zhihu.com/api/v4/members/' + userid + '/following-topic-contributions?include=data%5B*%5D.topic.introduction&offset=0&limit=20'
    nextsource_url = source_url
    for num in range(20):
        try:
            nextsource = s.get(nextsource_url, headers=headers)
        except:
            time.sleep(2)
            nextsource = s.get(nextsource_url, headers=headers)
        nextcontent = nextsource.content
        try:
            nextdata = json.loads(nextcontent.decode())
            for each in nextdata['data']:
                try:
                    title = each['topic']['name']
                    definetopic(userlink, title)
                except:
                    continue
            nextsource_url = nextdata['paging']['next']
        except:
            pass

if __name__ == '__main__':
    rows = getUsers()
    pool = threadpool.ThreadPool(30)
    topiclist = []
    for row in rows:
        topic = str(row).split("'")[1]
        print(topic)
        topiclist.append(topic)
    threads = threadpool.makeRequests(getTopicFollowers, topiclist)
    login()
    for t in threads:
        pool.putRequest(t)
    pool.wait()