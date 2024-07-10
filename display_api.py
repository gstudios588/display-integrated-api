

from flask import Flask, request, json, jsonify, send_file
import psycopg2
from dotenv import load_dotenv
from require_api_key import require_api_key
import os
import awsgi
from flask_jwt_extended import *

from funct.cek import *
from funct.cek_status import *
from funct.login import *


app = Flask(__name__)
app.json.sort_keys = False
app.config["JWT_SECRET_KEY"] = os.getenv('JWT_SECRET_KEY')
jwt = JWTManager(app)


load_dotenv()
api_key = os.getenv('API_KEY')

@jwt.expired_token_loader
def my_expired_token_callback(jwt_header, jwt_payload):
    return jsonify(status="X1", msg="Token expired"), 401

@jwt.unauthorized_loader
def my_unautorhized(jwt_header):
    return jsonify(status="X1", msg="Missing Authorization Header"), 401

@jwt.invalid_token_loader
def my_bad_header(jwt_header):
    return jsonify(status="X1", msg="Bad token!"), 401


@app.route('/get_info', methods=['POST'])
@require_api_key(key=api_key)
def cek():
    return f_cek()

@app.route('/cek_status', methods=['POST'])
@require_api_key(key=api_key)
@jwt_required()
def cek_status():
    return f_cek_status()

@app.route('/login', methods=['POST'])
@require_api_key(key=api_key)
def login():
    return f_login()

def handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    app.run(debug=True, port=8005, host='0.0.0.0')