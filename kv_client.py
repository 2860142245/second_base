from socket import *

HOST = 'localhost'
PORT = 5678
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket(AF_INET, SOCK_STREAM)

a = 0
try:
    tcpCliSock.connect(ADDR)
except Exception as e:
    print('服务器连接失败,错误原因：%s' % e)
    a = -1

if a == 0:
    while 1:
        command = input('请输入命令：\n')
        if not command:
            break
        tcpCliSock.send(command.encode('utf-8'))
        data = tcpCliSock.recv(BUFSIZ)
        print(data.decode('utf-8'))

print('goodbye ~.~')
tcpCliSock.close()
