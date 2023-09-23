from flask import *
from flask_ckeditor import CKEditor

import config
import decorators
from extensions import *
from model import *
from blueprints.qa import bp as qa_bp
from blueprints.auth import bp as auth_bp
from blueprints.monitor import bp as mnt_bp
from blueprints.backstage import bp as bs_bp
from blueprints.settings import bp as s_bp
from blueprints.mail import bp as mail_bp
from blueprints.others import bp as others_bp
from blueprints.register import bp as reg_bp
from blueprints.charts import bp as ch_bp
from blueprints.collect import bp as coll_bp
from blueprints.detect import bp as det_bp
from flask_migrate import *

app = Flask(__name__)
app.config.from_object(config)  # 绑定配置文件
app.register_blueprint(qa_bp)
app.register_blueprint(mnt_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(bs_bp)
app.register_blueprint(s_bp)
app.register_blueprint(mail_bp)
app.register_blueprint(others_bp)
app.register_blueprint(reg_bp)
app.register_blueprint(ch_bp)
app.register_blueprint(coll_bp)
app.register_blueprint(det_bp)

db.init_app(app)
migrate = Migrate(app, db)

ckeditor = CKEditor(app)


@app.before_request
def before_request():
    """在每一次请求之前 先设置全局变量g的属性值"""
    g.name = None
    if session.__contains__('admin_name'):
        admin_name = session["admin_name"]
        g.name = admin_name
    # if admin_name:  # 如果session中存在用户信息
    #     print('session存在用户信息')


@app.route('/')
def index():  # put application's code here
    if session:
        admin_name = session.get('admin_name')
        # print(admin_name, g, session['admin_name'])
        return render_template('404.html', admin_name=g.name)
    else:
        print('没有session')
        return redirect(url_for('auth.login'))


@app.errorhandler(404)
def page_not_found(err):
    return render_template('404.html', admin_name=g.name)


@app.errorhandler(500)
def internal_server_error(err):
    return render_template('500.html')


if __name__ == '__main__':
    app.run()
