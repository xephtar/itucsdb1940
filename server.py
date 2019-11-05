from flask import Flask
from flask_restful import Api
from views.vets import VetsAPI, VetsListAPI
from views.owners import OwnersAPI, OwnersListAPI
from views.register import list_vets, vet_register

app = Flask(__name__, template_folder='template')
api = Api(app)

api.add_resource(VetsAPI, '/vets/<int:id>')
api.add_resource(VetsListAPI, '/vets/')
api.add_resource(OwnersAPI, '/owners/<phonenumber>')
api.add_resource(OwnersListAPI, '/owners/')
app.add_url_rule("/owner_register/", view_func=list_vets)
app.add_url_rule("/vet_register/", view_func=vet_register)


@app.route("/")
def home_page():
    return "Initializing........"


if __name__ == '__main__':
    app.run(debug=True)
