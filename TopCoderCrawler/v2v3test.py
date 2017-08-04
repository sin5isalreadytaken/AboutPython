import urllib.request

response = urllib.request.urlopen('http://api.topcoder.com/v2/users/iRabbit/statistics/develop')
print(response.read().decode('utf-8'))