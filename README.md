# NCUT-WeChat
A chat room using sockets. It supports private chat and group chat. Users can send or receive text, emoji, pictures and files.  
一个使用套接字的聊天室，它支持私聊和群聊。用户可以发送或接收文本、表情、图片和文件。

Time: 2021 Spring Semester

## Details 细节
1. Using Python Socket, the GUI uses the Python tkinter library. 使用 Python Socket，图形界面使用 Python tkinter 库。
2. The server is deployed on one machine, the client is located on other machines, and multiple clients can log in at the same time. 将服务器部署在一台机器上，客户端位于其他机器，多个客户端可以同时登录。
3. Implemented private chat between 2 clients. 实现了 2 个客户端之间的私聊。
4. Group chat among multiple clients is implemented by using the server's broadcast function. 通过使用服务器的广播功能实现了多个客户端之间的群聊。
5. The communication between different group chats is independent of each other and does not interfere with each other. 不同群聊之间的通讯互相独立，互不干扰。
6. Support sending text, emoji, pictures and files. 可以发送文字、表情、图片和文件。