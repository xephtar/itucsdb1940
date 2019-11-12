from flask import Flask
from flask_restful import Api
from views.vets import VetsAPI, VetsListAPI
from views.owners import OwnersAPI, OwnersListAPI
from views.url import owner_register, vet_register, home_page
import secrets

app = Flask(__name__, template_folder='template')

app.secret_key = secrets.token_urlsafe(16)

api = Api(app)

api.add_resource(VetsAPI, '/vets/<int:id>')
api.add_resource(VetsListAPI, '/vets/')
api.add_resource(OwnersAPI, '/owners/<phonenumber>')
api.add_resource(OwnersListAPI, '/owners/')
app.add_url_rule("/owner_register/", view_func=owner_register)
app.add_url_rule("/vet_register/", view_func=vet_register)
app.add_url_rule("/", view_func=home_page)


if __name__ == '__main__':
    app.run(debug=True)
