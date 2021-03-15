# # -*- coding: utf-8 -*-
# import socket
# from tkinter import *
# import time, threading
# import tkinter.messagebox as messagebox
#
# class chat:
#     HOST = '172.28.32.140'
#     PORT = 9999
#     ADDR = (HOST, PORT)
#
#     def __init__(self):
#         self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#         self.root = Tk()
#         self.root.title("Hi Chat")
#         self.root.geometry('380x470')
#         self.frm = Frame(self.root)
#
#         #top
#         self.frm_T = Frame(self.frm)
#
#         #Entry for Master name
#         self.master = StringVar()
#         self.MasterEntry = Entry(self.frm_T, textvariable = self.master,width=8,font=('Verdana', 15))
#         self.master.set("aaa")
#         self.MasterEntry.pack(side=LEFT)
#
#         # to
#         Label(self.frm_T, text='to', width=8,font=('Arial', 12)).pack(side=LEFT)
#
#         #client name
#         self.client = StringVar()
#         self.ClientEntry = Entry(self.frm_T, textvariable = self.client,width=8, font=('Verdana', 15))
#         self.client.set("bbb")
#         self.ClientEntry.pack(side=RIGHT)
#         self.frm_T.pack()
#
#         #middle
#         self.frm_M = Frame(self.frm)
#         self.t_show = Text(self.frm_M, width=20, height=15, font=('Verdana', 15))
#         self.t_show.insert('1.0', '')
#         self.t_show.pack(fill=BOTH)
#         self.chat = StringVar()
#         self.ChatEntry = Entry(self.frm_M, textvariable = self.chat,width=8, font=('Verdana', 15))
#         self.chat.set("Enter message")
#         self.ChatEntry.pack(fill=BOTH)
#         self.frm_M.pack()
#
#         #bottom
#         self.frm_MB = Frame(self.frm)
#         self.SendButton=Button(self.frm_MB, text="发送",width=14, command=self.send).pack(side=LEFT)
#         self.ExitButton=Button(self.frm_MB, text="退出", command=self.exit).pack(side=RIGHT)
#         self.frm_MB.pack()
#         self.frm.pack()
#
#         self.s.sendto('hello'.encode('utf-8'), ('172.28.32.140', 9999))
#         print('thread %s is running...' % threading.current_thread().name)
#         self.t = threading.Thread(target=self.recv_loop, name='LoopThread')
#         self.t.start()
#         #self.root.mainloop()
#
#
#     # def send(self):
#     #     print('test!')
#
#     def send(self):
#         # 发送数据:
#         # s.sendto(data, ('172.93.34.44', 9999))
#         print('send data is: %s' % self.chat.get())
#         self.s.sendto(self.master.get().encode('utf-8')+b'to'+self.client.get().encode('utf-8')+self.chat.get().encode('utf-8'), self.ADDR)
#         # s.sendto(sendvar.get().encode('utf-8'), ('172.93.34.44', 9999))
#         self.t_show.insert(END, '  ' + self.chat.get() + ':' + self.master.get() + '\n')
#
#     def exit(self):
#         self.s.sendto(self.master.get().encode('utf-8')+b'to'+self.client.get().encode('utf-8')+'quit'.encode('utf-8'), self.ADDR)
#         #self.ExitButton['text'] = '成功'
#         self.root.destroy()
#
#     def recv_loop(self):
#         print('thread %s is running...' % threading.current_thread().name)
#         while True:
#             # time.sleep(3)
#             # 接收数据:
#             self.rec = self.s.recv(1024).decode('utf-8')
#             print('接收的数据是：%s' % self.rec)
#             if self.rec == 'quit':
#                 break
#             self.t_show.insert(END,self.client.get()+':'+self.rec+'\n')
#
#
#
# def main():
#     d = chat()
#     mainloop()
#     d.s.close()
#
#
# if __name__ == "__main__":
#     main()

# -*- coding: utf-8 -*-
import socket
from tkinter import *
import time, threading
#import tkinter.messagebox as messagebox
import re

class chat:
    HOST = '172.28.32.140'
    PORT = 9999
    ADDR = (HOST, PORT)

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.root = Tk()
        self.root.title("Hi Chat")
        self.root.geometry('380x470')
        self.frm = Frame(self.root)

        #top
        self.frm_T = Frame(self.frm)

        #Entry for Master name
        self.master = StringVar()
        self.MasterEntry = Entry(self.frm_T, textvariable = self.master,width=8,font=('Verdana', 15))
        self.master.set("bbb")
        self.MasterEntry.pack(side=LEFT)

        # to
        Label(self.frm_T, text='to', width=8,font=('Arial', 12)).pack(side=LEFT)

        #client name
        self.client = StringVar()
        self.ClientEntry = Entry(self.frm_T, textvariable = self.client,width=8, font=('Verdana', 15))
        self.client.set("aaa")
        self.ClientEntry.pack(side=RIGHT)
        self.frm_T.pack()

        #middle
        self.frm_M = Frame(self.frm)
        self.t_show = Text(self.frm_M, width=20, height=15, font=('Verdana', 15))
        self.t_show.insert('1.0', '')
        self.t_show.pack(fill=BOTH)
        self.chat = StringVar()
        self.ChatEntry = Entry(self.frm_M, textvariable = self.chat,width=8, font=('Verdana', 15))
        self.chat.set("Enter message")
        self.ChatEntry.pack(fill=BOTH)
        self.frm_M.pack()

        #bottom
        self.frm_MB = Frame(self.frm)
        self.SendButton=Button(self.frm_MB, text="发送",width=14, command=self.send).pack(side=LEFT)
        self.ExitButton=Button(self.frm_MB, text="退出", command=self.exit).pack(side=RIGHT)
        self.frm_MB.pack()
        self.frm.pack()

        self.s.sendto('hello'.encode('utf-8'), ('172.28.32.140', 9999))
        print('thread %s is running...' % threading.current_thread().name)
        self.t = threading.Thread(target=self.recv_loop, name='LoopThread')
        self.t.start()
        #self.root.mainloop()


    # def send(self):
    #     print('test!')

    def send(self):
        # 发送数据:
        # s.sendto(data, ('172.93.34.44', 9999))
        print('send data is: %s' % self.chat.get())
        self.s.sendto(b'<'+self.master.get().encode('utf-8')+b' to '+self.client.get().encode('utf-8')+b'>data='+self.chat.get().encode('utf-8'), self.ADDR)
        # s.sendto(sendvar.get().encode('utf-8'), ('172.93.34.44', 9999))
        self.t_show.insert(END, '  ' + self.chat.get() + ':' + self.master.get() + '\n')

    def exit(self):
        self.s.sendto(b'<'+self.master.get().encode('utf-8')+b' to '+self.client.get().encode('utf-8')+b'><!quit>', self.ADDR)
        #self.ExitButton['text'] = '成功'
        time.sleep(1)
        self.root.destroy()

    def recv_loop(self):
        print('thread %s is running...' % threading.current_thread().name)
        while True:
            # time.sleep(3)
            # 接收数据:
            #self.rec = self.s.recv(1024).decode('utf-8')
            self.rec = self.s.recv(1024)
            print('接收的数据是：%s' % self.rec.decode('utf-8'))
            #patternclient =   # 匹配查找client 名字
            if re.search(re.compile(b"(?<=<).+?(?= to)"), self.rec)!=None:
                client = re.search(re.compile(b"(?<=<).+?(?= to)"), self.rec).group(0).decode('utf-8')
            if re.search(re.compile(b"<!quit>"),self.rec) !=None:
                break
            if re.search(re.compile(b"(?<=data=).+"),self.rec)!=None:
                self.t_show.insert(END,client+':'+re.search(re.compile(b"(?<=data=).+"),self.rec).group(0).decode('utf-8')+'\n')
                self.client.set(client)




def main():
    d = chat()
    mainloop()
    d.s.close()


if __name__ == "__main__":
    main()