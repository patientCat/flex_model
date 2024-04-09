from dataclasses import dataclass
from app.service.model_domain.metadata.model import ModelContext, ModelNameCtx

"""
根据模型对数据库进行增删查改
"""


@dataclass
class DataOperationContext:
    model_context: ModelContext
    param_dict: dict


class DataOperation:
    def __init__(self):
        pass

    def createOne(self, context: DataOperationContext):
        pass

    def updateOne(self):
        pass

    def findOne(self):
        pass

    def findMany(self):
        pass

    def deleteOne(self):
        pass

    def deleteMany(self):
        pass
