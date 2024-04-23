# 如何高效组织代码
[github](https://github.com/patientCat/flex_model?tab=readme-ov-file)

## 项目结构

```
项目名/
│
├─docs/                  # 项目文档, 如说明手册和技术文档
│   ├─指南/               # 用户操作指南
│   └─API文档/            # API接口详细描述
│
├─app/                   # 存放源代码文件
│   ├─service            # service模块，负责组织
│   ├─common             # 公共模块
│   ├─controller         # 控制器模块
│   ├─domain             # 业务模块
│   └─repo               # 存储层
│
├─autotest               # 自动化测试
│
├─requirements.txt       # 项目所需依赖包列表以及版本号等信息
└─readme.md              # 项目简介和项目安装使用方法的说明文档

```
## 组织代码

使用controller， service，domain的轻量DDD模式组织代码

这里算是一些个人经验所得。

controller： 负责校验参数，处理输入输出的返回。以及特殊错误的处理
service or api: 是业务逻辑的实现。负责组织domain。只负责业务，不关心底层逻辑。
domain: 每一个domain都是完善的业务模块。对外抽象底层逻辑。


单元测试：
在domain层需要最多的单元测试。保证每个domain的正常和异常情况处理。
在service层一般不需要单元测试，因为service层在业务开发中，应该是变化最多的地方。
在controller层不需要单元测试。都是使用的公共模块。且业务逻辑简单。

集成测试：
使用流水线进行集成测试。

### controller层处理
controller层负责处理用户请求。
1. 校验参数。
2. 处理入参。
3. 处理出参。
4. 整体错误处理。

```python
def service_process():
    return {"success": True}

class TestArgParse(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument(name='Required', required=True, help="Required is needed")
        parser.add_argument(name='TestInt', type=int, required=True, help="TestInt must be an integer and required")
        parser.add_argument(name='Optional', dest='opt', type=str, required=False, default="default",
                            help="Optional must be a string")
        args = parser.parse_args()
        # log request args
        print(f"request_args={args}")
        # call service
        response = service_process()
        # log response 
        print(f"response={response}")
        return response
```

### service层
传统的贫血模式代码，经常会导致service层写的非常重。包含大量凌乱的业务逻辑代码。

而目前比较流行的方式会增加一层domain层。将不同业务逻辑进行抽象，解耦。对于Service层来说，只需要对domain进行组织即可。

关于这里的分层模式，每个人有每个人的思考。大家自己选择，如果有兴趣，可以了解下DDD。消化其中的思想后，然后进行应用。