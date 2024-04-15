import json


class Dog:
    def __init__(self):
        self.dog = "dog"


class Test:
    def __init__(self):
        self.name = "123"
        self.dog = Dog()
        self.dog2 = None


# print(json.dumps(Test().__dict__))


def toJSON(obj):
    return json.dumps(
        obj,
        default=lambda o: o.__dict__)


print(toJSON(Test()))


