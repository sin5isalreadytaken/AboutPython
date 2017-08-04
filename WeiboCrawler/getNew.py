#coding=utf-8
import requests
import threadpool
import json
import time

def get(num):
    url = 'http://m.weibo.cn/container/getIndex?uid=1713926427&luicode=20000174&type=uid&value=1713926427&containerid=1076031713926427&page=' + str(num)
    cookie = {"Cookie": "_T_WM=45e71aaa896de1c3d95908e5059597a6; SCF=AgR7AgQHn5NJ_eR04XRhau9xCf8abLV2SSFu827l7ExREYucrShU88Gm8SqjVTYBM8I7-mwmq8mqeCGTLK1Wzts.; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9W5cxnqrQHIshgWh9AiEaBpW5JpX5o2p5NHD95Q01hqXSoqpe0zfWs4DqcjCi--ci-20i-88i--ciKn7iKn0; M_WEIBOCN_PARAMS=luicode%3D20000174; SUB=_2A251xgWHDeRxGeVG7VYX9i_PyTmIHXVXSKvPrDV6PUJbkdBeLVXSkW0CaPYqD8yKU8FH4dQUUYXGhNCZsw..; SUHB=0auAxtrtUsS_sg; SSOLoginState=1489139159"}

    try:
        html = requests.get(url, cookies=cookie).content
        data = json.loads(html.decode())
    except:
        print(num)
        return
    for each in data['cards']:
        print('each:',each)
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
                    if each2['user']['id'] == 577225884:
                        print('each2:',each2, '\n')
                        txt = each['mblog']['text'] + ':    ' + each2['created_at'] + '    ' + each2['text']
                        print('txt: ',txt, "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
                        f = open('weibo.txt', 'a', encoding='utf-8')
                        f.write(txt)
                        f.close()
            except:
                break;

if __name__ == '__main__':
    threads = []
    pool = threadpool.ThreadPool(1)
    for num in range(2,10):
        threads.append(num)
    threads = threadpool.makeRequests(get, threads)
    for t in threads:
        pool.putRequest(t)
    pool.wait()