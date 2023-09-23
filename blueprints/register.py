import base64
import os
from datetime import date
import shutil

import requests
from flask import *
from sqlalchemy import false, true

from blueprints.forms import *
from blueprints.monitor import get_vp_str

bp = Blueprint('register', __name__, url_prefix='/register')


# 不是注册，是登记
@bp.route('/visitor_reg', methods=['POST', 'GET'])
def visitor_reg():
    if request.method == 'GET':
        return render_template('e_visitor_reg.html')
    else:
        form = VisitorRegForm(request.form)
        name = form.name.data
        reason = form.reason.data
        phone_num = form.phone_num.data

        source = r"C:\Users\79433\Downloads"
        dest = r"D:\Debugs\backend\static\photos\visitor"

        today = datetime.now()
        day = today.day
        filename = name+str(phone_num)[-4:]
        source_path = os.path.join(source, filename)
        dest_path = os.path.join(dest, filename)
        shutil.move(source_path, dest_path)
        print('已经将'+source_path+'挪到了'+dest_path)
        visitor = VisitorModel(name=name, reason=reason, phone_num=phone_num, photo=filename, le_type='没走')
        db.session.add(visitor)
        v = VisitorModel.query.order_by(VisitorModel.visit_time.desc()).first()
        r = PARecordModel(name=v.name, time=v.visit_time, le_type='入', person_type='访客', person_id=v.id)
        db.session.add(r)
        db.session.commit()
        return render_template('e_visitor_reg.html', msg='登记成功')


@bp.route('/vehicle_reg', methods=['POST', 'GET'])
def vehicle_reg():
    visitors = VisitorModel.query.order_by(VisitorModel.visit_time.desc()).all()
    if request.method == 'GET':
        vp = get_vp_str()
        if len(vp) > 0:
            return render_template('e_vehicle_reg.html', visitors=visitors,  vp=vp)
        else:
            return render_template('e_vehicle_reg.html', visitors=visitors, msg='未检测到车牌')
    else:
        form = TempVehicleForm(request.form)
        print(type(form))
        name = form.name.data
        vp = form.vp.data
        # 思路：在前端填写的是车主姓名和车牌号，后端根据车主姓名生成ID
        owner = VisitorModel.query.filter_by(name=name).first()
        print(owner)
        if owner is not None:
            temp_vehicle = TempVehicleModel(vp=vp, owner_id=owner.id)
            db.session.add(temp_vehicle)
            db.session.commit()
            return render_template('e_vehicle_reg.html', msg='登记成功')
        else:
            return render_template('e_vehicle_reg.html', msg='无此访客，请先登记访客，再登记其车辆')


@bp.route('/resident_reg', methods=['POST', 'GET'])
def resident_reg():
    if request.method == 'GET':
        return render_template('e_resident_reg.html')
    else:
        form = ResidentRegForm(request.form)
        name = form.name.data
        ih = request.form.get("is_holder")
        phone_num = form.phone_num.data
        bd = form.building.data
        room = form.room.data
        wp = form.workplace.data
        resident = ResidentModel(name=name, is_holder=bool(ih),
                                 phone_num=phone_num, building=bd, room=room, workplace=wp, le='未外出')
        db.session.add(resident)
        db.session.commit()
        return render_template('e_resident_reg.html', msg='登记成功')


@bp.route('/car_reg', methods=['POST', 'GET'])
def car_reg():
    residents = ResidentModel.query.order_by(ResidentModel.id).all()
    if request.method == 'GET':
        vp = get_vp_str()
        if len(vp) > 0:
            return render_template('e_car_reg.html', residents=residents, vp=vp)
        else:
            return render_template('e_car_reg.html', residents=residents, msg='未检测到车牌')
    else:
        form = TempVehicleForm(request.form)
        name = form.name.data
        vp = form.vp.data
        # 思路：在前端填写的是车主姓名和车牌号，后端根据车主姓名生成ID
        # 未处理重名问题，只会盲目搜第一个，有空处理
        owner = ResidentModel.query.filter_by(name=name).first()
        if owner is not None:
            car = CarModel(vp=vp, owner_id=owner.id)
            db.session.add(car)
            db.session.commit()
            return render_template('e_car_reg.html', error_msg='登记成功')
        else:
            return render_template('e_car_reg.html', error_msg='出错')
