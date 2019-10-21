from flask_restful import reqparse, Resource
from users.vets import Vets


class VetsAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=int)

    def get(self, id):
        u = Vets.get(id=id)
        if u:
            return u.__dict__
        return {}, 404

    def put(self, id):
        args = self.parser.parse_args()
        u = Vets.get(id=id)
        if u and args:
            u.update(**args)
            return u.__dict__
        return {}, 404

    def delete(self, id):
        u = Vets.get(id=id)
        if u:
            r = u.__dict__
            u.delete()
            return r, 200


class VetsListAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=int)

    def get(self):
        qs = Vets.filter()
        if qs:
            r = [u.__dict__ for u in qs]
            return r, 200
        return {}, 404

    def post(self):
        args = self.parser.parse_args()
        if args:
            u = Vets.create(**args)
            if u:
                return u.__dict__
        return {}, 404
