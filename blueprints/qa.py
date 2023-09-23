from flask import *
from sqlalchemy.orm import relationship
from model import *
from decorators import *

bp = Blueprint('qa', __name__, url_prefix='/qa')


@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    #  最近五条出入记录
    latest_ann = AnnouncementModel.query.order_by(AnnouncementModel.create_time.desc()).first()
    five_parecord = PARecordModel.query.filter(PARecordModel.person_type != '访客').order_by(PARecordModel.time.desc()).limit(5).all()
    five_parecord_visitor = PARecordModel.query.filter_by(person_type='访客').order_by(PARecordModel.time.desc()).limit(5).all()
    five_resident = []
    five_visitor = []

    for fp, fpv in zip(five_parecord, five_parecord_visitor):
        aim_resident = ResidentModel.query.filter_by(name=fp.name, id=fp.person_id).first()
        aim_visitor = VisitorModel.query.filter_by(name=fpv.name, id=fpv.person_id).first()
        print(five_resident, five_visitor)
        if aim_resident is not None:
            five_resident.append(aim_resident.phone_num[-4:])
        else:
            five_resident.append('unknown')

        if aim_visitor is not None:
            five_visitor.append(aim_visitor.phone_num[-4:])
        else:
            five_visitor.append('unknown')
    return render_template('b_index.html', fr=five_parecord, fp=five_resident,
                           fv=five_visitor, la=latest_ann, fpv=five_parecord_visitor)





