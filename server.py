from flask import Flask,jsonify
from client.db_client import db_client


exp = '''SELECT * FROM dummy'''
exp_insert = '''INSERT INTO dummy VALUES (%s)'''

app = Flask(__name__)


@app.route("/dummy/", methods=['GET'])
def show_dummy():
    rows = db_client.fetch(exp)
    return jsonify(rows)


@app.route("/dummy_insert/", methods=['GET'])
def insert_dummy():
    return db_client.query(exp, 33)


@app.route("/")
def home_page():
    return "Initializing........"


if __name__ == '__main__':
    app.run()
