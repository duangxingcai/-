"""
    注册，登录
"""
import pymysql
db = pymysql.connect(user="root",passwd='123456',database="stu",charset="utf8")
cur = db.cursor()

class Registe:
    def __init__(self,user,passwd):
        self.user = user
        self.passwd = passwd

    def find_user(self):
        sql = "select * from user where usa;"
        for i in sql:
            if i == user:
                return False
        return True

    def main(self):
        if self.find_user():
            sql1 = "insert into user values(%s,%s)"
            cur.execute(sql1,[self.user,self.passwd])
            return True



if __name__ == '__main__':
    while True:
        user = input("请输入您的用户名：")
        passwd = input("请输入您的密码：")
        r01 = Registe(user,passwd)
        item = r01.main()
        if item:
            print("注册成功")
            break
        else:
            print("用户名存在")