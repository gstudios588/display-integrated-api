
from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os
import json
import psycopg2

load_dotenv()

x = os.getenv('ENC_KEY')
s = x.encode()
dbHost = os.getenv('DBHOST')
userDb = os.getenv('USERDB')
passDb = os.getenv('PASSDB')
dbPORT = os.getenv('DBPORT')
dbname = os.getenv('DBNAME')

fernetAPI = Fernet(s)

vMsgRequestFormatError = 'Error request JSON format'

def cekDec(txt):
    global xor_key
    res =''
    res = txt

    # try:
    #    res = myDecryptAPI(txt)
    # except:
    #     return 'error decrypt'
    return res

def cek_json(text):
    try:
        ms = json.loads(text)
        return ms
    except:
        print('error json convert')
        return 'error format'

def myEncryptAPI(txt):
    enc = fernetAPI.encrypt(txt.encode())
    return enc.decode()

def myDecryptAPI(txt):
    dec = fernetAPI.decrypt(txt.encode())
    return dec.decode()

    
def connectDb():
    return psycopg2.connect(f"dbname={dbname} user={userDb} host={dbHost} password={passDb} port={dbPORT}")

