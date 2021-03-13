# -*- coding: utf-8 -*-
import socket
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
    print('Received from %s:%s.' % addr)

    clientA=data[:3]
    clientB=data[5:8]
    print('clientA:%s  clientB:%s' % (data[:3],data[5:8]))
    if data[8:12] == b'quit':
        s.sendto(data[8:12], addr)
        del clients[clientA]
    elif clients.has_key(clientA):
        print('1111111111')
        print(' %s: is exist '%clientA + ', addr is:  %s:%s' %clients[clientA][0] )
        if clients.has_key(clientB):
            print('--11--clientB  exist !')
            print('send to name is %s '%clientB + ',addr is:  %s:%s.'%clients[clientB][0])
            s.sendto(b'%s' % data[8:], clients[clientB][0])
        else:
            print('--11--clientB not exist !')
            s.sendto(b'%s not online!' % clientB, clients[clientA][0])
    elif  not clients.has_key(clientA):
        print('22222222')
        print(' %s is not exist ' % clientA)
        s.sendto(b'welcome %s' %clientA , addr)
        clients[clientA]=[addr,data]
        #clients[clientA][0]= addr
        #clients[clientA][1]= data
        if clients.has_key(clientB):
            print('--22--clientB  exist !')
            s.sendto(b'%s' % data[8:], clients[clientB][0])
        else:
            print('--22--clientB not exist !')
            #print('welcome:%s ' % clientB)
            s.sendto(b'%s not online!' % clientB, clients[clientA][0])

