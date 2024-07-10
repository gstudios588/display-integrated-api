
from flask import jsonify,request
from module import *


def f_login():
    jsRes =''
    if ('data' in request.form ): data = request.form['data']
    else : return {'status': 'NOK', 'msg': 'Missing data parameter'}
    
    js = cek_json(data)
    if (js == 'error format'): return {'status': 'NOK', 'msg': vMsgRequestFormatError}
    if ('user' not in js): return {'status': 'NOK', 'msg': 'user parameter missing'}
    if ('pass' not in js): return {'status': 'NOK', 'msg': 'password parameter missing'}
    user_name = js['user']
    passwd = js['pass']

    conn = connectDb()
    curr = conn.cursor()
    curr.execute('select user_name, pass from ms_user where user_name = %s', [ user_name])
    dtUser = curr.fetchone()

    conn.close()
    return jsonify(dtUser)