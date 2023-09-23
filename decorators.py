import time
from functools import wraps
from flask import *


def login_required(func):
    # 保留func的信息
    @wraps(func)
    def inner(*args, **kwargs):
        admin = session.get('admin_id')
        if admin:
            print('已进入登录状态')
            return func(*args, **kwargs)
        else:
            return redirect(url_for('auth.login'))
    return inner



