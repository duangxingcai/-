"""
    mysql
    pymysql
"""

import pymysql

# 连接数据库
db = pymysql.connect(host='localhost',port = 3306, user = 'root',passwd = '123456',database = 'stu',charset = 'utf8')

# 获取游标，执行sql语句，得到执行结果
cur = db.cursor()

# 执行语句
sql = "insert into class_1 values(5,'emma',17,'w',45);"
cur.execute(sql)

# 提交到数据库
db.commit()

# 关闭游标
cur.close()

# 关闭数据库
db.close()


