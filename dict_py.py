"""
    把单词录入数据库
"""
import pymysql

db = pymysql.connect(user="root",passwd='123456',database="dict",charset="utf8")

cur = db.cursor()
i = 0
f = open('dict.txt')
for word in f:
    words = word.split(' ')[0]
    mean = word.split(' ')[-1]
    try:
        sql = "insert into words values(%s,%s,%s)"
        i += 1
        cur.execute(sql,[i,words,mean])
    except Exception as e:
        print(e)
        db.rollback()

db.commit()
cur.close()
db.close()
print(i)