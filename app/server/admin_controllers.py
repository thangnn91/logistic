from flask import Blueprint, flash, render_template, request, session, abort, \
                  redirect, url_for, current_app, jsonify
from flask_login import login_user, logout_user, current_user
from itertools import groupby
from datetime import datetime
from app.model import user_model
from app.server.forms import LoginForm, CreateUserForm
from app.server.dao import DatabaseProcess
from app.server.helper import hashPassword, login_required, db_get_values_to_array, get_error_msg, get_user_role, \
                            is_not_blank
from app import app
import requests
import os
import json
import collections

admin_controller = Blueprint('admin', __name__, url_prefix='/admin')


@admin_controller.route("/")
@login_required(role="ADMIN,MOD,ASSIST,BUYER,SHIPPER")
def index():
    return render_template('admin/index.html')


@admin_controller.route("/fee-config", methods=['GET', 'POST'])
@login_required(role="ADMIN")
def fee_config():
    
    if request.method == 'POST':
        kwargs = type('Dummy', (object,), { "type": request.form.get("type"),
                                           "data": json.loads(request.form.get("data"))})
        fee_type = request.form.get("is_edit")
        if fee_type is not None:
            if fee_type.isdigit() == False:
                return jsonify(result=-1, msg='Không thể cập nhật bản ghi')
            kwargs.is_update = 1;
                   
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        result = _db_process.admin_insert_update_fee(kwargs)
        if result > 0:
            return jsonify(result=1, msg='Success')
        else:
            msg = get_error_msg(result)
            return jsonify(result=-1, msg=msg)
        
    fee_type = request.args.get('type')       
    if fee_type is not None:
        if fee_type.isdigit() == False:
            return redirect(url_for('admin.fee_config'))
        else:        
            _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])   
            result = _db_process.admin_get_list_fee()
            filterData = list(filter(lambda x : x['type'] == int(fee_type), result))
            return render_template('admin/fee_config.html', list_data=filterData, type=fee_type)
                       
    return render_template('admin/fee_config.html')


@admin_controller.route("/fee", methods=['GET', 'POST'])
@login_required(role="ADMIN")
def fee():
    if request.method == 'POST':
        kwargs = type('Dummy', (object,), { "type": request.form.get("type"),
                                           "data": json.loads(request.form.get("data"))})
        
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        
        result = _db_process.admin_insert_update_fee(kwargs)
        
        if result > 0:
            return jsonify(result=1, msg='Success')
        else:
            msg = get_error_msg(result)
            return jsonify(result=-1, msg=msg)                   
    return render_template('admin/fee.html')


@admin_controller.route("/list_fee", methods=['POST'])
@login_required(role="ADMIN")
def list_fee(): 
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])   
    result = _db_process.admin_get_list_fee()
    return jsonify(data=result)


@admin_controller.route("/currency-rate", methods=['GET', 'POST'])
@login_required(role="ADMIN")
def currency_rate():
    if request.method == 'POST':
        form_dic = request.form.to_dict()
        kwargs = collections.namedtuple("OjbDic", form_dic.keys())(*form_dic.values())
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        
        result = _db_process.admin_insert_update_currency(kwargs)
        if result >= 0:
            return jsonify(result=1, msg='Success')
        else:
            msg = get_error_msg(result)
            return jsonify(result=-1, msg=msg)                   
    return render_template('admin/currency_rate.html')


@admin_controller.route("/list_currency", methods=['POST'])
@login_required(role="ADMIN")
def list_currency(): 
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])   
    result = _db_process.admin_get_list_currency()
    return jsonify(data=result)


@admin_controller.route("/deposit", methods=['GET', 'POST'])
@login_required(role="ADMIN")
def deposit():
    if request.method == 'POST':
        form_dic = request.form.to_dict()
        kwargs = collections.namedtuple("OjbDic", form_dic.keys())(*form_dic.values())
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        
        result = _db_process.admin_insert_update_deposit(kwargs)
        if result >= 0:
            return jsonify(result=1, msg='Success')
        else:
            msg = get_error_msg(result)
            return jsonify(result=-1, msg=msg)                   
    return render_template('admin/deposit.html')


@admin_controller.route("/create-user", methods=['GET', 'POST'])
@login_required(role="ADMIN,MOD")
def create_user():
    form = CreateUserForm()
    if request.method == 'POST':    
        if form.validate_on_submit():
            urole = current_user.urole
            created_user_role = get_user_role(form.usertype.data)
            if(created_user_role == "MOD" and urole != "ADMIN"):
                return jsonify(result=-1, msg='Bạn không đủ quyền để tạo loại tài khoản này')           
                
            hashPass = hashPassword(form.password.data, form.email.data)
            _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
            result = _db_process.register(form.email.data, hashPass, form.usertype.data, form.mobile.data)                    
            if result > 0:
                return jsonify(result=1, msg='Success')
            else:
                 return jsonify(result=-1, msg=get_error_msg(result))
             
    return render_template('admin/create_user.html', form=form)


@admin_controller.route("/edit-user", methods=['GET', 'POST'])
@login_required(role="ADMIN,MOD")
def edit_user():
    if request.method == 'POST':
        return jsonify(result=1, msg='Success')     
    
    uid = request.args.get('id')
    if(uid is None or is_not_blank(uid) == False):
        return redirect(url_for('admin.list_user'))
      
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    result = _db_process.get_user_info(uid)
    return render_template('admin/edit_user.html', user=result)


@admin_controller.route("/list-user", methods=['GET', 'POST'])
@login_required(role="ADMIN,MOD")
def list_user():
    if request.method == 'POST':
        limit = 10
        offset = (int(request.form.get("page")) - 1) * limit;
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        args = type('Dummy', (object,), {"offset": offset, "limit": limit})
        if(request.form.get("type") is not None and is_not_blank(request.form.get("type"))):
            args.type = request.form.get("type")
        if(request.form.get("email") is not None and is_not_blank(request.form.get("email"))):
            args.email = request.form.get("email")
            
        userData = _db_process.get_list_user(args)
        return jsonify(data=userData[0], total=userData[1], limit=limit)

    return render_template('admin/list_user.html')


@admin_controller.route("/list-order", methods=['GET', 'POST'])
@login_required(role="ADMIN,MOD,ASSIST,BUYER,SHIPPER")
def list_order():
    if request.method == 'POST':
        limit = 10
        offset = (int(request.form.get("page")) - 1) * limit;
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        args = type('Dummy', (object,), {"offset": offset, "limit": limit, "admin": 1})
        if(request.form.get("status") is not None and is_not_blank(request.form.get("status"))):
            args.status = request.form.get("status")
        if(request.form.get("order_code") is not None and is_not_blank(request.form.get("order_code"))):
            args.order_code = request.form.get("order_code")
        
        if(request.form.get("from_time") is not None and is_not_blank(request.form.get("from_time"))):
            args.from_time = request.form.get("from_time")
        if(request.form.get("to_time") is not None and is_not_blank(request.form.get("to_time"))):
            args.to_time = request.form.get("to_time")       
        result = _db_process.get_list_order(args)
        return jsonify(data=result[0], total=result[1], limit=limit)
    
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    list_fee = _db_process.admin_get_list_fee()    
    return render_template('admin/list_order.html', list_fee=json.dumps(list_fee))


@admin_controller.route("/order-detail", methods=['GET'])
@login_required(role="ADMIN,MOD,ASSIST,BUYER,SHIPPER")
def order_detail():
    order_code = request.args.get('code')
    if order_code is None:
        return redirect(url_for('admin.index', msg='code empty'))
    order_array = order_code.split(".")
    if len(order_array) != 2:
        return redirect(url_for('admin.index', msg='code invalid'))
    
    kwargs = type('Dummy', (object,), { "id": order_array[1],
                                           "code": order_array[0]})
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    order_info = _db_process.get_order_info(kwargs)
    if order_info is None:
        return redirect(url_for('admin.index', msg='order null'))
    
    order_detail_id_array = order_info['order_item'].split(',')
    order_detail = _db_process.get_order_detail(order_detail_id_array)
    list_fee = _db_process.admin_get_list_fee()
    return render_template('admin/order_detail.html', order=order_info, detail=order_detail, list_fee=json.dumps(list_fee))


@admin_controller.route("/update-order-detail", methods=['POST'])
@login_required(role="ADMIN,MOD,ASSIST")
def update_order_detail():
    form_dic = request.form.to_dict()
    for key in form_dic.keys():
        if form_dic[key] is None or form_dic[key] == '':
            return jsonify(result=-600, msg=get_error_msg(-600))
    
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    list_currency_rate = _db_process.admin_get_list_currency()
    
    filterData = list(filter(lambda x : x['id'] == int(form_dic['p_currency']), list_currency_rate))
    if not len(filterData):
        return jsonify(result=-99, msg=get_error_msg(-99))
    
    currency_rate = filterData[0]['rate'] 
    item_price_vnd = float(form_dic['p_price']) * currency_rate * int(form_dic['p_quantity'])
    form_dic['p_vnd_price'] = item_price_vnd
    order_info = _db_process.get_order_from_detail_id(form_dic['id'])
    if(order_info is None):
        return jsonify(result=-102, msg=get_error_msg(-102))
    
    order_detail = _db_process.get_order_detail([form_dic['id']])
    
    form_dic['price_vnd'] = int(order_info['price_vnd']) - int(order_detail[0]['p_vnd_price']) + int(item_price_vnd)
    form_dic['order_id'] = order_info['id']
    _db_process.admin_update_order_detail(form_dic)
    return jsonify(result=1, msg='Success')


@admin_controller.route("/update-order", methods=['POST'])
@login_required(role="ADMIN,MOD,ASSIST,BUYER,SHIPPER")
def update_order():
    status = int(request.form.get("status"))
    order_id = request.form.get("id")
    if order_id is None or order_id == '':
        return jsonify(result=-600, msg=get_error_msg(-600))

    urole = current_user.urole
     
    if status < 0 or status > 9:
        return jsonify(result=-600, msg=get_error_msg(-600))
    
    if urole == 'BUYER':
        if status != 3 and status != 4:
            return jsonify(result=-103, msg=get_error_msg(-103))
        kwargs = type('Dummy', (object,), { "status": status, "id": order_id})
        
    elif urole == 'SHIPPER':
        if status != 6 and status != 7:
            return jsonify(result=-103, msg=get_error_msg(-103))
        kwargs = type('Dummy', (object,), { "status": status, "id": order_id})
    else:
        user_deposit = int(request.form.get("user_deposit"))
        total_weight = float(request.form.get("total_weight"))
        final_price = int(request.form.get("final_price"))
        if(user_deposit < 0 or total_weight < 0 or final_price < 0):
            return jsonify(result=-600, msg=get_error_msg(-600))
        kwargs = type('Dummy', (object,), { "status": status, "user_deposit" : user_deposit, "total_weight": total_weight, "final_price": final_price, "id": order_id})
    
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
    result = _db_process.admin_update_order(kwargs)
    return jsonify(result=1, msg='Success')


@admin_controller.route("/list_deposit", methods=['POST'])
@login_required(role="ADMIN")
def list_deposit(): 
    _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])   
    result = _db_process.admin_get_list_deposit()
    return jsonify(data=result)


@admin_controller.route("/recharge", methods=['GET', 'POST', 'PUT'])
@login_required(role="ADMIN,MOD")
def recharge():
    if request.method == 'POST':
        email = request.form.get("email")
        if not(email):
            return jsonify(result=-600, msg=get_error_msg(-600))
        
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        result = _db_process.get_user_info_by_email(email)
        if result is None:
            return jsonify(result=-106, msg=get_error_msg(-106))
        return jsonify(result=1, msg='Success', user=result)
    
    elif request.method == 'PUT':
        email = request.form.get("email")
        if not(email):
            return jsonify(result=-600, msg=get_error_msg(-600))
        total = request.form.get("total")
        if not(total):
            return jsonify(result=-600, msg=get_error_msg(-600))
        
        _db_process = DatabaseProcess(current_app.config['DB_CONNECTSTRING'])
        kwargs = type('Dummy', (object,), { "email": email, "total": total})
        result =  _db_process.admin_topup_user(kwargs)
        return jsonify(result=1, msg='Success')
    
    return render_template('admin/recharge.html')
        
