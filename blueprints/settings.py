import time

import requests
from flask import *
from .forms import *
from werkzeug.security import *

from .monitor import capture_photo

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/test')
def test():  # put application's code here
    return render_template('Test.html')


@bp.route('/blank')
def blank():  # put application's code here
    return render_template('base.html')


@bp.route('/200')
def test200():
    return render_template('200.html')


@bp.route('/404')
def test404():
    return render_template('404.html')


@bp.route('/500')
def test500():
    return render_template('500.html')
