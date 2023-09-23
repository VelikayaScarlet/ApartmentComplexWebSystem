import time

import requests
from flask import *

from model import *
from .forms import *
from werkzeug.security import *

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        print('get')
        return render_template('b_login.html')
    else:
        print('post')
        form = LoginForm(request.form)
        if form.validate():
            name = form.name.data
            password = form.password.data
            admin = AdminModel.query.filter_by(name=name).first()
            if not admin:
                print('无此用户', form.errors)
                return render_template('b_login.html', error_msg='无此用户')
                # return redirect(url_for('auth.login', error_msg='无此用户'))
            if check_password_hash(admin.password, password):
                print(name, password, '登陆成功')
                session['admin_name'] = admin.name
                session['admin_id'] = admin.id
                print(admin.name, admin.id)
                g.id = admin.id
                g.name = admin.name
                return redirect(url_for('qa.index', admin_name=name))
            else:
                print('用户名或密码错误')
                # return redirect(url_for('auth.login', error_msg='用户名或密码错误'))
                return render_template('b_login.html', error_msg='用户名或密码错误')
        else:
            print(form.errors)
            # return redirect(url_for('auth.login', error_msg='用户名或密码格式错误'))
            return render_template('b_login.html', error_msg='用户名或密码格式错误')


@bp.route('/recruit', methods=['GET', 'POST'])
def recruit():
    if request.method == 'GET':
        # time.sleep(0.2)
        return render_template('b_recruit.html', form=RecruitForm())  # 要加上form = RecruitForm()前台才能识别到form.errors
    else:
        form = RecruitForm(request.form)
        if form.validate():
            password = form.password.data
            phone_num = form.phone_num.data
            strpn = str(phone_num)
            cut = strpn[7:11]
            list = []
            for i in cut:
                list.append(strpn[int(i)])
            suffix = "".join(list)
            name = 'admin' + str(suffix)

            admin = AdminModel(name=name, password=generate_password_hash(password), phone_num=phone_num)
            db.session.add(admin)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print(form.errors)
            return redirect(url_for('auth.recruit'))


@bp.route('/forget', methods=['GET', 'POST'])
def forget():
    print('forget')
    if request.method == 'GET':
        return render_template('b_forget.html')
    else:
        form = ForgetForm(request.form)
        if form.validate():
            captcha = form.captcha.data
            phone_num = form.phone_num.data
            admin = CaptchaModel.query.filter_by(captcha=captcha, phone_num=phone_num).first()
            print(admin)
            if not admin:
                print('无此用户')
                print(form.errors)
                return render_template('b_forget.html', error_msg='无此用户或验证码输入错误')
            else:
                # return render_template('b_confirm.html', phone_num=phone_num)
                return redirect(url_for('auth.confirm', phone_num=phone_num))
        else:
            print(form.errors)
            # return redirect(url_for('auth.forget', error_msg='手机号或验证码格式错误'))
            return render_template('b_forget.html', error_msg='手机号或验证码格式错误')


@bp.route('/confirm?phone_num=<phone_num>', methods=['GET', 'POST'])
def confirm(phone_num):
    print(phone_num)
    if request.method == 'GET':
        return render_template('b_confirm.html')
    else:
        form = ConfirmForm(request.form)
        if form.validate():
            password = form.password.data
            # confirm = form.confirm.data
            admin = AdminModel.query.filter_by(phone_num=phone_num).first()
            admin.password = generate_password_hash(password)
            db.session.commit()
            return redirect(url_for('auth.login'))
        else:
            print('两次输入的密码不同')
            return render_template('b_confirm.html', error_msg='两次输入的密码不同')


@bp.route('/logout')
def logout():
    # session.clear()
    return redirect(url_for('auth.login'))
