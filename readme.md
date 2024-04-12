# Readme
低代码中数据模型的实现
## quickstart

## 项目讲解
低代码项目中的数据模型实现。

数据模型的意义就是对数据库表进行抽象。

### 数据模型表结构
对于普通开发者来说，使用数据库之前需要了解一些数据库特性，比如字段的类型，长度等概念。
对于不同数据库，比如mysql，mongo等，需要明白这些差异。

但是对于低码开发者来说，他们不需要关心这些细节。他们更关心的是我需要定义一个字段来存放email，存放图片，存放时间。
我不需要关心这些底层的实现细节。

#### 使用schema定义表结构
1. 可以利用schema本身具有的功能对写数据进行校验。
2. 前端可以通过schema进行表单的快速生成。

[快速了解schema](/doc/learn/learn_about_schema.md)



## Python3工程学习
[Json和python字典深入学习](/doc/learn/json_and_dict.md)

[如何进行统一全局Response结构和处理全局业务异常](/doc/learn/global_error_handle.md)

[使用flask-restful进行controller处理](/doc/learn/flask-restful.md)