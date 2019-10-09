import psycopg2
import os
from flask import Flask, redirect, url_for
from flask import jsonify


url = os.getenv("DATABASE_URL")


app = Flask(__name__)

con = psycopg2.connect(url)

# cursor
cur = con.cursor()


def print_dummy():
    cur.execute("select * from dummy")
    rows = cur.fetchall()
    return rows


@app.route("/dummy/", methods=['GET'])
def show_dummy():
    rows = print_dummy()
    return jsonify(rows)


@app.route("/")
def home_page():
    return "Initializing........"


if __name__ == '__main__':
    app.run()

# close the cursor
cur.close()
# close the connection
con.close()
