from flask_restful import Resource


class HealthCheck(Resource):
    def get(self):
        print("HealthCheck")
        return {"success": True}

    def post(self):
        print("HealthCheck")
        return {"success": True}
