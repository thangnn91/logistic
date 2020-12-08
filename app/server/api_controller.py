from flask import Blueprint, flash, request, jsonify, current_app
from flask_api import FlaskAPI, status, exceptions
from app import app
from app.vndb import DBHelper

import requests
import os
import hashlib, uuid
import app.server.helper as server_helper


api_controller = Blueprint('api', __name__, url_prefix='/api')

@api_controller.route("/test", methods=['GET','POST'])
def test():
    print(current_app.config['DB_CONNECTSTRING'])
    db_conf = {
            'user' : 'root',
            'passwd' : 'nnt',
            'host' : '127.0.0.1',
            'schema' : 'logistic',
            'charset' : 'utf8mb4'
        }
    with DBHelper(**db_conf) as db:
        string_to_hash = '123456'
        salt = uuid.uuid4().hex
        string_to_hash = string_to_hash + 'user1@logistic.com' + '!@#$%^&*()%^$&#'
        hash_object = hashlib.sha512(str(string_to_hash).encode('utf-8')).hexdigest()
        
        sql = 'insert into dbo_user(email, password, status, type) values (%s,%s,%s,%s)'
        params = ['user1@logistic.com', hash_object, 1, 0]
        #db.execute(sql, params)
   
    return jsonify(hash_object)