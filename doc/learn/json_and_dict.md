# Json和python字典

## python字典使用
### 常见操作
Python 3 中的字典（dictionary）是一种可变的、无序的、键值对（key-value pair）的集合

1. 创建字典：

```python
# 使用花括号 {} 创建空字典
empty_dict = {}

# 使用花括号 {} 创建带有键值对的字典
person = {"name": "John", "age": 30, "city": "New York"}
```

2. 访问字典中的值：

```python
# 使用键访问字典中的值
name = person["name"]
print(name)  # 输出：John
```

3. 修改字典中的值：

```python
# 使用键修改字典中的值
person["age"] = 31
print(person)  # 输出：{'name': 'John', 'age': 31, 'city': 'New York'}
```

4. 添加新的键值对：

```python
# 使用新的键添加键值对
person["job"] = "Developer"
print(person)  # 输出：{'name': 'John', 'age': 31, 'city': 'New York', 'job': 'Developer'}
```

5. 删除字典中的键值对：

```python
# 使用 del 语句删除字典中的键值对
del person["age"]
print(person)  # 输出：{'name': 'John', 'city': 'New York', 'job': 'Developer'}
```

6. 检查字典中是否存在某个键：

```python
# 使用 in 关键字检查字典中是否存在某个键
if "name" in person:
    print("Name key exists.")
```

7. 遍历字典中的键值对：

```python
# 使用 for 循环遍历字典中的键值对
for key, value in person.items():
    print(key, value)
```

8. 获取字典中的所有键：

```python
# 使用 keys() 方法获取字典中的所有键
keys = person.keys()
print(keys)  # 输出：dict_keys(['name', 'city', 'job'])
```

9. 获取字典中的所有值：

```python
# 使用 values() 方法获取字典中的所有值
values = person.values()
print(values)  # 输出：dict_values(['John', 'New York', 'Developer'])
```

这些是 Python 3 字典的基本操作。你可以根据需要使用字典来存储和操作数据。


### 深入了解
然而这里有些不习惯的地方在于通过字典拿取value会导致异常

访问字典中的值：

```python
# 使用键访问字典中的值
name = person["name_not_exist"] # raise exception
print(name)  # 输出：John

# 应该使用
name = person.get("name_not_exist", "default_value")
```

## json 序列化

正常的json使用这里就不谈了。
当我们想使用json序列化一个类时
```python
class Test:
    def __init__(self):
        self.name = "123"

print(json.dumps(Test())) # raise TypeError: Object of type Test is not JSON serializable
```
即默认的Python类是无法进行Json序列化的。
```python
class Test:
    def __init__(self):
        self.name = "123"
    def to_dict(self):
        return {"name": self.name}
    
print(json.dumps(Test().to_dict()))
```
因此我们需要生成一个字典方法来进行序列化。

但是对于每个类都要生成这样一个字典方法有点麻烦，好在python本身有魔术方法__dict__
```python
print(json.dumps(Test().__dict__))
```

但是当我们进行嵌套处理的时候，就又会有问题
```python
class Dog:
    def __init__(self):
        self.dog = "dog"
class Test:
    def __init__(self):
        self.name = "123"
        self.dog = Dog()

print(json.dumps(Test().__dict__)) #raise Type Error
```

因此我们为了嵌套处理定义工具类
```python
def toJSON(obj):
    return json.dumps(
        obj,
        default=lambda o: o.__dict__,
        sort_keys=True,
        indent=4)

print(toJSON(Test()))
"""
{
    "dog": {
        "dog": "dog"
    },
    "name": "123"
}

"""
```