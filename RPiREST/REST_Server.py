#!/usr/bin/python3
from flask import Flask, make_response
from flask_httpauth import HTTPBasicAuth
import json
import psycopg2

app = Flask(__name__)
auth = HTTPBasicAuth()

usernameDB = "pi"
passwordDB = "raspberry"

@auth.get_password
def get_pw(username):
    if username == usernameDB:
        return passwordDB
    return None

@auth.error_handler
def unauthorized():
    return make_response(json.dumps({'error': 'Unauthorized access'}), 401)

@app.route("/",methods=["GET"])
@auth.login_required
def index():
    return "Response from RPi"

@app.route("/DumpSensor01",methods=["GET"])
@auth.login_required
def DumpSensor01():
    conn = psycopg2.connect(
        database="sensordb",
        user="postgres",
        password="raspDB",
        host="127.0.0.1",
        port="5432"
    )

    cur = conn.cursor()
    cur.execute("SELECT * FROM sensortable")
    rows = cur.fetchall()
    conn.close()

    resultList = []
    for row in rows:
        resultDict = {
            "ID"    : row[0],
            "NAME"  : row[1],
            "TYPE"  : row[2],
            "VALUE" : row[3],
            "DATE"  : str(row[4])
        }
        resultList.append(resultDict)

    return json.dumps(resultList)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
