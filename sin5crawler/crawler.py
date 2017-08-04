import urllib.request
users4getSkills = {'skills': ['Petr','sin5']}
urls4getSkills = {'skills': []}
response = urllib.request.urlopen("https://api.topcoder.com/v3/members/Petr/skills/")
html = response.read().decode('utf-8')
print(html)

#参数users,返回获取skills的urls
def users2urls(user4getSkills):
    return



