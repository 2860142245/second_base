import re
import threading
import requests
from socket import *


def ser_oneClient(a_tcpclisock):
    n = 0  # 计数器
    through = '-1'
    while 1:
        n += 1
        data = a_tcpclisock.recv(BUFSIZ)
        print(n)
        print('receive successfully')
        if not data:
            break
        command = data.decode('utf-8')
        result = parse(command)
        send_data = ' '
        if result == -1:
            send_data = 'please give a correct command'
        elif result[0] == 'SET':
            send_data = set_key(result[1], result[2])
        elif result[0] == 'GET':
            send_data = get_key(result[1])
        elif result[0] == 'AUTH':
            through = login(result[1], result[2])
            send_data = through
        elif result[0] == 'URL':
            if through == '0':
                with open('dict_base.txt', 'r+') as f:
                    for i in f.readlines():
                        s = re.match(result[1]+':(.*)', i)
                        if s:
                            send_data = get_key(result[1])
                            break
                    else:
                        file_size = str(get_urlfile_size(result[2]))
                        set_key(result[1], file_size)
                        send_data = file_size
        a_tcpclisock.send(send_data.encode('utf-8'))
        print('send successfully')
        print('wait next command...\n')
    print('one thread end\n')
    a_tcpclisock.close()


def parse(command):  # command必须为字符串
    result1 = re.match('SET (.*?) (.*)', command)  # 键没有空格，值可以有空格
    if result1:
        key = result1.group(1)
        value = result1.group(2)
        return 'SET', key, value
    else:
        result2 = re.match('GET (.*)', command)
        if result2:
            key = result2.group(1)
            return 'GET', key
        else:
            result3 = re.match('AUTH (.*?) (.*)', command)
            if result3:
                input_username = result3.group(1)
                input_password = result3.group(2)
                return 'AUTH', input_username, input_password
            else:
                result4 = re.match('URL (.*?) (.*)', command)
                if result4:
                    name = result4.group(1)
                    url = result4.group(2)
                    return 'URL', name, url
                else:
                    return -1


def set_key(key, value):
    with open('dict_base.txt', 'r+') as f:
        for i in f.readlines():
            result = re.match(key+':(.*)', i)
            if result:
                change_dict(result.group(), key+':'+value)
                break
        else:
            f.write(key+':'+value+'\n')
    return ' '


def change_dict(old_kav, new_kav):
    with open('dict_base.txt', 'r') as old_f:
        with open('dict_base.txt', 'r+') as new_f:
            for i in old_f.readlines():
                if format_str(i) == old_kav:
                    new_f.write(new_kav+'\n')
                    continue
                new_f.write(i)
            new_f.truncate()


def get_key(key):
    with open('dict_base.txt', 'r') as f:
        for i in f.readlines():
            result = re.match(key+':(.*)', i)
            if result:
                return result.group(1)
        else:
            return ' '


def login(username, password):
    through = 0
    with open('auth.conf.txt', 'r') as f:
        for i in f.readlines():
            result = re.match(username+':'+password, i)  # 密码中可能出现':'
            if result:
                through = 1
                break
    if through:
        return '0'
    return '-1'


def get_urlfile_size(url):
    response = requests.get(url)
    file_size = len(response.content)
    return file_size


def format_str(a_str):
    if a_str[-1] == '\n':
        return a_str[:-1]
    return a_str


# 创建套接字：
HOST = 'localhost'
PORT = 5678
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(ADDR)
tcpSerSock.listen(5)


# 创建线程：
print('wait connection...')
while 1:
    tcpclisock_tmp, addr = tcpSerSock.accept()
    print('connect successfully')
    print('wait next connection...\n')
    t1 = threading.Thread(target=ser_oneClient, args=(tcpclisock_tmp,))
    t1.start()

print('all end')
tcpSerSock.close()

