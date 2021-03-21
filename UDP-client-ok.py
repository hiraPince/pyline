# -*- coding: utf-8 -*-
import socket
from tkinter import *
import time, threading
# import tkinter.messagebox as messagebox
import re
from tkinter.scrolledtext import ScrolledText


class chat:
    # HOST = '172.28.32.140'
    HOST = '172.93.34.44'
    PORT = 9999
    ADDR = (HOST, PORT)

    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        # -----------------------------------------------------------------------------
        self.root = Tk()

        #主聊天人窗口
        self.master = StringVar()
        self.MasterEntry = Entry(self.root, textvariable=self.master, width=8, font=('Verdana', 15), bg='turquoise',highlightcolor='red')
        self.master.set("bbb")

        # to
        self.labelto = Label(self.root, text=' to ', width=8, font=('Arial', 12))

        # 客户聊天人窗口
        self.client = StringVar()
        self.ClientEntry = Entry(self.root, textvariable=self.client, width=8, font=('Verdana', 15), bg='yellowgreen')
        self.client.set("aaa")

        # 聊天窗口
        self.t_show = ScrolledText(self.root, width=40, height=30, font=('Verdana', 12), background='#ffffff',state=DISABLED)
        self.t_show.tag_config('m', foreground='turquoise')
        self.t_show.tag_config('c', foreground='yellowgreen')
        #self.t_show.insert('1.0', '')

        # 聊天输入窗口
        self.chat = StringVar()
        self.ChatEntry = Entry(self.root, textvariable=self.chat, width=25, font=('Verdana', 15), foreground='gray')
        self.chat.set("Enter message")
        self.ChatEntry.bind('<Key-Return>', self.enter_send)  # bind enter键按下事件
        self.ChatEntry.bind('<FocusIn>', self.chat_cursor_enter)  # bind 光标进入事件
        self.ChatEntry.bind('<FocusOut>', self.chat_cursor_leave)  # bind 光标离开事件

        #发送和退出按钮
        self.SendButton = Button(self.root, text="发送", width=16, command=self.send)
        self.ExitButton = Button(self.root, text="退出", width=8, command=self.exit, padx=5)

        #图片显示
        self.photo = PhotoImage(file='p3m.png')
        self.labelimage = Label(image=self.photo)
        self.labelimage.image = self.photo

        self.labelimage.grid(row=1, column=3, columnspan=2, rowspan=1, sticky=W + E + N + S)
        self.MasterEntry.grid(row=0, column=0)
        self.labelto.grid(row=0, column=1)
        self.ClientEntry.grid(row=0, column=2)
        self.t_show.grid(row=1, column=0, columnspan=3, rowspan=1, sticky=W + E + N + S, padx=10, pady=10)
        self.ChatEntry.grid(row=2, column=0, columnspan=2, padx=10, pady=10)
        self.SendButton.grid(row=2, column=2)
        self.ExitButton.grid(row=2, column=3, columnspan=2)

        # self.s.sendto('hello'.encode('utf-8'), ('172.28.32.140', 9999))
        self.s.sendto('hello'.encode('utf-8'), self.ADDR)
        print('thread %s is running...' % threading.current_thread().name)
        self.t = threading.Thread(target=self.recv_loop, name='LoopThread')
        self.t.setDaemon(True)  # 设置为守护线程，守护进程有个好处就是主进程结束，自动结束，解决之前窗口强制退出报错问题
        self.t.start()

        # self.root.mainloop()

    def chat_cursor_enter(self, event):
        if self.chat.get() == 'Enter message' or self.chat.get() == '':
            self.chat.set("")
        self.ChatEntry['foreground'] = 'black'  # 重新设置Entry字体颜色

    def chat_cursor_leave(self, event):
        self.ChatEntry['foreground'] = 'gray'  # 重新设置Entry字体颜色
        if self.chat.get() == 'Enter message' or self.chat.get() == '':  # 如果输入框里面有输入内容则不使用默认语句覆盖
            self.chat.set("Enter message")

    # def send(self):
    #     print('test!')
    def enter_send(self, event):
        print('按下Enter: ' + event.char)
        self.send()

    def send(self):
        # 发送数据:
        # s.sendto(data, ('172.93.34.44', 9999))
        if self.master.get() == '':
            self.t_show.config(state=NORMAL)     #让消息显示框可以正常输入
            self.t_show.insert(END, '请输入您的姓名！\n', 'm')
            self.t_show.config(state=DISABLED)  #让消息显示框禁止输入
            return

        if self.client.get() == '':
            self.t_show.config(state=NORMAL)  # 让消息显示框可以正常输入
            self.t_show.insert(END, '请输入对方姓名！\n', 'm')
            self.t_show.config(state=DISABLED)  # 让消息显示框禁止输入
            return
        # self.DefaultMaster=self.master.get()
        # self.DefaultClient=self.master.get()

        tmpdata = b'<' + self.master.get().encode('utf-8') + b' to ' + self.client.get().encode(
            'utf-8') + b'>data=' + self.chat.get().encode('utf-8')
        print('send data is: %s' % tmpdata)
        self.s.sendto(tmpdata, self.ADDR)
        # s.sendto(sendvar.get().encode('utf-8'), ('172.93.34.44', 9999))
        # self.t_show.insert(END, '  ' + self.chat.get() + ':' + self.master.get() + '\n','m')
        self.t_show.config(state=NORMAL)  # 让消息显示框可以正常输入
        self.t_show.insert(END, self.chat.get() + '\n\n', 'm')
        self.t_show.config(state=DISABLED)  # 让消息显示框禁止输入
        self.t_show.see(END)  # 让滚动条一直处于最下端
        self.chat.set('')

    def exit(self):
        tpdata=b'<' + self.master.get().encode('utf-8') + b' to ' + self.client.get().encode('utf-8') + b'><!quit>'
        print('exit send :%s' %tpdata)
        self.s.sendto(tpdata,self.ADDR)
        # self.s.sendto(b'<'+self.master.get().encode('utf-8')+b' to '+self.client.get().encode('utf-8')+b'><!quit>data=',self.ADDR)
        # self.s.sendto( '<!quit>data='.encode('utf-8'),self.ADDR)

        # self.ExitButton['text'] = '成功'
        #time.sleep(1)  # 一定要延时，否则没等消息过来终止线程，窗口退出会异常
        self.root.destroy()

    def recv_loop(self):
        print('thread %s is running...' % threading.current_thread().name)
        self.s.settimeout(2)
        while True:
            # time.sleep(3)
            # 接收数据:
            # self.rec = self.s.recv(1024).decode('utf-8')
            try:
                self.rec = self.s.recv(1024)
                # break
            except socket.timeout:
                print('-------超时，重新接收--------')
                continue
            print('接收的数据是：%s' % self.rec.decode('utf-8'))
            # patternclient =   # 匹配查找client 名字8
            if re.search(re.compile(b"<!quit>"), self.rec) != None:
                break
            if re.search(re.compile(b"(?<=<).+?(?= to)"), self.rec) != None:
                clientname = re.search(re.compile(b"(?<=<).+?(?= to)"), self.rec).group(0).decode('utf-8')
                if re.search(re.compile(b"(?<=data=).+"), self.rec) != None:
                    # 带有谁发送提示
                    # self.t_show.insert(END,clientname+':'+re.search(re.compile(b"(?<=data=).+"),self.rec).group(0).decode('utf-8')+'\n','a')
                    self.t_show.config(state=NORMAL)  # 让消息显示框可以正常输入
                    self.t_show.insert(END, re.search(re.compile(b"(?<=data=).+"), self.rec).group(0).decode('utf-8') + '\n\n', 'c')
                    self.t_show.config(state=DISABLED)  # 让消息显示框禁止输入
                    self.t_show.see(END)  # 让滚动条一直处于最下端
                    if self.master.get() != clientname:  # 防止自己跟自己聊天
                        self.client.set(clientname)


def main():
    d = chat()
    mainloop()
    d.s.close()


if __name__ == "__main__":
    main()
