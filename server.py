from flask import Flask, session, request
from flask_restful import Api
from views.users import get_user
from views.vets import VetsAPI, VetsListAPI
from views.owners import OwnersAPI, OwnersListAPI
from views.url import owner_register, vet_register, home_page
import secrets
from flask_login import LoginManager, current_user
from views.login import login_page, logout_page


lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    if not session.get("token") is None:
        return get_user(session.get("user_id"))

    if user_id is not None:
        return get_user(user_id)
    return None


app = Flask(__name__, template_folder='template')
app.secret_key = secrets.token_urlsafe(16)
api = Api(app)
lm.init_app(app)
lm.login_view = "login_page"


@app.before_request
def before_request():
    user = current_user


api.add_resource(VetsAPI, '/vets/<int:id>')
api.add_resource(VetsListAPI, '/vets/')
api.add_resource(OwnersAPI, '/owners/<phonenumber>')
api.add_resource(OwnersListAPI, '/owners/')
app.add_url_rule("/owner_register/", view_func=owner_register, methods=["GET"])
app.add_url_rule("/vet_register/", view_func=vet_register, methods=["GET"])
app.add_url_rule("/", view_func=home_page)
app.add_url_rule("/login", view_func=login_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout_page, methods=["GET"])

if __name__ == '__main__':
