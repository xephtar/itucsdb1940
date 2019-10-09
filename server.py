from flask import Flask, jsonify, redirect, url_for
from client.db_client import db_client


exp = '''SELECT * FROM dummy'''
exp_insert = '''INSERT INTO DUMMY VALUES (33)'''

app = Flask(__name__)


@app.route("/dummy/", methods=['GET'])
def show_dummy():
    rows = db_client.fetch(exp)
    return jsonify(rows)


@app.route("/dummy_insert/", methods=['GET'])
def insert_dummy():
    db_client.insert()
    return redirect(url_for('show_dummy'))


@app.route("/dummy_insert/", methods=['POST'])
def insert_dummy_post():
    db_client.insert()
    return redirect(url_for('show_dummy'))


@app.route("/")
def home_page():
    return "Initializing........"


if __name__ == '__main__':
    app.run()
