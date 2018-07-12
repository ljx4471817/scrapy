print('mysqlpipelines is start')


import pymysql
db = pymysql.connect(
    host='127.0.0.1',
    port=3306,
    user='ljx',  # 使用自己的用户名
    passwd='123456',  # 使用自己的密码
    db='spiderdata',  # 数据库名
    charset='utf8'
)
# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()
print('数据库连接成功!')

def insert(items):
    sql='''insert into dd_name(xs_name,xs_author,category,name_id,serialurl,serialstatus,serialnumber)
values (%s,%s,%s,%s,%s,%s,%s)'''
    lis = (items['name'],items['author'],items['category'],items['name_id'],items['serialurl'],items['serialstatus'],items['serialnumber'])
    cursor.execute(sql,lis)
    db.commit()
    return

def select_name(id):
    sql='SELECT * FROM dd_name where name_id = id'
    print('select_name',id)
    cursor.execute(sql)
    results = cursor.fetchone()
    if results==None:
        return True
    else:
        return False

def close_connect():
    print('关闭数据库连接')
    cursor.close()
    db.close()