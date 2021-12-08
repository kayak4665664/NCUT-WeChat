import socket
import tkinter as tk
from tkinter import filedialog
import time
import threading
import os
import datetime
from tkmacosx import Button

ip = '10.251.245.239'
port = 8000


class Client:
    def __init__(self, ip, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((ip, port))  # 连接到服务器
        self.window = tk.Tk()  # 创建主界面
        self.window.withdraw()  # 暂时移除主界面
        self.login = tk.Toplevel()  # 创建登录界面
        self.login.title('NCUT微信')  # 登录界面标题
        self.login.resizable(width=False, height=False)
        self.login.configure(width=400, height=350)
        self.lable = tk.Label(self.login, text='由 北方工业大学 计XX-X XXX 制作',
                              justify=tk.RIGHT, font='Helvetica 13 bold')
        self.lable.place(relheight=0.15, relx=0.2, rely=0.07)
        self.userLabel = tk.Label(
            self.login, text='用户名: ', font='Helvetica 15 bold')
        self.userLabel.place(relheight=0.2, relx=0.1, rely=0.25)
        self.userEntry = tk.Entry(self.login, font='Helvetica 15')  # 用户名输入框
        self.userEntry.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.30)
        self.userEntry.focus()
        self.groupLabel = tk.Label(
            self.login, text='微信群: ', font='Helvetica 15 bold')
        self.groupLabel.place(relheight=0.2, relx=0.1, rely=0.40)
        self.groupEntry = tk.Entry(self.login, font='Helvetica 15')  # 微信群输入框
        self.groupEntry.place(relwidth=0.4, relheight=0.1, relx=0.35, rely=0.45)
        self.enterButton = Button(self.login, text='登录', font='Helvetica 15 bold', fg='#F1F1F1', bg='#2BA245',
                         command=lambda: self.enter(self.userEntry.get(), self.groupEntry.get()))  # 登录按钮
        self.enterButton.place(relx=0.35, rely=0.62)
        self.window.mainloop()  # 启动界面

    def enter(self, username, group_id=0):  # 登录到服务器
        self.name = username
        self.server.send(str.encode(username))
        time.sleep(0.1)
        self.server.send(str.encode(group_id))
        self.login.destroy()  # 销毁登录界面
        self.interface()  # 进入主界面
        rcv = threading.Thread(target=self.receive)  # 创建接收服务器消息线程
        rcv.start()

    def interface(self):  # 主界面GUI
        self.window.deiconify()  # 重新显示主界面
        self.window.title('NCUT微信')  # 主界面标题
        self.window.resizable(width=False, height=False)
        self.window.configure(width=650, height=600)
        self.head = tk.Label(
            self.window, text=self.name, font='Helvetica 25 bold', pady=5)  # 顶部
        self.head.place(relwidth=1)
        self.line = tk.Label(self.window, width=580)
        self.line.place(relwidth=1, rely=0.07, relheight=0.012)
        self.text = tk.Text(self.window, width=20, height=2,
                            font='Helvetica 15 bold', padx=5, pady=5)  # 聊天内容显示
        self.text.place(relheight=0.745, relwidth=1, rely=0.08)
        self.labelBottom = tk.Label(self.window, height=80)
        self.labelBottom.place(relwidth=1, rely=0.8)
        self.msgEntry = tk.Entry(self.labelBottom, font='Helvetica 15')  # 消息输入框
        self.msgEntry.place(relwidth=0.88, relheight=0.03,
                            rely=0.008, relx=0.011)
        self.msgEntry.focus()
        self.msgButton = Button(self.labelBottom, text='发送', font='Helvetica 15 bold', width=10,
                                fg='#F1F1F1', bg='#2BA245', command=lambda: self.sendButton(self.msgEntry.get()))  # 发送按钮
        self.msgButton.place(relx=0.90, rely=0.008,
                             relheight=0.03, relwidth=0.10)
        self.labelFile = tk.Label(self.window, height=70)
        self.labelFile.place(relwidth=1, rely=0.9)
        self.fileLocation = tk.Label(
            self.labelFile, text='文件传输助手', font='Helvetica 15 bold')
        self.fileLocation.place(
            relwidth=0.78, relheight=0.03, rely=0.008, relx=0.011)
        self.browse = Button(self.labelFile, text='文件', font='Helvetica 15 bold',
                             width=10, fg='#F1F1F1', bg='#2BA245', command=self.browseFile)  # 文件按钮
        self.browse.place(relx=0.80, rely=0.008, relheight=0.03, relwidth=0.10)
        self.fileButton = Button(self.labelFile, text='传输', font='Helvetica 15 bold',
                                  width=10, fg='#F1F1F1', bg='#2BA245', command=self.sendFile)  # 传输文件按钮
        self.fileButton.place(relx=0.90, rely=0.008,
                               relheight=0.03, relwidth=0.10)
        self.text.config(cursor='arrow')
        scrollbar = tk.Scrollbar(self.text)  # 界面滚动条
        scrollbar.place(relheight=1, relx=0.974)
        scrollbar.config(command=self.text.yview)
        self.text.config(state=tk.DISABLED)

    def browseFile(self):  # 选取文件
        self.file_name = filedialog.askopenfilename(
            initialdir='/', title='文件')
        self.fileLocation.configure(text=self.file_name)

    def sendFile(self):  # 向服务器发送文件
        self.server.send('FILE'.encode())  # 发送 'FILE' 标记
        time.sleep(0.1)
        self.server.send(str(os.path.basename(self.file_name)).encode())
        time.sleep(0.1)  # 发送文件名
        self.server.send(str(os.path.getsize(self.file_name)).encode())
        time.sleep(0.1)  # 发送文件长度
        file = open(self.file_name, 'rb')  # 读取文件
        data = file.read(1024)
        while data:
            self.server.send(data)  # 每次发送1024长度
            data = file.read(1024)
        self.text.config(state=tk.DISABLED)
        self.text.config(state=tk.NORMAL)
        self.text.tag_add('tag', tk.END)
        self.text.tag_config('tag', foreground='#2BA245')
        if self.file_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
            self.text.insert(tk.END, datetime.datetime.now().strftime(
                '%H:%M ') + '你发送了图片: ' + str(os.path.basename(self.file_name)) + '\n\n', 'tag')
        else:
            self.text.insert(tk.END, datetime.datetime.now().strftime(
                '%H:%M ') + '你发送了文件: ' + str(os.path.basename(self.file_name)) + '\n\n', 'tag')
        self.text.config(state=tk.DISABLED)
        self.text.see(tk.END)

    def sendButton(self, msg):  # 发送消息按钮
        self.text.config(state=tk.DISABLED)
        self.msg = msg
        self.msgEntry.delete(0, tk.END)
        s = threading.Thread(target=self.sendMessage)  # 发送消息线程
        s.start()

    def receive(self):  # 接收服务器消息
        while True:
            try:
                message = self.server.recv(1024).decode()
                if str(message) == 'FILE':  # 如果收到了 'FILE' 标记
                    file_name = self.server.recv(1024).decode()  # 接收文件名
                    lenOfFile = self.server.recv(1024).decode()  # 接收文件长度
                    send_user = self.server.recv(1024).decode()  # 接收发送者用户名
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    total = 0
                    with open(file_name, 'wb') as file:
                        while str(total) != lenOfFile:
                            data = self.server.recv(1024)
                            total = total + len(data)
                            file.write(data)
                    self.text.config(state=tk.DISABLED)
                    self.text.config(state=tk.NORMAL)
                    if file_name.lower().endswith(('.bmp', '.dib', '.png', '.jpg', '.jpeg', '.pbm', '.pgm', '.ppm', '.tif', '.tiff')):
                        self.text.insert(tk.END, str(
                            send_user) + '发送了图片: ' + file_name + ' ，请在新窗口中预览\n\n')
                        time.sleep(2)
                        os.system('open ' + file_name)
                    else:
                        self.text.insert(tk.END, str(
                            send_user) + '发送了文件: ' + file_name + ' ，已自动下载至文件夹\n\n')
                    self.text.config(state=tk.DISABLED)
                    self.text.see(tk.END)
                else:
                    self.text.config(state=tk.DISABLED)
                    self.text.config(state=tk.NORMAL)
                    self.text.insert(tk.END, message+'\n\n')  # 直接在界面中显示消息
                    self.text.config(state=tk.DISABLED)
                    self.text.see(tk.END)
            except:
                print('发生错误!')
                self.server.close()
                break

    def sendMessage(self):  # 向服务器发送消息
        self.text.config(state=tk.DISABLED)
        while True:
            self.server.send(self.msg.encode())
            self.text.config(state=tk.NORMAL)
            self.text.tag_add('tag', tk.END)
            self.text.tag_config('tag', foreground='#2BA245')
            self.text.insert(tk.END, datetime.datetime.now().strftime(
                '%H:%M ') + '你: ' + self.msg + '\n\n', 'tag')
            self.text.config(state=tk.DISABLED)
            self.text.see(tk.END)
            break


if __name__ == '__main__':
    c = Client(ip, port)