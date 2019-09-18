"""
        发送请求：
        注册，登录，退出，
        查单词，历史记录，注销
        协议： 登录 E
              注册 R
              退出 Q
              查询 F
           历史记录 H
              注销 C
    """
from socket import *
import sys
import getpass

# 服务器地址
ADDR = ('127.0.0.1',8888)

# 处理客户请求
def handle():
    pass

# 打印一级请求
def print_one_view():
    propert = """输入1 注册
输入2 登录
输入3 退出
    """
    print(propert)

# 打印二级请求
def print_two_view():
    propert = """输入4 查询
输入5 历史记录 
输入6 注销
        """
    print(propert)

# 注册
def do_register(s):
    while True:
        name = input("请输入您的昵称:")
        passwd = getpass.getpass("请输入您的密码:")
        passwd1 = getpass.getpass("Again:")
        if passwd != passwd1:
            print("两次密码不一致")
            continue
        if (' 'in name )or (' 'in  passwd):
            print("用户名名字或者密码不能有空格")
            continue

        # 发送请求
        msg = "R %s %s" % (name,passwd)
        s.send(msg.encode())

        data = s.recv(128).decode()
        if data == 'ok':
            print("注册成功")
            do_two_handle(s)
        else:
            print("注册失败")
        break
# 登录
def do_enter(s):
    while True:
        name = input("请输入您的名字:")
        passwd = input("请输入您的密码:")
        if (' 'in name) or (' ' in passwd):
            print("您输入的名字或者密码有空格 ")
            continue

        msg = 'E %s %s' % (name,passwd)
        s.send(msg.encode())
        data = s.recv(1024).decode()
        if data == "ok":
            print("登录成功")
            do_two_handle(s,name)
        else:
            print("登录失败")
        break

def do_two_handle(s,name):
    while True:
        print_two_view()
        msg = int(input("请输入您的选项："))
        if msg == 4:
            find_word(s,name)
        elif msg == 5:
            find_history(s,name)
        elif msg == 6:
            return

# 查单词
def find_word(s,name):
    while True:
        word = input("请输入您要查询的单词:")
        if word =="##":
            break
        msg = "F %s %s" % (name,word)
        s.send(msg.encode())

        data = s.recv(1024).decode()
        if data != "file":
            print(data)
        else:
            print("您查询的单词不存在")
        break

# 查看历史
def find_history(s,name):
    msg = "H "+name
    s.send(msg.encode())

    while True:
        data = s.recv(1024).decode()
        if data == '##':
            break
        print(data)

# 搭建网络
def main():
    s = socket()
    s.connect(ADDR)
    while True:
        print_one_view()
        commend = int(input("请输入您的选项："))
        if commend == 1:
            do_register(s)
        elif commend == 2:
            do_enter(s)
        elif commend == 3:
            s.send(b'Q')
            sys.exit()

if __name__ == '__main__':
    main()
