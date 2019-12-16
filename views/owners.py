from flask_login import login_required, current_user
from flask_restful import reqparse, Resource, abort
from flask import redirect, flash, request, url_for
from models.owners import Owners


class OwnersAPI(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('name', type=str)
        self.parser.add_argument('age', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('gender', type=str)
        self.parser.add_argument('treatments', type=str)

    def post(self, phonenumber):
        method = reqparse.RequestParser()
        method.add_argument('_method', type=str)
        method = method.parse_args()
        if method['_method'] == "Delete":
            if OwnersAPI.delete(self, phonenumber):
                flash("Success, Owner is deleted!")
            else:
                flash("Fail, Owner is not deleted!")
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
        elif method['_method'] == "Update":
            if OwnersAPI.put(self, phonenumber):
                flash("Success, Owner is updated!")
            else:
                flash("Fail, Owner is not updated!")
            next_page = request.args.get("next", url_for("home_page"))
            return redirect(next_page)
        else:
            abort(405)

    def get(self, phonenumber):
        u = Owners.get(phonenumber=phonenumber)
        if u:
            owner = u.__dict__
            return owner
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

    def delete(self, phonenumber):
        if current_user.is_admin:
            u = Owners.get(phonenumber=phonenumber)
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
        self.parser.add_argument('gender', type=str)
        self.parser.add_argument('address', type=str)
        self.parser.add_argument('treatments', type=str)

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
            if u is Owners:
                owner = Owners.filter(**args).__getitem__(0)
                flash('You were successfully created Owner!')
                flash(owner.name)
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash('You were failed to create Owner!')
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        return {}, 404
