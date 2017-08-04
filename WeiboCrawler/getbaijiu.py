#coding=utf-8
import requests
import threadpool
import json
import time

def get(num):
    url = 'http://m.weibo.cn/container/getIndex?uid=1713926427&luicode=20000174&type=uid&value=1713926427&containerid=1076031713926427&page=' + str(num)
    cookie = {"Cookie": "_T_WM=55319b69226094d6e518572a471146b9; SCF=AgR7AgQHn5NJ_eR04XRhau9xCf8abLV2SSFu827l7ExR05EbOFcFUBqdTUIPzoQbLxL2wp1zDcjvuPmwZLVatkM.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF1XRfDf04FghIQF_VAcFl-5JpX5KMhUgL.Fo-cS0ncSK2RS0.2dJLoIp7LxKML1KBLBKnLxKqL1hnLBoMfSoMRSo-p1hM4; H5_INDEX=3; H5_INDEX_TITLE=%E6%A3%AE%E6%80%83; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D102803_ctg1_8999_-_ctg1_8999_home%26fid%3D102803_ctg1_8999_-_ctg1_8999_home%26uicode%3D10000011; SUB=_2A251pCTkDeRxGeNI7FoX9S_EzDWIHXVXZ0ysrDV6PUJbkdBeLRfYkW1X2jEpOxIY8aMxW03OQmdpXIutVw..; SUHB=079jGEsG4-Vtvd; SSOLoginState=1486902452"}

    try:
        html = requests.get(url, cookies=cookie, timeout = 3).content
        data = json.loads(html.decode())
    except:
        print(num)
        return
    for each in data['cards']:
        print(each)
        id = each['itemid'].split('_-_')[1]
        url1 = 'http://m.weibo.cn/api/comments/show?id=' + id + '&page='
        for num in range(20000):
            time.sleep(2)
            url2 = url1 + str(num+1)
            try:
                data2 = requests.get(url2, cookies = cookie).content.decode()
                data2 = json.loads(data2)
                for each2 in data2['data']:
                    print(each2['user']['screen_name'])
                    if each2['user']['id'] == 5165550870:#5884844329
                        print('each2:', each2, '\n')
                        txt = each['mblog']['text'] + ':    ' + each2['created_at'] + '    ' + each2['text']
                        print('txt: ', txt,
                              "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        f = open('weibo.txt', 'a', encoding='utf-8')
                        f.write(txt)
                        f.close()
            except:
                break;

if __name__ == '__main__':
    threads = []
    pool = threadpool.ThreadPool(1)
    for num in range(471,477):
        threads.append(num)
    threads = threadpool.makeRequests(get, threads)
    for t in threads:
        pool.putRequest(t)
    pool.wait()