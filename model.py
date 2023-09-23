from extensions import db
from datetime import datetime


class AdminModel(db.Model):
    __tablename__ = 'admin'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)
    phone_num = db.Column(db.String(100), nullable=False, unique=True)
    company = db.Column(db.String(100), nullable=False)
    edu_bg = db.Column(db.String(100), nullable=False)
    skill = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    sentence = db.Column(db.String(100), nullable=False)
    salary = db.Column(db.String(100), nullable=False)


class ResidentModel(db.Model):
    __tablename__ = 'resident'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), nullable=False)
    is_holder = db.Column(db.Boolean, nullable=False)
    phone_num = db.Column(db.String(20), nullable=False)
    building = db.Column(db.Integer, nullable=False)
    room = db.Column(db.Integer, nullable=False)
    workplace = db.Column(db.String(100), nullable=False)
    le = db.Column(db.String(3), nullable=False)
    photo = db.Column(db.String(100), nullable=False)


class VisitorModel(db.Model):
    __tablename__ = 'visitor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(12), nullable=False)
    reason = db.Column(db.Text)
    phone_num = db.Column(db.String(20), nullable=False)
    visit_time = db.Column(db.DateTime, default=datetime.now)
    le_type = db.Column(db.String(2), nullable=False)  # 0 leave, 1 enter
    photo = db.Column(db.String(100), nullable=False)


class CaptchaModel(db.Model):
    # 给指定邮箱发邮件，物业经理拿着这个验证码给保安注册，验证码与手机号绑定
    __tablename__ = 'captcha'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone_num = db.Column(db.String(100), nullable=False)
    captcha = db.Column(db.String(100), nullable=False)


class CarModel(db.Model):
    __tablename__ = 'car'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vp = db.Column(db.String(12), nullable=False)  # vehicleplate
    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey("resident.id"), nullable=False)
    # 关系
    owner = db.relationship(ResidentModel, backref='cars')


class TempVehicleModel(db.Model):
    __tablename__ = 'temp_vehicle'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vp = db.Column(db.String(12), nullable=False)  # vehicleplate
    # 外键
    owner_id = db.Column(db.Integer, db.ForeignKey("visitor.id"), nullable=False)
    owner = db.relationship(VisitorModel, backref='temp_vehicles')


class EmailModel(db.Model):
    __tablename__ = 'email'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    is_trash = db.Column(db.Boolean, nullable=False)
    is_important = db.Column(db.Boolean, nullable=False)
    is_read = db.Column(db.Boolean, nullable=False)
    is_draft = db.Column(db.Boolean, nullable=False)

    sender_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    receiver_id = db.Column(db.Integer, nullable=False)

    sender = db.relationship(AdminModel, backref='emails')


class AnnouncementModel(db.Model):
    __tablename__ = 'announcement'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)


class PARecordModel(db.Model):
    __tablename__ = 'parecord'  # person access record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    person_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(12), nullable=False)
    person_type = db.Column(db.String(2), nullable=False)  # 0 visitor, 1 resident
    le_type = db.Column(db.String(2), nullable=False)  # 0 leave, 1 enter
    time = db.Column(db.DateTime, default=datetime.now)


class VARecordModel(db.Model):
    __tablename__ = 'varecord'  # vehicle access record
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    vehicle_id = db.Column(db.Integer, nullable=False)
    vp = db.Column(db.String(12), nullable=False)
    vehicle_type = db.Column(db.String(2), nullable=False)  # 0 visitor, 1 resident
    le_type = db.Column(db.String(2), nullable=False)  # 0 leave, 1 enter
    time = db.Column(db.DateTime, default=datetime.now)


class MapMarkModel(db.Model):
    __tablename__ = 'mapmark'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    long = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    lat = db.Column(db.Numeric(precision=9, scale=6), nullable=False)
    content = db.Column(db.String(100), nullable=False)