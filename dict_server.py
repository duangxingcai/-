"""
    1. 技术点

        并发模型（进程）和网络模型（tcp）
        确定细节功能，注册要注册的什么（name,passwd），注册后是否直接登录(name,passwd)
        一级界面，二级界面如何切换

    2. mysql数据库设计 dict
        words

    3. 结构设计，功能模块划分
        如何封装，客户端，服务端的工作流程，有几个功能模块

    4. 通信搭建

"""
"""
        处理客户请求
        注册，登录，退出，
        查询:单词 历史 注销
        协议： 登录 E    
              退出 Q
              注册 R    用户名密码 加密存储 注册后直接登录
              查询 F
           历史记录 H   最近前10条
              注销 C
        存储用户名： user表         name  passwd
      存储历史记录： history表      id name   word   time 
                  单词表：         id word mean
        
        cookie:
             import getpass 可以隐藏密码输入过程
                    getpass.getpass()
             import hashlib 加密模块
                    hash = hashlib.md5() #生成md5对象
                    参数:盐 （自定义的字节串）
                    
                    hash.update(passwd.encode()) # 进行加密处理 参数，密码转化为字节串
                    new_passwd = hash.hexdigest() # 得到转换后的密码
                        
     """

from dict_db import User
from socket import *
from multiprocessing import  Process
import signal,sys
from time import sleep


# 处理僵尸进程
signal.signal(signal.SIGCHLD,signal.SIG_IGN)

# 地址
ADDR= ('0.0.0.0',8888)
db = User('dict')

# 注册
def do_register(connfd,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.register(name,passwd):
        connfd.send(b'ok')
    else:
        connfd.send(b'fail')

# 登录
def do_enter(connfd,data):
    tmp = data.split(' ')
    name = tmp[1]
    passwd = tmp[2]
    if db.login(name, passwd):
        connfd.send(b'ok')
    else:
        connfd.send(b'fail')

# 查询单词
def do_find_word(connfd,data):
    tmp = data.split(' ')
    name = tmp[1]
    word = tmp[2]
    temp = db.find(word)

    if temp:
        db.insert_history(name,word)
        msg = "%s:%s"%(word,temp)
        connfd.send(msg.encode())

    else:
        connfd.send(b"fail")

# 查询历史
def do_find_history(connfd,data):
    name = data.split(' ')[1]
    r = db.find_history(name)
    for i in r:
        msg = '%s  %-16s  %s'%i
        connfd.send(msg.encode())
        sleep(0.1)
    connfd.send(b'##')

# 处理
def do_handle(connfd):
    # 创建游标
    db.create_cursor()
    while True:
        # 接收请求
        data = connfd.recv(1024).decode()
        if data[0] == 'R':
            do_register(connfd,data)
        elif data[0] == 'E':
            do_enter(connfd,data)
        elif data[0] == 'F':
            do_find_word(connfd,data)
        elif data[0] == 'H':
            do_find_history(connfd,data)
        elif not data or data[0] == 'Q':
            sys.exit('退出程序')


# 搭建网络模型
def main():
    # 创建套接字
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.bind(ADDR)
    sockfd.listen(5)

    # 循环等待客户端链接
    print("listen the port 8000")
    while True:
        try:
            connfd,addr = sockfd.accept()
            print("connect from ",addr)
        except Exception as e:
            print(e)
            continue
        except:
            sys.exit("服务器退出")

        # 创建子进程
        p = Process(target=do_handle,args=(connfd,))
        p.daemon = True
        p.start()


if __name__ == '__main__':
    main()
