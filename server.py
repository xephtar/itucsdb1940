from flask import Flask,jsonify
from client.db_client import db_client


exp = '''SELECT * FROM dummy'''


app = Flask(__name__)


@app.route("/dummy/", methods=['GET'])
def show_dummy():
    rows = db_client.fetch(exp)
    return jsonify(rows)


@app.route("/")
def home_page():
    return "Initializing........"


if __name__ == '__main__':
    app.run()
