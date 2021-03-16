# -*- coding: utf-8 -*-
import socket
import re
global a
global b
a=''
b=''
clients = {}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
s.bind(('172.93.34.44', 9999))
#s.bind(('172.28.32.140', 9999))
print('Bind UDP on 9999...')
addra = (0, 0)
addrb = (0, 0)
while True:
    # 接收数据:

    data, addr = s.recvfrom(1024)
    print('connect from %s:%s.' % addr)
    print('data is:*************  %s.' % data)
    if data == b'hello':               #登陆时候欢迎
        print('--------- from %s:%s.' % addr)
        continue


    if re.search(re.compile(b"(?<=<).+?(?= to)"), data)!=None:  #匹配查找clientA 名字,如果为空则默认名字master
        clientA=re.search(re.compile(b"(?<=<).+?(?= to)"), data).group(0)
    else:
        clientA=b'master'

    if re.search(re.compile(b"(?<=to ).+?(?=>)"), data)!=None: #匹配查找clientB 名字,如果为空则默认名字client
        clientB = re.search(re.compile(b"(?<=to ).+?(?=>)"), data).group(0)
    else:
        clientA = b'client'

    print('clientA:%s  clientB:%s' % (clientA,clientB))
    #header=b'<'+clientA+' to '+clientB+'>'

    if re.search(re.compile(b"<!quit>"),data)!=None: #如果匹配到有quit,就执行退出操作并删除用户
        s.sendto(data, addr)
        if clients.has_key(clientA):
            del clients[clientA]
            print('delete %s'% clientA)

    if re.search(re.compile(b"(?<=data=).+"),data)==None:  #如果发过来的数据是空，则不做操作
        continue

    if re.search(re.compile(b"<.+?>"), data)!=None:   #获取数据包头信息
          header=re.search(re.compile(b"<.+?>"), data).group(0)


    if clients.has_key(clientA):   #clientA 存在的情况
        print('1111111111')
        print(' %s: is exist '%clientA + ', addr is:  %s:%s' %clients[clientA][0] )
        if clients.has_key(clientB):    #clientB 存在的情况
            print('--11--clientB %s exist !'%clientB)
            print('send to name is %s '%clientB + ',addr is:  %s:%s.'%clients[clientB][0])
            #s.sendto(header + b'data=' + b'%s 在线' % clientB, clients[clientA][0])
            s.sendto(b'%s' % data, clients[clientB][0])

        else:        #clientB 不存在的情况
            print('--11--clientB  %s not exist !' %clientB)
            s.sendto(header+b'data='+b'%s 不在线' % clientB, clients[clientA][0])


    elif  not clients.has_key(clientA):    #clientA 不存在的情况

        print('22222222 header is %s'% header)
        print(' %s is not exist' % clientA)
        s.sendto(header+b'data='+b'welcome %s' % clientA , addr)
        clients[clientA]=[addr,data]
        if clients.has_key(clientB):    #clientB 存在的情况
            print('--22--clientB %s exist !' %clientB)
            #s.sendto(header + b'data=' + b'%s 在线' % clientB, clients[clientA][0])
            s.sendto(b'%s' % data, clients[clientB][0])
        else:                  #clientB 不存在的情况
            print('--22--clientB not exist !')
            #print('welcome:%s ' % clientB)
            s.sendto(header+b'data='+b'%s 不在线' % clientB, clients[clientA][0])

