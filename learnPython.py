if (True and 1):
    print("true")
    print("true2")
else:
    print("false")
print("out")

import sys; x = "输出"; sys.stdout.write(x + \
                                       "结束")

str = "输出两次"
print(str * 2)

list1 = ['a', 1]
tuple1 = ('abc', '元组',
         2.3, list1)
print(tuple1)
print(tuple1[1: 3])
print(tuple1[2:])
print(tuple1[-4: -1])

dictionary1 = {1: '一', 'john': tuple}
print(dictionary1['john'])
print(dictionary1[1])
#迭代器
it = iter(tuple1)
print(next(it))
print(next(it))
for i in it:
    print(i, end='\n\n')
# it2 = iter(tuple1)
# while True:
#     try:
#         print(next(it2))
#     except StopIteration:
#         sys.exit(1)
#元组与列表转换
print(list(tuple1))

#商为整数
print(3//2)
print(3/2)
#3^2=9
print(3**2)

if not 2 in list1:
    print('list1 check')

a = 20
b = 20
#格式化输出
print("%d %d"%(id(a), id(b)))
#TODO
if a is b:
    print('a is b')
b = 30
print(id(b))

#TODO
for num in range(len(tuple1)):
    b -= 1
    print(b)
else:
    print(b)

import time
print("当前时间",time.time())
print("当地时间", time.localtime(time.time()))
print("格式化时间", time.asctime(time.localtime(time.time())))
print("格式化日期", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time())), time.strftime("%a %b %d %H:%M:%S %Y", time.localtime()))
import calendar
cal = calendar.month(2016, 9)
print("日历", cal,"end")

def printme(str):
    print(str)
    return
#关键字参数
printme(str = "abc")

def printinfo(name, age = 20):
    print(name, age)
    return
#缺省参数
printinfo("名字")

def printanything(arg1, *args):
    print(arg1)
    for var in args:
        print(var)
    return
#不定长参数
printanything("字符串", 10, 20, "again")

printsum = lambda arg1, arg2 : print(arg1+arg2)
#匿名函数
printsum(2, 3)
print(id(printsum))
print(id(printanything))

# #io操作
# str = input("输入：")
# print("确认",str)

#生成器
def fibonacci(n):
    a, b, counter = 0, 1, 0
    while True:
        if counter > n:
            return
        yield a
        a, b = b, a + b
        counter += 1
    return
f = fibonacci(30)
for ff in f:
    print(ff, end=" ")
