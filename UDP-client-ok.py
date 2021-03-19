# -*- coding: utf-8 -*-
import socket
from tkinter import *
import time, threading
#import tkinter.messagebox as messagebox
import re

class chat:
    #HOST = '172.28.32.140'
    HOST ='172.93.34.44'
    PORT = 9999
    ADDR = (HOST, PORT)

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.root = Tk()
        self.root.title("Hi Chat")
        self.root.geometry('500x570')
        self.frm = Frame(self.root)

        #top
        self.frm_T = Frame(self.frm)

        #Entry for Master name
        self.master = StringVar()
        self.MasterEntry = Entry(self.frm_T, textvariable = self.master,width=8,font=('Verdana', 15),bg='turquoise')
        self.master.set("bbb")
        self.MasterEntry.pack(side=LEFT)

        # to
        Label(self.frm_T, text='to', width=8,font=('Arial', 12)).pack(side=LEFT)

        #client name
        self.client = StringVar()
        self.ClientEntry = Entry(self.frm_T, textvariable = self.client,width=8, font=('Verdana', 15),bg='silver')
        self.client.set("aaa")
        self.ClientEntry.pack(side=RIGHT)
        self.frm_T.pack()

        #middle
        self.frm_M = Frame(self.frm)
        self.t_show = Text(self.frm_M, width=20, height=15, font=('Verdana', 15))
        self.t_show.tag_config('m', foreground='turquoise')
        self.t_show.tag_config('c', foreground='silver')
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
        #self.SendButton.grid(row=0,column=0,sticky=EW,pady=3,padx=3)
        self.frm_MB.pack()
        self.frm.pack()

        #self.s.sendto('hello'.encode('utf-8'), ('172.28.32.140', 9999))
        self.s.sendto('hello'.encode('utf-8'), self.ADDR)
        print('thread %s is running...' % threading.current_thread().name)
        self.t = threading.Thread(target=self.recv_loop, name='LoopThread')
        self.t.start()
        #self.root.mainloop()


    # def send(self):
    #     print('test!')

    def send(self):
        # 发送数据:
        # s.sendto(data, ('172.93.34.44', 9999))
        if self.master.get()=='':
            self.t_show.insert(END,'请输入您的姓名！\n','m')
            return

        if self.client.get() == '':
            self.t_show.insert(END, '请输入对方姓名！\n','m')
            return

        tmpdata=b'<'+self.master.get().encode('utf-8')+b' to '+self.client.get().encode('utf-8')+b'>data='+self.chat.get().encode('utf-8')
        print('send data is: %s'% tmpdata)
        self.s.sendto(tmpdata, self.ADDR)
        # s.sendto(sendvar.get().encode('utf-8'), ('172.93.34.44', 9999))
        #self.t_show.insert(END, '  ' + self.chat.get() + ':' + self.master.get() + '\n','m')
        self.t_show.insert(END, self.chat.get() + '\n\n', 'm')
        self.chat.set('')

    def exit(self):
        self.s.sendto(b'<'+self.master.get().encode('utf-8')+b' to '+self.client.get().encode('utf-8')+b'><!quit>', self.ADDR)
        #self.s.sendto(b'<'+self.master.get().encode('utf-8')+b' to '+self.client.get().encode('utf-8')+b'><!quit>data=',self.ADDR)
        #self.s.sendto( '<!quit>data='.encode('utf-8'),self.ADDR)

        #self.ExitButton['text'] = '成功'
        time.sleep(1)  #一定要延时，否则没等消息过来终止线程，窗口退出会异常
        self.root.destroy()

    def recv_loop(self):
        print('thread %s is running...' % threading.current_thread().name)
        while True:
            # time.sleep(3)
            # 接收数据:
            #self.rec = self.s.recv(1024).decode('utf-8')
            self.rec = self.s.recv(1024)
            print('接收的数据是：%s' % self.rec.decode('utf-8'))
            #patternclient =   # 匹配查找client 名字8
            if re.search(re.compile(b"<!quit>"),self.rec) !=None:
                break
            if re.search(re.compile(b"(?<=<).+?(?= to)"), self.rec)!=None:
                clientname = re.search(re.compile(b"(?<=<).+?(?= to)"), self.rec).group(0).decode('utf-8')
                if re.search(re.compile(b"(?<=data=).+"),self.rec)!=None:
                    #带有谁发送提示
                    #self.t_show.insert(END,clientname+':'+re.search(re.compile(b"(?<=data=).+"),self.rec).group(0).decode('utf-8')+'\n','a')
                    self.t_show.insert(END,re.search(re.compile(b"(?<=data=).+"),self.rec).group(0).decode('utf-8')+'\n\n','c')

                    if self.master.get()!=clientname:   #防止自己跟自己聊天
                        self.client.set(clientname)




def main():
    d = chat()
    mainloop()
    d.s.close()


if __name__ == "__main__":
    main()