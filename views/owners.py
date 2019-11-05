from flask_restful import reqparse, Resource
from flask import redirect
from models.owners import Owners


class OwnersAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('phoneNumber', type=str)

    def get(self, id):
        u = Owners.get(id=id)
        if u:
            return u.__dict__
        return {}, 404

    def put(self, id):
        args = self.parser.parse_args()
        u = Owners.get(id=id)
        if u and args:
            u.update(**args)
            return u.__dict__
        return {}, 404

    def delete(self, id):
        u = Owners.get(id=id)
        if u:
            r = u.__dict__
            u.delete()
            return r, 200


class OwnersListAPI(Resource):

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('phoneNumber', type=str)

    def get(self):
        qs = Owners.filter()
        if qs:
            r = [u.__dict__ for u in qs]
            return r
        return {}, 404

    def post(self):
        args = self.parser.parse_args()
        if args:
            u = Owners.create(**args)
            if u:
                return redirect('/owners/')
        return {}, 404
