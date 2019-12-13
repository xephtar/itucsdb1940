from flask_login import login_required, current_user
from flask_restful import reqparse, Resource, abort
from flask import redirect, flash, session, request, url_for
from models.owners import Owners
from models.vets_to_owners import Vets_to_Owners
from views.url import home_page


class OwnersAPI(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('phonenumber', type=str)

    def get(self, phonenumber):
        u = Owners.get(phonenumber=phonenumber)
        if u:
            return u.__dict__
        return {}, 404

    def put(self, phonenumber):
        if current_user.is_admin:
            args = self.parser.parse_args()
            u = Owners.get(phonenumber=phonenumber)
            if u and args:
                u.update(**args)
                return u.__dict__
        else:
            abort(403)
        return {}, 404

    def delete(self, id):
        if current_user.is_admin:
            u = Owners.get(id=id)
            if u:
                r = u.__dict__
                u.delete()
                return r, 200
        else:
            abort(403)


class OwnersListAPI(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('phonenumber', type=str)

    def get(self):
        qs = Owners.filter()
        if qs:
            r = [u.__dict__ for u in qs]
            return r
        return {}, 404

    def post(self):
        args = self.parser.parse_args()
        vet = reqparse.RequestParser()
        vet.add_argument('phonenumber', type=str)
        vet.add_argument('vet_id', type=int)
        vet = vet.parse_args()
        if args:
            u = Owners.create(**args)
            ovr = Vets_to_Owners.create(**vet)
            if u == '404':
                flash('You were failed to create Owner!')
            else:
                flash('You were successfully created Owner!')

            if ovr == '404':
                flash('You were failed to add Vet!')
            else:
                flash('You were successfully added Vet!')
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
        return {}, 404
