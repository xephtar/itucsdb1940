from flask_login import login_required, current_user
from flask_restful import reqparse, Resource, abort
from flask import redirect, flash, request, url_for
from models.vets_to_owners import Vets_to_Owners


class VetsOwners(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('vet_id', type=str)
        self.parser.add_argument('owner_phone', type=str)

    def get(self, vet_id):
        qs = Vets_to_Owners.get(vet_id=vet_id)
        if qs:
            vet = [u.__dict__ for u in qs]
            return vet
        return {}, 404


class VetsOwnersList(Resource):
    method_decorators = [login_required]

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('vet_id', type=str)
        self.parser.add_argument('owner_phone', type=str)

    def get(self):
        if current_user.is_admin:
            qs = Vets_to_Owners.filter()
            if qs:
                r = [u.__dict__ for u in qs]
                return r
        else:
            abort(403)
        abort(404)

    def post(self):
        args = self.parser.parse_args()
        if args:
            u = Vets_to_Owners.create(**args)
            if type(u) is str:
                flash(u)
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
            else:
                flash('You were successfully added relation!')
                next_page = request.args.get("next", url_for("home_page"))
                return redirect(next_page)
        return {}, 404
