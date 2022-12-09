import tensorflow as tf
import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import warnings
import re
import pickle
from collections import defaultdict
import string
warnings.filterwarnings("ignore")

from knn_ColorDetection import *
# from ocr import ocr

#%%
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

#%%
color_data_path = 'hsv_training.data'

#%%
my = tf.keras.models.load_model('clss_model/my/efnet1')
jh = tf.keras.models.load_model('clss_model/jh/efnet1')
bh = tf.keras.models.load_model('clss_model/bh/efnet1')


#%%
def predict(im, my, jh, bh):

    color_data_path = 'hsv_training.data'
    jh_dict = {3: '정제', 0: '경질캡슐', 2: '연질캡슐', 1: '기타'}
    my_dict = {6: '원형',
                  8: '장방형',
                  9: '타원형',
                  0: '기타',
                  4: '삼각형',
                  10: '팔각형',
                  3: '사각형',
                  5: '오각형',
                  7: '육각형',
                  1: '마름모형',
                  2: '반원형'}
    bh_dict = {2: 'x', 1: '-', 0: '+', 3: '기타'}
    pred_my = my_dict[np.argmax(my.predict(im))]
    pred_jh = jh_dict[np.argmax(jh.predict(im))]
    pred_bh = bh_dict[np.argmax(bh.predict(im))]
    pred_cr = detect_color(im[0], color_data_path)

    return pred_my, pred_jh, pred_bh
