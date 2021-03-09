import socket
global a
global b
a=''
b=''
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# 绑定端口:
#s.bind(('172.93.34.44', 9999))
s.bind(('172.28.32.140', 9999))
print('Bind UDP on 9999...')
while True:
    # 接收数据:
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s.' % addr)
    print('data[0:3]:%s '%data[:3])
    if data[:3] == b'aaa':
        length=len(data)
        a += data[3:length].decode('utf-8')
        print('Received a len: %d is: %s '%(length ,a))
        if len(b)!=0:
            s.sendto(b'Hello, %s' % b.encode('utf-8'), addr)
            b=''
        else:
            s.sendto(b'Hello, %s!' % 'No message'.encode('utf-8'), addr)

    if data[:3] == b'bbb':
        length=len(data)
        b += data[3:length].decode('utf-8')
        print('Received b len: %d is: %s '%(length ,b))
        if len(a)!=0:
            s.sendto(b'Hello, %s' % a.encode('utf-8'), addr)
            a=''
        else:
            s.sendto(b'Hello, %s!' % 'No message'.encode('utf-8'), addr)
    #s.sendto(b'Hello, %s!' % data, addr)