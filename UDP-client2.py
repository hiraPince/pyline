import socket
from tkinter import *
import time, threading
import tkinter.messagebox as messagebox
stop=0
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

root = Tk()
root.title("Hi chat!")
root.geometry('300x200')




sendvar = StringVar()
send = Entry(root, textvariable = sendvar)
sendvar.set("send message!")
send.pack()

receivevar = StringVar()
receive = Entry(root, textvariable = receivevar)
receivevar.set("receive message!")
receive.pack()

def sendmessage():
    # 发送数据:
    #s.sendto(data, ('172.93.34.44', 9999))
    print('send data is: %s' %sendvar.get())
    s.sendto(sendvar.get().encode('utf-8'), ('172.28.32.140', 9999))
    #s.sendto(sendvar.get().encode('utf-8'), ('172.93.34.44', 9999))
Button(root, text="send", command = sendmessage).pack()

def loop():
    global stop
    global s
    print('thread %s is running...' % threading.current_thread().name)
    while True:
        time.sleep(1)
        # 接收数据:
        rec=s.recv(1024).decode('utf-8')
        print('接收的数据是：%s'%rec )
        receivevar.set(rec)
    return
s.sendto('hello'.encode('utf-8'), ('172.28.32.140', 9999))
print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=loop, name='LoopThread')
t.start()
#t.join()

root.mainloop()
#t.join(2)
t.stop()
time.sleep(6)
s.close()