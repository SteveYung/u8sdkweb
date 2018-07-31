#!/data/py/android
# -*-coding: utf-8 - *-
import pymysql

#数据库链接配置
host = '127.0.0.1'
port = 3306
user = 'catplay'
passwd = 'Cat@play0904'
db = 'u8sdk'



def write(sql_insert):
    # print(sql_insert)
    client = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
    Client_tk = client.cursor()

    try:
        # 执行sql语句
        Client_tk.execute(sql_insert)
        client.commit()
        sign = True
    except:
        # 发生错误时回滚
        client.rollback()
        sign = False
    client.close()
    return sign


def Initial_contrast(sql_insert):
    # print(sql_insert)
    client = pymysql.connect(host=host,port=port,user=user,passwd=passwd,db=db,charset='utf8')
    Client_tk = client.cursor()

    Client_tk.execute(sql_insert)
    contrast = Client_tk.fetchall()
    client.close()
    return contrast
