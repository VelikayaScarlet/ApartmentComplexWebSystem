import glob

import numpy as np
import skimage
from flask import *
import cv2
import dlib
import os
from skimage import *

from extensions import db

bp = Blueprint('collect', __name__, url_prefix='/collect')

# 人脸关键点检测器
predictor_path = "D:/Debugs/backend/face_recognition/models/shape_predictor_68_face_landmarks.dat"
# 人脸识别模型、提取特征值
face_rec_model_path = "D:/Debugs/backend/face_recognition/models/dlib_face_recognition_resnet_model_v1.dat"
# 训练图像文件夹
faces_folder_path = 'D:\\Debugs\\backend\\static\\photos'

# 加载模型
detector = dlib.get_frontal_face_detector()
sp = dlib.shape_predictor(predictor_path)
facerec = dlib.face_recognition_model_v1(face_rec_model_path)

candidate = []  # 存放训练集人物名字
descriptors = []  # 存放训练集人物特征列表


def write_to_file(descriptor, name, person_type):
    fd = 'D:/Debugs/backend/face_recognition/'
    path = os.path.join(fd, "face_data", person_type, f"{name}.txt")
    with open(path, "w") as f:
        f.write(','.join(map(str, descriptor)))


def train(person_type):
    for f in glob.glob(os.path.join(faces_folder_path, person_type, "*.png")):
        print("正在处理: {}".format(f))
        img = skimage.io.imread(f)
        name = f.split('\\')[-1].split('.')[0]
        candidate.append(name)
        # 人脸检测
        dets = detector(img, 1)
        for k, d in enumerate(dets):
            shape = sp(img, d)
            # 提取特征
            face_descriptor = facerec.compute_face_descriptor(img, shape)
            v = np.array(face_descriptor)
            descriptors.append(v)
            write_to_file(v, name, person_type)
    print('识别训练完毕！')


def detect_face(img, person_type):
    dets = detector(img, 1)
    path = "face_data/" + person_type + "/"
    path = 'D:/Debugs/backend/face_recognition/face_data/' + person_type + "/"
    for file_name in os.listdir(path):
        name = os.path.splitext(file_name)[0]
        candidate.append(name)
        file_path = os.path.join(path, file_name)
        with open(file_path, "r"):
            descriptor = np.loadtxt(file_path, delimiter=',')
            descriptors.append(descriptor)
    dist = []
    for k, d in enumerate(dets):
        shape = sp(img, d)
        face_descriptor = facerec.compute_face_descriptor(img, shape)
        d_test = np.array(face_descriptor)
        for i in descriptors:  # 计算距离
            dist_ = np.linalg.norm(i - d_test)
            dist.append(dist_)

    # 训练集人物和距离组成一个字典
    c_d = dict(zip(candidate, dist))
    cd_sorted = sorted(c_d.items(), key=lambda d: d[1])

    if len(cd_sorted) >= 1 and cd_sorted[0][1] < 0.4:
        print("识别到的人最有可能是: ", cd_sorted[0][0])
        return str(cd_sorted[0][0])
    else:
        print('未知人员')
        return '未知人员'


@bp.route('/resident_photos')
def resident_photos():
    train('resident')
    return render_template('Test.html')


@bp.route('/visitor_photos')
def visitor_photos():
    train('visitor')
    return render_template('Test.html')


