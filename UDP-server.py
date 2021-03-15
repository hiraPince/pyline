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
#s.bind(('172.93.34.44', 9999))
s.bind(('172.28.32.140', 9999))
print('Bind UDP on 9999...')
addra = (0, 0)
addrb = (0, 0)
while True:
    # 接收数据:

    data, addr = s.recvfrom(1024)
    print('connect from %s:%s.' % addr)


    print('data is:     %s.' % data)
    if data == b'hello':
        print('--------- from %s:%s.' % addr)
        continue
    patternA = re.compile(b"(?<=<).+?(?= to)")#匹配查找clientA 名字
    clientA=re.search(patternA, data).group(0)

    patternB = re.compile(b"(?<=to ).+?(?=>)") #匹配查找clientB 名字
    clientB = re.search(patternB, data).group(0)
    print('clientA:%s  clientB:%s' % (clientA,clientB))

    patternheader=re.compile(b"(?<=<).+?(?=>)")
    if re.search(patternheader, data)!=None:
         header=re.search(patternheader, data).group(0)

    pattern_quit = re.compile(b"<!quit>")
    patterndata = re.compile(b"(?<=data=).+")   #匹配是否有有效数据

    if re.search(pattern_quit,data)!=None: #如果匹配到有quit,就执行退出操作并删除用户
        s.sendto(data, addr)
        if clients.has_key(clientA):
            del clients[clientA]
            print('delete %s'% clientA)


    elif re.search(patterndata,data)==None:
        continue


    elif clients.has_key(clientA):
        print('1111111111')
        print(' %s: is exist '%clientA + ', addr is:  %s:%s' %clients[clientA][0] )
        if clients.has_key(clientB):
            print('--11--clientB  exist !')
            print('send to name is %s '%clientB + ',addr is:  %s:%s.'%clients[clientB][0])
            s.sendto(b'%s' % data, clients[clientB][0])
        else:
            print('--11--clientB not exist !')
            s.sendto(b'%s not online!' % clientB, clients[clientA][0])


    elif  not clients.has_key(clientA):

        print('22222222')
        print(' %s is not exist ' % clientA)
        s.sendto(header+b'welcome %s' %clientA , addr)
        clients[clientA]=[addr,data]
        if clients.has_key(clientB):
            print('--22--clientB  exist !')
            s.sendto(b'%s' % data, clients[clientB][0])
        else:
            print('--22--clientB not exist !')
            #print('welcome:%s ' % clientB)
            s.sendto(header+b'%s not online!' % clientB, clients[clientA][0])

