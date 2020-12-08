from flask import current_app, session, flash, request, url_for, redirect
from functools import wraps
from flask_login import current_user, logout_user
from ast import literal_eval

import random, string
import hashlib
import logging
import logging.handlers

def hashPassword(password, user_name):
    string_to_hash = password + user_name + '!@#$%^&*()%^$&#'
    hash_object = hashlib.sha512(str(string_to_hash).encode('utf-8')).hexdigest()
    return hash_object

def login_required(role="ANY"):
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                logout_user()
                session.clear()
                return current_app.login_manager.unauthorized()
            urole = current_user.urole
            if ((urole not in role) and (role != "ANY")):   
                            
                if(request.path.startswith('/admin')):                   
                    flash('Bạn không có quyền sử dụng chức năng này');
                    return redirect(url_for('admin.index'))
                
                logout_user()
                session.clear()
                return current_app.login_manager.unauthorized()      
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper

def get_user_role(role):
    switcher = { 
        0: "USER", 
        1: "ADMIN", 
        2: "MOD",
        3: "ASSIST",
        4: "BUYER",
        5: "SHIPPER"
    }
    return switcher.get(role, "USER")

# (1,2,3) => ['1','2','3']
def db_get_values_to_array(str_db_value):
    for ch in [' ', '(', ')']:
        if ch in str_db_value:
            str_db_value = str_db_value.replace(ch, '')
    
    return str_db_value.split(',')


#-100:tk da ton tai trong he thong
def get_error_msg(code):
    switcher = { 
        -100: "Tài khoản đã tồn tại trong hệ thống",
        -101: "Mật khẩu cũ không đúng",
        -102: "Đơn hàng không tồn tại",
        -103: "Bạn không có quyền cập nhật đơn hàng sang trạng thái này",
        -104: "Tài khoản của bạn đang bị khóa",
        -105: "Tài khoản hoặc mật khẩu không đúng",
        -106: "Tài khoản không tồn tại trong hệ thống",
        -107: "Số dư không đủ để thực hiện giao dịch",
        -600: "Dữ liệu đầu vào không hợp lệ"
    }
    return switcher.get(code, "Hệ thống đang bận, vui lòng thử lại sau")

def randomstring(length):
   letters = string.ascii_uppercase
   return ''.join(random.choice(letters) for i in range(length))
def is_not_blank(s):
    return bool(s and s.strip())

def get_logger(filename='', name=''):
    log_file_name = filename
    logging_level = logging.DEBUG
    # set TimedRotatingFileHandler for root
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
    # use very short interval for this example, typically 'when' would be 'midnight' and no explicit interval
    handler = logging.handlers.TimedRotatingFileHandler(log_file_name, when='midnight', backupCount=10)
    handler.suffix = "%Y-%m-%d"

    handler.setFormatter(formatter)
    logger = logging.getLogger(name)  # or pass string to give it a name
    logger.addHandler(handler)
    logger.setLevel(logging_level)
    return logger


