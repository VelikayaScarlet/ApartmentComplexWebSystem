import csv

import numpy as np
import skimage
from flask import *
import cv2
import dlib
import os

bp = Blueprint('detect', __name__, url_prefix='/detect')


@bp.route('resident_detect')
def resident_detect():
    pass
