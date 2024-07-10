from flask import Flask, request, json, jsonify, send_file
from module import *

def f_cek():
    jsRes = ''
    if (not 'data' in request.form): return {'status': 'NOK', 'msg': 'missing data form request'}
    data = request.form['data']
    
    dt = cekDec(data)
    if (dt == 'error decrypt') : return {'status': 'NOK', 'msg': 'Invalid request data'}
    js = cek_json(dt)
    if (js == 'error format'): return {'status': 'NOK', 'msg': 'JSON request format invalid!'}
    
    if ('id_cabang' not in js): return {'status': 'NOK', 'msg': 'id_cabang parameter missing'}
    if ('monitor' not in js): return {'status': 'NOK', 'msg': 'monitor parameter missing'}
    id_cabang = js['id_cabang']
    monitor = js['monitor']

    try: int(id_cabang)
    except: return {'status': 'NOK', 'msg': 'invalid id_cabang value'} 
    try: int(monitor)
    except: return {'status': 'NOK', 'msg': 'invalid monitor value'} 

    conn = connectDb()
    curr = conn.cursor()
    
    # cek id cabang
    curr.execute('SELECT idx, nama_cabang, ket FROM public.ms_cabang where idx = %s', [id_cabang])
    dtCabang = curr.fetchone()
    if (dtCabang == None): jsRes = {'status': 'NOK', 'msg': 'id cabang not found!'}
    
    if (jsRes == ''):
        # get data video
        curr.execute('SELECT idx, file_name, hs, jumlah_monitor, stat, tm FROM public.ms_video '
                    ' where jumlah_monitor = %s and stat = %s order by idx desc limit 1', [monitor, 1])
        dtVideo = curr.fetchone()
        if (dtVideo == None): jsRes = {'status': 'NOK', 'msg': 'data info video tidak ditemukan'}

    if (jsRes == ''):
        # get jobs for cabang
        curr.execute('select job from jobs where id_cabang = %s', [id_cabang])
        dtJobs = curr.fetchall()
        jobs = ''
        for j in dtJobs:
            jobs = jobs + j[0] + ','
        jobs = jobs[:-1]

        if (jobs != []):
            curr.execute('delete from jobs where id_cabang = %s', [id_cabang])

        # update last_check cabang
        curr.execute('update ms_cabang set last_check = now()::timestamp where idx = %s returning last_check', [id_cabang])
        x = curr.fetchone()[0]
        print(str(x))
        fileName = dtVideo[1]
        sgn = dtVideo[2]

        # get param
        curr.execute('select val from ms_param where nama = %s', ['stop_all'])
        dtStopAll = curr.fetchone()
        dtStopAll = dtStopAll[0]

        jsRes = {
            'status': 'OK',
            'cabang': dtCabang[1],
            'fileName': fileName,
            'key': sgn,
            'stop_all': dtStopAll,
            'jobs': jobs
            }
    
    conn.commit()
    conn.close()
    return jsonify(jsRes)