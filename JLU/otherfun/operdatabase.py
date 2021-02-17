import pymysql

URL = 'localhost'
USER = 'root'
PASSWD = '123456'
DBNAME = 'm_trainsystem'


def mdbinsertone(table, names, values):
    conn = pymysql.connect(URL, user=USER, passwd=PASSWD, db=DBNAME)
    # 获取游标
    cursor = conn.cursor()
    strname = ",".join(names)
    for i, v in enumerate(values):
        values[i] = "\'" + v + "\'"
    strvalue = ",".join(values)
    try:
        insert = cursor.execute("insert into " + table + "(" + strname + ") values (" + strvalue + ")")
        conn.commit()
        print(insert)
    except:
        conn.rollback()

    cursor.close()
    conn.close()


def mdbinsertmany(table, names, values):
    conn = pymysql.connect(URL, user=USER, passwd=PASSWD, db=DBNAME)
    # 获取游标
    cursor = conn.cursor()
    strname = ",".join(names)

    cnames = names.copy()
    for i, v in enumerate(cnames):
        cnames[i] = '%s'
    prevaluestr = ",".join(cnames)

    try:
        sql = "insert into " + table + "(" + strname + ")" + " values(" + prevaluestr + ")"
        print("您的sql语句是:"+sql)
        insert = cursor.executemany(sql, values)
        conn.commit()
        print("操作影响的行数:"+str(insert))
    except Exception as e:
        print(e)
        conn.rollback()

    cursor.close()
    conn.close()

import os
def writefiletodb(path):
    ncontent = []
    with open(path, encoding='utf-8') as file_obj:
        stationcontent = file_obj.readlines()
    for i, v in enumerate(stationcontent):
        ncontent.append((i+1,v.replace("\n", "")))

    # print(ncontent)
    tablename = "ticket_station"
    strname = ["id","name"]
    # strvalue = [("test1"), ("test2"), ("test3"), ]
    mdbinsertmany(tablename,strname,ncontent)


if __name__ == '__main__':
    writefiletodb("C:/Users/34588/Desktop/name.txt")