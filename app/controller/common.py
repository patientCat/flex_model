from flask_restful import Resource, reqparse


class HealthCheck(Resource):
    def get(self):
        print("HealthCheck")
        return {"success": True}

    def post(self):
        print("HealthCheck")
        return {"success": True}

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
