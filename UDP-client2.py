import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
for data in [b'bbb222']:
    # 发送数据:
    #s.sendto(data, ('172.93.34.44', 9999))
    s.sendto(data, ('172.28.32.140', 9999))
    # 接收数据:
    print(s.recv(1024).decode('utf-8'))
s.close()