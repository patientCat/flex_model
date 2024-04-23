import flask


class HelloWorld:
    def __init__(self):
        self.name = "Hello World"


res = flask.jsonify(HelloWorld)
print(res)
