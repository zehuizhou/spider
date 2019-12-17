import pymysql

# 打开数据库连接
db = pymysql.connect("localhost", "root", "123456", "douban")

# 使用 cursor() 方法创建一个游标对象 cursor
cursor = db.cursor()

# 使用 execute() 方法执行 SQL，如果表存在则删除
cursor.execute("DROP TABLE IF EXISTS EMPLOYEE")

# 使用预处理语句创建表
sql = """CREATE TABLE EMPLOYEE (
         FIRST_NAME  CHAR(20) NOT NULL,
         LAST_NAME  CHAR(20),
         AGE INT,  
         SEX CHAR(1),
         INCOME FLOAT )"""

cursor.execute(sql)

# SQL 插入语句
sql = "INSERT INTO EMPLOYEE(FIRST_NAME, \
       LAST_NAME, AGE, SEX, INCOME) \
       VALUES (%s, %s,  %s, %s,  %s)"
try:
    # 执行sql语句
    cursor.executemany(sql, [('234', 'sdf', 20, 'M', 2000), ('1', '12312', 20, 'M', 2000)])
    # 执行sql语句
    db.commit()
except:
    # 发生错误时回滚
    print("回滚")
    db.rollback()

# 关闭数据库连接
db.close()
