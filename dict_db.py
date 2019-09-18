"""
   编写一个程序,模拟用户注册,登录的数据库行为

   stu->user表

   * 用户名不能重复
   * 要包含用户名和密码字段
"""

import pymysql
import hashlib

class User:
    def __init__(self,database):
        self.db = pymysql.connect(user='root',
                                  passwd='123456',
                                  database=database,
                                  charset='utf8')

    # 创建游标对象
    def create_cursor(self):
        self.cur = self.db.cursor()

    #  注册用户
    def register(self,name,passwd):
        sql = "select * from user where name=%s"
        self.cur.execute(sql,[name])
        r = self.cur.fetchone()
        # 查找到说明用户存在
        if r:
            return False

        # 插入用户名密码
        sql = "insert into user (name,passwd) \
        values (%s,%s)"
        # 加密处理
        wd = jm(passwd)
        try:
            self.cur.execute(sql, [name,wd])
            self.db.commit()
            return True
        except:
            self.db.rollback()
            return False

    # 登录用户
    def login(self,name,passwd):
        sql = "select * from user \
        where name=%s and passwd=%s"
        wd = jm(passwd)
        self.cur.execute(sql, [name,wd])
        r = self.cur.fetchone()
        # 查找到则登录成功
        if r:
            return True

    # 查单词
    def find(self,words):
        sql = "select mean from words where word=%s;"
        self.cur.execute(sql,[words])
        r = self.cur.fetchone()
        # 查到则成功
        if r:
            return r[0]

    def insert_history(self,name,words):
        sql = "insert into hist (name,word)values(%s,%s);"
        try:
            self.cur.execute(sql,[name,words])
            self.db.commit()
        except:
            self.db.rollback()

    def find_history(self,name):
        sql = "select name,word,time from hist where name=%s order by time desc"
        self.cur.execute(sql,[name])
        return self.cur.fetchall()



def jm(passwd):
    salt = "^$%#[]{}"
    hash = hashlib.md5(salt.encode())
    hash.update(passwd.encode())
    return hash.hexdigest()


if __name__ == '__main__':
    user = User('stu')

    # if user.register('Abby','123'):
    #     print("注册成功")

    if user.login('Abby','1234'):
        print("登录成功")
