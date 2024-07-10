from flask import Flask, request, json, jsonify, send_file
from module import *

def f_cek_status():
    jsRes = ''

    conn = connectDb()
    curr = conn.cursor()
    curr.execute("select idx, nama_cabang, round( date_part('second' , age(now()::timestamp, last_check)) + "
        " date_part('minute' , age(now()::timestamp, last_check)) * 60 +  "
        " date_part('hour' , age(now()::timestamp, last_check)) * 3600 + "
        " date_part('day' , age(now()::timestamp, last_check)) * 86400 + "
        " date_part('month' , age(now()::timestamp, last_check)) * 2628000000 + "
        " date_part('year' , age(now()::timestamp, last_check)) * 31540000000), " 
        " to_char(last_check, 'yyyy-MM-dd HH24:MI:ss') as last_check "
        " from ms_cabang order by idx") 
    dtStatus = curr.fetchall()

    cabang = []
    for x in dtStatus:
        cabang.append({
            'id_cabang': x[0],
            'nama_cabang': x[1],
            'last_check': x[3],
            'flag': x[2]

        })
    jsRes = {'status': 'OK', 'cabang': cabang}
    conn.close()
    return jsonify(jsRes)