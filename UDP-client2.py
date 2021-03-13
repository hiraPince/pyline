# -*- coding: utf-8 -*-
import socket
from tkinter import *
import time, threading
import tkinter.messagebox as messagebox
#HOST ='172.93.34.44'
HOST = '172.28.32.140'
PORT = 9999
ADDR = (HOST, PORT)

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

def send():
    # 发送数据:
    #s.sendto(data, ('172.93.34.44', 9999))
    print('send data is: %s' %sendvar.get())
    s.sendto(sendvar.get().encode('utf-8'), ADDR)
    #s.sendto(sendvar.get().encode('utf-8'), ('172.93.34.44', 9999))
Button(root, text="send", command = send).pack()

def exit():
    s.sendto('quit'.encode('utf-8'),ADDR)
    ExitButton['text']='exit ok'
    root.destroy()

ExitButton=Button(root, text="exit", command = exit)
ExitButton.pack()
def recv_loop():
    global s
    print('thread %s is running...' % threading.current_thread().name)
    while True:
        #time.sleep(3)
        # 接收数据:
        rec=s.recv(1024).decode('utf-8')
        print('接收的数据是：%s'%rec )
        if rec == 'quit':
            break
        receivevar.set(rec)

s.sendto('hello'.encode('utf-8'), ('172.28.32.140', 9999))
print('thread %s is running...' % threading.current_thread().name)
t = threading.Thread(target=recv_loop, name='LoopThread')
t.start()
root.mainloop()
s.close()