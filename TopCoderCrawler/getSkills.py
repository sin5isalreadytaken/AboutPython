import urllib.request
import urllib.error
import json
import globalValue
import pymysql
import threading

users = ['saarixx', 'kyky', 'dmks', 'duner', 'aubergineanode', 'dcp', 'catechumen', 'nhzp339', 'soso0574', 'magicpig']
users += ['Petr', 'tourist', 'rng_58', 'scott_wu', 'Kankuro', 'ACRush', 'Egor', 'xudyh', 'krijgertje', 'Um_nik']
users += ['iamtong', 'abedavera', 'selvia_ettine', 'oninkxronda', 'gh3ablo', 'DaraK', 'yoki', '5y5', 'picachui', 'ujazz']

#参数string：user；返回值string：获取skills的url
def users2urls(user):
    return globalValue.user2skillsUrl.replace('?', user)

#参数string：user，skills。所有skills保存在一个json字符串中
def storeUserSkills(user, skills):
    try:
        conn = pymysql.connect(user=globalValue.MySQLRoot, password=globalValue.MySQLPassword, host=globalValue.MySQLHost, db=globalValue.MySQLDatabase)
        cur = conn.cursor()
    except:
        print('db conn error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS " + globalValue.MySQLUser_SkillsTableName + " (user varchar(50) not null, skills varchar(1000), primary key(user)) ENGINE=InnoDB DEFAULT CHARSET=utf8")
        cur.execute("INSERT INTO " + globalValue.MySQLUser_SkillsTableName + "(user,skills) VALUES(%s,%s)", (user, skills))
        conn.commit()
    except:
        pass
    try:
        cur.close()
        conn.close()
    except:
        pass

class skillsCrawler(threading.Thread):
    def __init__(self, user):
        super().__init__()
        self.user = user
    def run(self):
        try:
            request = urllib.request.Request(users2urls(self.user))
            request.add_header('User-Agent',
                               'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
            response = urllib.request.urlopen(request, timeout=globalValue.timeout)
            responseStr = response.read().decode('utf-8')
            userDict = json.loads(responseStr)
            skillsDict = userDict['result']['content']['skills']
            skillsKeys = skillsDict.keys()
            skills = []  # 所有skills保存在一个字符串中
            for j in skillsKeys:
                skills.append(skillsDict[j]['tagName'])
            storeUserSkills(self.user, json.dumps(skills))
        except urllib.error.URLError as e:
            print('URLError: errorReason: user=', i, e.reason)
        except urllib.error.HTTPError as e:
            print('HTTPError: errorCode: user=', i, e.code)
        except:
            pass

for i in users:
    skillsCrawler(i).start()


