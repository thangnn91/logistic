from flask import Flask, render_template, url_for, redirect, session
from flask_wtf.csrf import CsrfProtect
from datetime import timedelta
from flask_login import LoginManager, login_manager
from functools import wraps
from app.model import user_model

import logging
import logging.handlers
import os
import sys

app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)
from app.server.user_controllers import user_controller as user_module
app.register_blueprint(user_module)

from app.server.admin_controllers import admin_controller as admin_module
app.register_blueprint(admin_module)

from app.server.api_controller import api_controller as api_module
app.register_blueprint(api_module)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "Vui lòng đăng nhập để sử dụng chức năng"
login_manager.login_view = "user.signin"

formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')
handler = logging.handlers.TimedRotatingFileHandler('logs.log', when='midnight', backupCount=10)
handler.suffix = "%Y-%m-%d"
handler.setFormatter(formatter)
app.logger.setLevel(logging.WARNING)
app.logger.addHandler(handler)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

    
@login_manager.user_loader
def load_user(user_id):   
    return user_model.User(user_id, session.get('user_name'), session.get('role'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')
