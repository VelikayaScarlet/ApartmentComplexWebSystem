import sys
from datetime import timedelta
import dlib
import imutils
from flask import *
import cv2
from scipy.spatial import distance
from imutils import face_utils

from model import *
from paddleocr import PaddleOCR
from blueprints.collect import detect_face

bp = Blueprint('monitor', __name__, url_prefix='/monitor')
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor('D:/Debugs/backend/face_recognition/models/shape_predictor_68_face_landmarks.dat')
eye_aspect_ratio_thresh = 0.25
eye_aspect_CF = 3


def gen_monitor1():
    vc = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    while True:
        ret, frame = vc.read()
        if not ret:
            return render_template('500.html')
        image = cv2.imencode('.jpg', frame)[1].tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + image + b'\r\n')


@bp.route('/monitor1')
def monitor1():
    return render_template('b_monitor1.html')
    # return render_template('b_monitor1.html', response=Response(gen_monitor1(),
    # mimetype='multipart/x-mixed-replace; ''boundary=frame'))


@bp.route('/c_monitor1')
def c_monitor1():
    return Response(gen_monitor1(), mimetype='multipart/x-mixed-replace; boundary=frame')


def eye_aspect_ratio(eye):
    # 计算垂直方向的两个坐标点之间的欧几里得距离
    a = distance.euclidean(eye[1], eye[5])
    b = distance.euclidean(eye[2], eye[4])
    # 计算水平方向的坐标点之间的欧几里得距离
    c = distance.euclidean(eye[0], eye[3])
    # 计算纵横比
    ear = (a + b) / (2.0 * c)
    return ear


def detect_biometrics():
    wait = 0
    biometrics = 0
    msg = '异常'
    (lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS['left_eye']
    (rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS['right_eye']
    camera = cv2.VideoCapture(0)
    while True:
        print('wait: ' + str(wait))
        print('biometrics: ' + str(biometrics))
        ret, frame = camera.read()
        frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dets = detector(gray, 0)
        for d in dets:
            shape = predictor(gray, d)
            shape = face_utils.shape_to_np(shape)
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)  # 计算纵横比
            rightEAR = eye_aspect_ratio(rightEye)
            EAR = (leftEAR + rightEAR) / 2
            if EAR < eye_aspect_ratio_thresh:
                cv2.putText(frame, 'BIOMETRICS DETECTED', (30, 50),
                            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
                biometrics += 1
                if biometrics == 1:
                    msg = '检测到生物特征'
                    camera.release()
                    cv2.destroyAllWindows()
                    return msg
            else:
                if wait == 8:
                    msg = '非活体攻击'
                    camera.release()
                    cv2.destroyAllWindows()
                    return msg
                else:
                    wait += 1
                    continue
        cv2.imshow('Video', frame)
        key = cv2.waitKey(10)
        if key == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()
    return msg


@bp.route('/detect_face_here')
def detect_face_here():
    return render_template('c_detect_face_here.html')


@bp.route('/detect_face_profile/<info>')
def detect_face_profile(info):
    # info = Kotsky1234 [:-4][-4:]
    name = info[:-4]
    tail = info[-4:]
    print(name, tail)
    visitor = db.session.query(VisitorModel).filter(VisitorModel.name == name, tail == VisitorModel.phone_num[-4:]).all()
    resident = db.session.query(ResidentModel).filter(ResidentModel.name == name, tail == ResidentModel.phone_num[-4:]).all()
    if len(resident) > 0:
        person = resident[0]
    else:
        person = visitor[0]
    return render_template('c_detect_face_profile.html', person=person, info=info)


@bp.route('/detect_face_le/<le_type>')
def detect_face_le(le_type):
    result = '未知人员'
    known = 0
    unknown = 0
    person = "未知人员0000"
    msg = detect_biometrics()
    if msg == '非活体攻击':
        return render_template('c_detect_face_here.html', msg='非活体攻击，停止检测')
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        if not ret:
            break
        result = detect_face(frame, 'resident')
        #  cv2.imshow('frame', frame)
        if result == '未知人员':
            unknown += 1
        else:
            known += 1
        if known >= 10 or unknown >= 10:
            break
    print(known, unknown)
    if known >= unknown:
        person = result
        name = person[0:-4]  # 考茨基
        tail = person[-4:]  # 3858
        id = 0
        resident = ResidentModel.query.filter_by(name=name).all()
        for i in resident:
            if i.phone_num[-4:] == tail:
                id = i.id
                break
        resident = ResidentModel.query.filter_by(id=id, name=name).first()
        if le_type == '入':
            resident.le = '未外出'
        else:
            resident.le = '已外出'
        r = PARecordModel(person_id=id, name=name, person_type='住户', le_type=le_type, time=datetime.now())
        last = PARecordModel.query.filter_by(name=name).order_by(PARecordModel.time.desc()).first()

        if last is not None and r.time - last.time < timedelta(seconds=15):
            msg = name
            print('已经写入一次了')
        else:
            db.session.add(r)
            db.session.commit()
            msg = name
    else:
        r = PARecordModel(person_id=0, name='未知人员', person_type='未知', le_type=le_type, time=datetime.now())
        db.session.add(r)
        db.session.commit()
        msg = '未知人员'
    if msg == '未知人员':
        return render_template('c_detect_face_here.html', msg='未知人员', )

    else:
        print(person)
        return render_template('c_detect_face_profile.html', info=person, person=r)


def capture_photo(file_path):
    camera = cv2.VideoCapture(0)
    if not camera.isOpened():
        print("无法打开摄像头")
        return
    ret, frame = camera.read()
    if not ret:
        print("无法读取图像")
        camera.release()
        return
    cv2.imwrite(file_path, frame)
    camera.release()
    print("照片已保存：", file_path)


def get_vp_str():
    ocr = PaddleOCR(use_angle_cls=True)
    capture_photo('D:/Debugs/backend/static/photos/vp/vp.png')
    img_path = 'D:/Debugs/backend/static/photos/vp/vp.png'
    result = ocr.ocr(img_path, cls=True)
    if result is not None:
        vp = result[0][0][1][0].replace("·", "")
        print(vp)
        return vp
    else:
        get_vp_str()


@bp.route('/detect_vp_in')
def detect_vp_in():
    vp = get_vp_str()
    car = db.session.query(CarModel).filter_by(vp=vp).first()
    tv = db.session.query(TempVehicleModel).filter_by(vp=vp).first()
    print(car, tv)
    if car is not None:
        r = db.session.query(ResidentModel).filter_by(id=car.owner_id).first()
        rec = VARecordModel(vehicle_id=car.id, vp=vp, vehicle_type='内部', le_type='入', time=datetime.now())
        db.session.add(rec)
        db.session.commit()
        return render_template('c_detect_vp_in.html', vp=vp, person=r)
    elif tv is not None:
        v = db.session.query(VisitorModel).filter_by(id=tv.owner_id).first()
        rec = VARecordModel(vehicle_id=tv.id, vp=vp, vehicle_type='外来', le_type='入', time=datetime.now())
        db.session.add(rec)
        db.session.commit()
        return render_template('c_detect_vp_in.html', vp=vp, person=v)
    else:
        return redirect(url_for('register.vehicle_reg', error_msg='未查询到该车辆，请先登记'))


@bp.route('/detect_vp_out')
def detect_vp_out():
    vp = get_vp_str()
    car = db.session.query(CarModel).filter_by(vp=vp).first()
    tv = db.session.query(TempVehicleModel).filter_by(vp=vp).first()
    print(car, tv)
    if car is not None:
        r = db.session.query(ResidentModel).filter_by(id=car.owner_id).first()
        rec = VARecordModel(vehicle_id=car.id, vp=vp, vehicle_type='内部', le_type='出', time=datetime.now())
        db.session.add(rec)
        db.session.commit()
        return render_template('c_detect_vp_in.html', vp=vp, person=r)
    elif tv is not None:
        v = db.session.query(VisitorModel).filter_by(id=tv.owner_id).first()
        rec = VARecordModel(vehicle_id=tv.id, vp=vp, vehicle_type='外来', le_type='出', time=datetime.now())
        visitor_rec = PARecordModel(person_id=v.id, person_type='访客', name=v.name, le_type='出', time=datetime.now())
        db.session.add(rec)
        db.session.delete(tv)
        #  db.session.delete(v)
        db.session.add(visitor_rec)
        #  车辆出去后，删除车辆的信息，然后创建一条访客的外出记录
        #  访客并不直接删除，而是在一段时间后批量删除（保留数据）
        db.session.commit()
        return render_template('c_detect_vp_in.html', vp=vp, person=v)
    else:
        return redirect(url_for('register.vehicle_reg', error_msg='未查询到该车辆，怎么进来的？'))


@bp.route('/detect_vp')
def detect_vp():
    return render_template('c_detect_vp.html')