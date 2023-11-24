import json
import sqlite3
from sqlite3 import Error
from datetime import datetime
import pytz

from flask import abort, Flask, jsonify, redirect, request, url_for

def create_connection():
    try:
        return sqlite3.connect('milestones.db')
    except:
        print('Error! tidak dapat terkoneksi ke database.')
        return None

def create_table():
    try:
        with create_connection() as conn:
            c = conn.cursor()
            c.execute('''
                CREATE TABLE IF NOT EXISTS milestone(
                    "id" integer NOT NULL PRIMARY KEY AUTOINCREMENT,
                    "capaian" text(150),
                    "waktu" text(150),
                    "waktu_ditambahkan" text(150),
                    "waktu_diubah" text(150)
                );
            ''')
    except Error as e:
        print(e)

def get(id=None, is_set=False):

    with create_connection() as conn:
        c = conn.cursor()

        if id:
            c.execute(
                '''
                    SELECT *
                    FROM milestone
                    WHERE id = ?;
                ''',
                (id,)
            )

            row = c.fetchall()

            if row:
                row = row[0]
                data = {
                    'id': row[0],
                    'capaian': row[1],
                    'waktu': row[2],
                    'waktu_ditambahkan': row[3],
                    'waktu_diubah': row[4]
                }
            else:
                data = []
        else:
            c.execute(
                '''
                    SELECT *
                    FROM milestone;
                ''',
            )
            
            data = [
                {
                    'id': row[0],
                    'capaian': row[1],
                    'waktu': row[2],
                    'waktu_ditambahkan': row[3],
                    'waktu_diubah': row[4]
                } for row in c.fetchall()
            ]
    
    if data:
        data = {
            'code': 200,
            'message': 'milestone berhasil ditemukan.',
            'data': data
        }

        if is_set:
            data['code'] = 201
            data['message'] = 'Data milestone barhasil tersimpan.'
    else:
        abort(404)

    return data

def get_current_time():
    utc_time = datetime.utcnow()
    jakarta_timezone = pytz.timezone('Asia/Jakarta')
    jakarta_time = utc_time.replace(tzinfo=pytz.utc).astimezone(jakarta_timezone)
    return jakarta_time

def post():

    with create_connection() as conn:
        c = conn.cursor()

        current_time = get_current_time()

        if request.json:
            capaian = json.loads(
                request.data
            ).get('capaian')
        else:
            capaian = request.form.get('capaian')

        if request.json:
            waktu = json.loads(
                request.data
            ).get('waktu')
        else:
            waktu = request.form.get('waktu')

        if capaian and waktu:
            c.execute(
                '''
                    INSERT INTO "main"."milestone" ("capaian", "waktu", "waktu_ditambahkan", "waktu_diubah") 
                    VALUES (?, ?, ?, ?);
                ''',
                (capaian, waktu, current_time, current_time)
            )

            id = c.lastrowid
        else:
            abort(400)
        
    return get(id, True)

def put(id):

    with create_connection() as conn:
        c = conn.cursor()
        current_time = get_current_time()

        if request.json:
            capaian = json.loads(
                request.data
            ).get('capaian')
        else:
            capaian = request.form.get('capaian')

        if request.json:
            waktu = json.loads(
                request.data
            ).get('waktu')
        else:
            waktu = request.form.get('waktu')
        
        if capaian and waktu:
            c.execute(
                '''
                    UPDATE main.milestone 
                    SET capaian = ?, waktu = ?, waktu_diubah = ?
                    WHERE id = ?
                ''',
                (capaian, waktu, current_time, id)
            )
        elif capaian:
            c.execute(
                '''
                    UPDATE main.milestone
                    SET capaian = ?, waktu_diubah = ? 
                    WHERE id = ?;
                ''',
                (capaian, current_time, id)
            )
        elif waktu:
            c.execute(
                '''
                    UPDATE "main"."milestone"
                    SET "waktu" = '?', waktu_diubah = ? WHERE id
                ''',
                (waktu, current_time, id)
            )
        else:
            abort(400)

    return get(id, True)

def delete(id):

    with create_connection() as conn:
        c = conn.cursor()

        c.execute(
            '''
                DELETE
                FROM main.milestone
                WHERE id = ?;
            ''',
            (id,)
        )

    return {
        'code': 200,
        'message': 'Data milestone berhasil dihapus.',
        'data': None
    }

def response_api(data):

    return (
        jsonify(**data),
        data['code']
    )

app = Flask(__name__)

@app.errorhandler(400)
def bad_request(e):
    return response_api({
        'code': 400,
        'message': 'Ada kekeliruan input saat melakukan request.',
        'data': None
    })

@app.errorhandler(404)
def not_found(e):
    return response_api({
        'code': 404,
        'message': 'milestone tidak berhasil ditemukan.',
        'data': None
    })

@app.errorhandler(405)
def method_not_allowed(e):
    return response_api({
        'code': 405,
        'message': 'milestone tidak berhasil ditemukan.',
        'data': None
    })

@app.errorhandler(500)
def internal_server_error(e):
    return response_api({
        'code': 500,
        'message': 'Mohon maaf, ada gangguan pada server.',
        'data': None
    })

@app.route('/')
def root():
    return 'RESTful API Sederhana Menggunakan Flask'

@app.route('/milestone', methods=['GET', 'POST'])
@app.route('/milestone/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def users(id=None):
    """
    RESTful API /users.
    """
    if request.method == 'GET':
        data = get(id)
    if request.method == 'POST':
        data = post()
    elif request.method == 'PUT':
        data = put(id)
    elif request.method == 'DELETE':
        data = delete(id)
    
    return response_api(data)

if __name__ == '__main__':
    create_table()
    app.run(debug=True)