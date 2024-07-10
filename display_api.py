

from flask import Flask, request, json, jsonify, send_file
import psycopg2
from dotenv import load_dotenv
from require_api_key import require_api_key
import os
import awsgi


from funct.cek import *
from funct.cek_status import *

app = Flask(__name__)
app.json.sort_keys = False

load_dotenv()
api_key = os.getenv('API_KEY')

@app.route('/get_info', methods=['POST'])
@require_api_key(key=api_key)
def cek():
    return f_cek()

@app.route('/cek_status', methods=['POST'])
@require_api_key(key=api_key)
def cek_status():
    return f_cek_status()

def handler(event, context):
    return awsgi.response(app, event, context)

if __name__ == '__main__':
    app.run(debug=True, port=8005, host='0.0.0.0')