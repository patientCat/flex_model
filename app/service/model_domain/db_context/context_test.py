from context import DbContext, Table
from pymongo import MongoClient
import unittest


class ContextTest(unittest.TestCase):
    def test_collection_name(self):
        test_db_context = DbContext('mongodb://localhost:27017/', "my_database", Table("my_collection"))
        self.assertEqual("default_my_collection", test_db_context.table.collection_name())

        test_db_context = DbContext('mongodb://localhost:27017/', "my_database", Table("my_collection", use_ns=False))
        self.assertEqual("my_collection", test_db_context.table.collection_name())


db_context = DbContext('mongodb://localhost:27017/', "my_database", Table("my_collection"))
# 连接到MongoDB服务器
client = MongoClient(db_context.db_url)

# 选择一个数据库
db = client[db_context.database_name]

# 选择一个集合（类似于表）
collection = db[db_context.table.collection_name()]

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
collection.delete_one({'name': 'John'})
