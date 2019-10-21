from flask import Flask, jsonify, redirect, url_for
from flask_restful import Api
from client.db_client import db_client
from views.vets import VetsAPI, VetsListAPI

exp = '''SELECT * FROM DUMMY'''
fecthing_vets = '''SELECT * FROM VETS'''
exp_insert = '''INSERT INTO DUMMY VALUES (%s)'''
vet_insert = '''INSERT INTO VETS (name,age) values (%s, %s)'''

app = Flask(__name__)
api = Api(app)

api.add_resource(VetsAPI, '/vets/<int:id>')
api.add_resource(VetsListAPI, '/vets/')


@app.route("/dummy/", methods=['GET'])
def show_dummy():
    rows = db_client.fetch(exp)
    return jsonify(rows)


@app.route("/vet_register/", methods=['GET'])
def show_form():
    form = """<form action="/vets/" method="post">
  Name : <input type="text" name="name" id="name"><br>
  Age : <input type="number" name="age" id="age"><br>
  <input type="submit" value="submit">
    </form>"""
    return form


@app.route("/dummy_insert/", methods=['POST'])
def insert_dummy_post():
    db_client.insert(exp_insert, (33,))
    return redirect(url_for('show_dummy'))


# @app.route("/vet_insert/", methods=['POST'])
# def insert_vet_post():
#     data = request.form
#     if data:
#         db_client.insert(vet_insert, (data['name'], data['age']))
#     return redirect(url_for('show_vets'))


@app.route("/")
def home_page():
    return "Initializing........"


if __name__ == '__main__':
    app.run()
