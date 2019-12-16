from flask_login import login_required, current_user
from flask_restful import reqparse, Resource
from flask import redirect, abort, flash, request, url_for
from models.vets import Vets


class VetsAPI(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('profession', type=str)
        self.parser.add_argument('gender', type=str)

    def post(self, id):
        method = reqparse.RequestParser()
        method.add_argument('_method', type=str)
        method = method.parse_args()
        if method['_method'] == "Delete":
            if VetsAPI.delete(self, id):
                flash("Success, Vet is deleted!")
            else:
                flash("Fail, Vet is not deleted!")
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
        elif method['_method'] == "Update":
            if VetsAPI.put(self, id):
                flash("Success, Vet is updated!")
            else:
                flash("Fail, Vet is not updated!")
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
        else:
            abort(405)

    def get(self, id):
        u = Vets.get(id=id)
        if u:
            vet = u.__dict__
            return vet
        return {}, 404

    def put(self, id):
        if current_user.is_admin:
            args = self.parser.parse_args()
            u = Vets.get(id=id)
            if u and args:
                u.update(**args)
                return u.__dict__
        else:
            abort(403)
        return {}, 404

    def delete(self, id):
        if current_user.is_admin:
            u = Vets.get(id=id)
            if u:
                r = u.__dict__
                u.delete()
                return r, 200
        else:
            abort(403)


class VetsListAPI(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('gender', type=str)
        self.parser.add_argument('profession', type=str)

    def get(self):
        if current_user.is_admin:
            qs = Vets.filter()
            if qs:
                r = [u.__dict__ for u in qs]
                return r
        else:
            abort(403)
        abort(404)

    def post(self):
        args = self.parser.parse_args()
        if args:
            if Vets.create(**args):
                vet = Vets.filter(**args).__getitem__(0)
                flash('You were successfully created Vet!')
                flash(vet.name)
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash('You were failed to create Vet!')
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        return {}, 404
