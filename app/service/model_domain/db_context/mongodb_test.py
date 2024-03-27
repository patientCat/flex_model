from pymongo import MongoClient

# 连接到MongoDB服务器
client = MongoClient('mongodb://localhost:27017/')

# 选择一个数据库
db = client['my_database']

# 选择一个集合（类似于表）
collection = db['my_collection']

# 插入一个文档
result = collection.insert_one({'name': 'John', 'age': 30})

# 查询文档
cursor = collection.find({'name': 'John'})

# 遍历查询结果并打印
for doc in cursor:
    print(doc)

# 更新文档
collection.update_one({'name': 'John'}, {'$set': {'age': 31}})

# 删除文档
#collection.delete_one({'name': 'John'})