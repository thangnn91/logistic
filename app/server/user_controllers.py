from flask import Blueprint, flash, render_template, request, session, abort, \
                  redirect, url_for, current_app, jsonify
from flask_login import login_user, logout_user, current_user
from app.model import user_model
from app.server.forms import LoginForm, RegisterForm, ChangepassForm
from app.server.dao import DatabaseProcess
from app.server.helper import hashPassword, login_required, \
                    db_get_values_to_array, get_error_msg, randomstring, is_not_blank, get_logger
from app import app

import requests
import os
import json
import collections
from werkzeug.utils import secure_filename
import time
import math

user_controller = Blueprint('user', __name__, url_prefix='')

@user_controller.route("/")
def index():
    return render_template('intro/index.html')
    #return redirect(url_for('user.signin'))


@user_controller.route("/dashboard")
@login_required(role="USER")
def dashboard():
    #app.logger.warning('testing warning log')
    return render_template('user/dashboard.html')


@user_controller.route("/dashboard/profile", methods=['GET', 'POST'])
@login_required(role="USER")
def profile():
    user_id = current_user.get_id()
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    if request.method == 'POST':       
        kwargs = type('Dummy', (object,), { "fullname": request.form.get("fullname"),
                                           "address": request.form.get("address"), "mobile": request.form.get("mobile"),
                                           "id": user_id })
        result = _db_process.update_user_info(kwargs)
        user = _db_process.get_user_info(user_id)        
        return render_template('user/profile.html', user=user)
    
    user = _db_process.get_user_info(user_id)
    return render_template('user/profile.html', user=user)

@user_controller.route("/dashboard/user-balance", methods=['GET'])
@login_required(role="USER")
def get_user_balance():
    user_id = current_user.get_id()
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])   
    user = _db_process.get_user_info(user_id)
    return jsonify(user['balance'])

@user_controller.route("/dashboard/change-pass", methods=['GET', 'POST'])
@login_required(role="USER")
def changepass():
    user_id = current_user.get_id()
    form = ChangepassForm()
    if form.validate_on_submit():       
        user_name = current_user.get_name()
        hashOldPass = hashPassword(form.old_pass.data, user_name)
        hashNewPass = hashPassword(form.new_pass.data, user_name)
        kwargs = type('Dummy', (object,), { "old_pass": hashOldPass,
                                           "new_pass": hashNewPass, "id": user_id})
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        
        result = _db_process.user_change_pass(kwargs)                   
        if result > 0:
            return jsonify(result=1, msg='Success')
        else:
            msg = get_error_msg(result)
            return jsonify(result=-1, msg=msg)
            
    return render_template('user/changepass.html', form=form)


@user_controller.route("/dashboard/create-order", methods=['GET', 'POST'])
@login_required(role="USER")
def create_order():
    if request.method == 'POST':
        user_id = current_user.get_id()
        form_dic = request.form.to_dict()
        order_data = form_dic['order_data']
        d = json.loads(order_data)
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        list_currency_rate = _db_process.admin_get_list_currency()
        price_vnd = 0
        for item in d:
            # check du lieu dau vao
            if is_not_blank(item['name']) == False or is_not_blank(item['link']) == False or is_not_blank(item['color']) == False or is_not_blank(item['size']) == False or is_not_blank(item['quantity']) == False \
            or is_not_blank(item['price']) == False or is_not_blank(item['image']) == False or is_not_blank(item['currency']) == False:
                return jsonify(result=-600, msg=get_error_msg(-600))
            # lay ty gia
            filterData = list(filter(lambda x : x['id'] == int(item['currency']), list_currency_rate))
            if not len(filterData):
                return jsonify(result=-99, msg=get_error_msg(-99))
            
            currency_rate = filterData[0]['rate']
            
            item['price_vnd'] = float(item['price']) * currency_rate * int(item['quantity'])
            price_vnd += item['price_vnd'] 
            if(item['is_upload'] == True):
                image_upload = request.files[item['image']]
                filename = secure_filename(image_upload.filename)
                image_upload.save(os.path.join(os.getcwd() + "/app/static/upload/image", filename))
                item['image'] = filename  
               
        memory_code = randomstring(6)
        kwargs = type('Dummy', (object,), { "data": d,
                                           "memory_code": memory_code, "price_vnd": price_vnd, "user_id": user_id})
        
        
        result = _db_process.user_create_order(kwargs)
        if result > 0:
            return jsonify(result=1, msg='Success')
        else:
            msg = get_error_msg(result)
            return jsonify(result=-1, msg=msg)        
    
    return render_template('user/create_order.html')


@user_controller.route("/dashboard/order-detail", methods=['GET', 'PUT'])
@login_required(role="USER")
def order_detail():
    user_id = current_user.get_id()
    #dat coc don hang, method put
    if request.method == 'PUT':
        user_id = current_user.get_id()
        order_code = request.form.get("code")
        
        if order_code is None or is_not_blank(order_code) == False:
            return jsonify(result=-600, msg=get_error_msg(-600))
        order_array = order_code.split(".")
        if len(order_array) != 2:
            return jsonify(result=-600, msg=get_error_msg(-600))
        
        kwargs = type('Dummy', (object,), { "id": order_array[1],
                                               "code": order_array[0], "user_id": user_id})
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        order_info = _db_process.get_order_info(kwargs)
        if order_info is None:
            return jsonify(result=-102, msg=get_error_msg(-102))

        user = _db_process.get_user_info(user_id)
        price_vnd = order_info['price_vnd']
        price_deposit = math.floor(int(price_vnd) * 70 / 100)
        if(int(user['balance']) < price_deposit):
            return jsonify(result=-107, msg=get_error_msg(-107))
        
        kwargs.deposit_value = price_deposit
        kwargs.order_id = order_info['id']
        kwargs.user_id = user_id
        _db_process.user_deposit_order(kwargs)
        return jsonify(result=1, msg='Success')
    
    order_code = request.args.get('code')
    if order_code is None:
        return redirect(url_for('user.dashboard', msg='code empty'))
    order_array = order_code.split(".")
    if len(order_array) != 2:
        return redirect(url_for('user.dashboard', msg='code invalid'))
    
    kwargs = type('Dummy', (object,), { "id": order_array[1],
                                           "code": order_array[0], "user_id": user_id})
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    order_info = _db_process.get_order_info(kwargs)
    if order_info is None:
        return redirect(url_for('user.dashboard', msg='order null'))
    
    order_detail_id_array = order_info['order_item'].split(',')
    order_detail = _db_process.get_order_detail(order_detail_id_array)
    list_fee = _db_process.admin_get_list_fee()
    return render_template('user/order_detail.html', order=order_info, detail=order_detail, list_fee=json.dumps(list_fee))

@user_controller.route("/dashboard/list-order", methods=['GET', 'POST'])
@login_required(role="USER")
def list_order():
    if request.method == 'POST':
        user_id = current_user.get_id()
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        args = type('Dummy', (object,), {"uid": user_id})
        
        if(request.form.get("status") is not None and is_not_blank(request.form.get("status"))):
            args.status = request.form.get("status")
            
        if(request.form.get("from_time") is not None and is_not_blank(request.form.get("from_time"))):
            args.from_time = request.form.get("from_time")
            
        if(request.form.get("to_time") is not None and is_not_blank(request.form.get("to_time"))):
            args.to_time = request.form.get("to_time")
            
        orders = _db_process.get_list_order(args)
        return jsonify(data=orders)
    
    return render_template('user/list_order.html')


@user_controller.route("/signin", methods=['GET', 'POST'])
def signin():
    # user_object = user_model.User(1)
    # login_user(user_object)
    # return redirect(url_for('admin.index'))
    form = LoginForm()
    if form.validate_on_submit():
        hashPass = hashPassword(form.password.data, form.email.data)
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        result = _db_process.login(form.email.data, hashPass)                      
        if type(result) == int:
            flash(get_error_msg(result))
        else:
            login_user(result)
            urole = current_user.urole
            session['user_name'] = form.email.data
            session['role'] = urole
            if urole == "ADMIN" or urole == "MOD" or urole == "ASSIST" or urole == "BUYER" or urole == "SHIPPER":
                return redirect(url_for('admin.index'))
            else:
                return redirect(url_for('user.dashboard'))
              
    return render_template('signin.html', form=form, title='Login')


@user_controller.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect(url_for('user.signin'))


@user_controller.route("/signup", methods=['GET', 'POST'])
def signup():
    # user_object = user_model.User(1)
    # login_user(user_object)
    # return redirect(url_for('admin.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        hashPass = hashPassword(form.password.data, form.email.data)
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        result = _db_process.register(form.email.data, hashPass)                   
        if result > 0:
            return redirect(url_for('user.signin'))
        else:
            msg = get_error_msg(result)
            flash(msg)
                  
    return render_template('signup.html', form=form, title='Register')

