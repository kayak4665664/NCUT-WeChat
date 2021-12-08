import socket
from _thread import *
from collections import defaultdict
import time
import datetime

class Server:
    def __init__(self):
        self.groups = defaultdict(list)  # 记录群聊
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 面向连接
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def accept_connections(self, ip, port):  # 接受连接
        self.ip = ip
        self.port = port
        self.server.bind((self.ip, int(self.port)))
        self.server.listen(5)  # 最大连接数
        while True:
            connection, address = self.server.accept()
            print(str(address[0]) + ':' + str(address[1]) + ' 连接成功！')
            start_new_thread(self.clientThread, (connection,))  # 创建客户端线程
        self.server.close()

    def clientThread(self, connection):  # 客户端线程
        user_id = connection.recv(1024).decode()  # 接收用户名
        group_id = connection.recv(1024).decode()  # 接收微信群
        connection.send('欢迎加入NCUT微信！'.encode())
        self.groups[group_id].append(connection)  # 添加记录
        while True:
            try:
                message = connection.recv(1024)  # 接收客户端数据
                if message:
                    if str(message.decode()) == 'FILE':  # 如果收到了 'FILE' 标记
                        self.broadcastFile(connection, group_id, user_id)  # 广播文件
                    else:
                        message_to_send = datetime.datetime.now().strftime('%H:%M ') + str(user_id) + ": " + message.decode()  # 添加时间信息
                        self.broadcast(message_to_send, connection, group_id)  # 广播消息
                else:
                    self.remove(connection, group_id)  # 强制断开连接
            except Exception as e:
                print(repr(e))
                print('已断开连接！')
                break

    def broadcastFile(self, connection, group_id, user_id):  # 广播文件
        file_name = connection.recv(1024).decode()  # 接收文件名
        lenOfFile = connection.recv(1024).decode()  # 接收文件长度
        for client in self.groups[group_id]:  # 向群聊中除发送者以外的客户端广播
            if client != connection:
                try:
                    client.send('FILE'.encode())  # 发送 'FILE' 标记
                    time.sleep(0.1)
                    client.send(file_name.encode())  # 发送文件名
                    time.sleep(0.1)
                    client.send(lenOfFile.encode())  # 发送文件长度
                    time.sleep(0.1)
                    client.send(str(datetime.datetime.now().strftime('%H:%M ') + str(user_id)).encode())  # 发送 时间与发送者用户名
                except:
                    client.close()
                    self.remove(client, group_id)
        total = 0
        while str(total) != lenOfFile:  # 当没有全部接收文件
            data = connection.recv(1024)
            total = total + len(data)
            for client in self.groups[group_id]:  # 向群聊中除发送者以外的客户端广播
                if client != connection:
                    try:
                        client.send(data)  # 发送接收到的部分文件
                    except:
                        client.close()
                        self.remove(client, group_id)

    def broadcast(self, message_to_send, connection, group_id):  # 广播消息
        print(message_to_send)
        for client in self.groups[group_id]:  # 向群聊中除发送者以外的客户端广播
            if client != connection:
                try:
                    client.send(message_to_send.encode())  # 发送消息
                except:
                    client.close()
                    self.remove(client, group_id)

    def remove(self, connection, group_id):  # 强制断开连接
        if connection in self.groups[group_id]:
            self.groups[group_id].remove(connection)


if __name__ == '__main__':
    ip = '10.54.62.73'
    port = 8000
    s = Server()
    s.accept_connections(ip, port)