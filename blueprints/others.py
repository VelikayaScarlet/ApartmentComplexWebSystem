import json
import time

import requests
from flask import *
from flask_ckeditor import *

from decorators import *
from .forms import *
from werkzeug.security import *

bp = Blueprint('others', __name__, url_prefix='/others')


@bp.route('/profile')
@login_required
def profile():
    admin = AdminModel.query.filter_by(name=g.name).first()
    return render_template("d_profile.html", admin=admin)


@bp.route('/lockscreen', methods=['POST', 'GET'])
@login_required
def lockscreen():
    if request.method == 'GET':
        return render_template("d_lockscreen.html")
    else:
        form = PasswordForm(request.form)
        password = form.password.data
        admin = AdminModel.query.filter_by(name=g.name).first()
        if check_password_hash(admin.password, password):
            return redirect(url_for('qa.index'))
        else:
            return render_template("d_lockscreen.html", error_msg='密码错误')


@bp.route('/announce', methods=['GET', 'POST'])
@login_required
def announce():
    form = AnnounceForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        A = AnnouncementModel(title=title, content=content)
        db.session.add(A)
        db.session.commit()
        return redirect(url_for('others.announcement'))
    return render_template('f_announce.html', form=form)


@bp.route('/announcement')
#  @login_required
def announcement():
    announcements = AnnouncementModel.query.order_by(AnnouncementModel.create_time.desc()).all()
    return render_template('f_announcement.html', announcement=announcements)


@bp.route('/announcement_bs')
@login_required
def announcement_bs():
    announcements = AnnouncementModel.query.order_by(AnnouncementModel.create_time.desc()).all()
    return render_template('f_announcement_bs.html', announcement=announcements)


@bp.route('/announcement_delete/<a_id>')
@login_required
def announcement_delete(a_id):
    a = AnnouncementModel.query.filter_by(id=a_id).first()
    db.session.delete(a)
    db.session.commit()
    return redirect(url_for('others.announcement_bs'))


@bp.route('/announcement_search/', methods=['POST', 'GET'])
@login_required
def announcement_search():
    ctt = request.form.get('ctt')
    print(ctt)
    if ctt is None:
        ctt = ''
    a = AnnouncementModel.query.order_by(AnnouncementModel.id).all()
    a_list = []
    for r in a:
        if ctt in str(r.id) or ctt in r.content or ctt in str(r.create_time) or ctt in r.title:
            a_list.append(r)
    return render_template('f_announcement_bs.html', announcement=a_list)


@bp.route('/announcement_view/<announcement_id>')
@login_required
def announcement_view(announcement_id):
    a = AnnouncementModel.query.filter_by(id=announcement_id).first()
    return render_template('f_announcement_view.html', a=a)


@bp.route('/calendar')
@login_required
def calendar():
    return render_template('e_calendar.html')


@bp.route('/info_today')
@login_required
def info_today():
    return render_template('f_info_today.html')


@bp.route('/info_history')
@login_required
def info_history():
    return render_template('f_info_history.html')


@bp.route('/mapmarks2json')
def mapmarks2json():
    mms = MapMarkModel.query.order_by(MapMarkModel.id).all()
    jmms = [
        {
            'id': mm.id,
            'long': mm.long,
            'lat': mm.lat,
            'content': mm.content
        }
        for mm in mms
    ]
    print(jmms)
    return json.dumps(jmms, ensure_ascii=False)


@bp.route('/leaflet_map', methods=['POST', 'GET'])
@login_required
def leaflet_map():
    return render_template('f_leaflet.html')


@bp.route('/map_add_mark', methods=['POST', 'GET'])
@login_required
def map_add_mark():
    if request.method == 'GET':
        return redirect(url_for('others.leaflet_map'))
    else:
        long = request.form.get('longitude')
        lat = request.form.get('latitude')
        content = request.form.get('content')
        mm = MapMarkModel.query.filter_by(long=long, lat=lat).first()
        if mm is None:
            mm = MapMarkModel(long=long, lat=lat, content=content)
            db.session.add(mm)
            db.session.commit()
        return redirect(url_for('others.leaflet_map'))


@bp.route('/map_delete_mark', methods=['POST', 'GET'])
@login_required
def map_delete_mark():
    if request.method == 'GET':
        return redirect(url_for('others.leaflet_map'))
    else:
        long = request.form.get('longitudedelete')
        lat = request.form.get('latitudedelete')
        mm = MapMarkModel.query.filter_by(long=long, lat=lat).first()
        print(mm)
        db.session.delete(mm)
        db.session.commit()
        return redirect(url_for('others.leaflet_map'))
