from flask import Flask
from flask_restful import Api
from models.users import Users
from views.vets import VetsAPI, VetsListAPI
from views.owners import OwnersAPI, OwnersListAPI
from views.url import owner_register, vet_register, home_page, vet_profile, vet_profiles, owner_profile, owner_profiles
import secrets
from flask_login import LoginManager, confirm_login
from views.login import login_page, logout_page, register_page


lm = LoginManager()


@lm.user_loader
def load_user(user_id):
    reg_user = Users.get(username=user_id)
    if reg_user:
        if user_id == reg_user.get_id():
            return reg_user
    return None


app = Flask(__name__, template_folder='template')
app.secret_key = secrets.token_urlsafe(16)
app.url_map.strict_slashes = False
api = Api(app)
lm.init_app(app)
lm.login_view = "login_page"


@app.before_request
def before_request():
    confirm_login()


api.add_resource(VetsAPI, '/vets/<int:id>')
api.add_resource(VetsListAPI, '/vets/')
api.add_resource(OwnersAPI, '/owners/<phonenumber>')
api.add_resource(OwnersListAPI, '/owners/')
app.add_url_rule("/profile/vet/<int:id>", view_func=vet_profile, methods=["GET"])
app.add_url_rule("/profile/vets/", view_func=vet_profiles, methods=["GET"])
app.add_url_rule("/profile/owner/<phonenumber>", view_func=owner_profile, methods=["GET"])
app.add_url_rule("/profile/owners/", view_func=owner_profiles, methods=["GET"])
app.add_url_rule("/owner_register/", view_func=owner_register, methods=["GET"])
app.add_url_rule("/vet_register/", view_func=vet_register, methods=["GET"])
app.add_url_rule("/", view_func=home_page)
app.add_url_rule("/login", view_func=login_page, methods=["GET", "POST"])
app.add_url_rule("/register", view_func=register_page, methods=["GET", "POST"])
app.add_url_rule("/logout", view_func=logout_page, methods=["GET"])

if __name__ == '__main__':
    app.run(debug=True)
