import pymysql

# 连接到数据库
connection = pymysql.connect(
    host="localhost",
    user="root",
    password="123456",
    database="test_mysql"
)

# 创建一个游标对象
cursor = connection.cursor()

# 插入数据（CREATE）
insert_query = "INSERT INTO teacher (name, address) VALUES (%s, %s)"
data = ("value1", "value2")
cursor.execute(insert_query, data)
connection.commit()

# 读取数据（READ）
read_query = "SELECT * FROM teacher"
cursor.execute(read_query)
result = cursor.fetchall()
for row in result:
    print(row)

# 更新数据（UPDATE）
update_query = "UPDATE teacher SET name = %s WHERE address = %s"
data = ("new_value1", "value2")
cursor.execute(update_query, data)
connection.commit()

# 删除数据（DELETE）
delete_query = "DELETE FROM teacher WHERE address = %s"
data = ("value2",)
cursor.execute(delete_query, data)
connection.commit()

# 关闭游标和连接
cursor.close()
connection.close()