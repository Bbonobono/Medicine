import imutils

from imutils import perspective
from imutils import contours

import tensorflow as tf
import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from io import BytesIO
import warnings
import re
import pickle
from collections import defaultdict
import string

warnings.filterwarnings("ignore")

from knn_ColorDetection import *
from ocr import ocr

#%%
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


#%%
my = tf.keras.models.load_model('clss_model/my/efnet_v2_3')
jh = tf.keras.models.load_model('clss_model/jh/efnet_v2_2')
bh = tf.keras.models.load_model('clss_model/bh/efnet_v2')
seg = tf.keras.models.load_model('seg_model/DeepLab/DL_fine_tuning_ver2')

#%%
# def predict(im, my, jh, bh):
#
#     color_data_path = 'hsv_training.data'
#     jh_dict = {3: '정제', 0: '경질캡슐', 2: '연질캡슐', 1: '기타'}
#     my_dict = {6: '원형',
#                   8: '장방형',
#                   9: '타원형',
#                   0: '기타',
#                   4: '삼각형',
#                   10: '팔각형',
#                   3: '사각형',
#                   5: '오각형',
#                   7: '육각형',
#                   1: '마름모형',
#                   2: '반원형'}
#     bh_dict = {2: 'x', 1: '-', 0: '+', 3: '기타'}
#     pred_my = my_dict[np.argmax(my.predict(im))]
#     pred_jh = jh_dict[np.argmax(jh.predict(im))]
#     pred_bh = bh_dict[np.argmax(bh.predict(im))]
#     pred_cr = detect_color(im[0], color_data_path)
#
#     return pred_my, pred_jh, pred_bh

#%%

img_size = 224

def crop_segd(img):
  # img = load_and_seg_img(img)
  # load the image, copy image to origin
  img = (img * 255).astype(np.uint8)
  origin = img.copy()

  # morphology
  kernel = np.ones((5, 5), np.uint8)
  mor_img = cv.morphologyEx(img, cv.MORPH_OPEN, kernel)

  # edge detecting
  edged = cv.Canny(mor_img, 50, 100)
  edged = cv.dilate(edged, None, iterations=1)
  edged = cv.erode(edged, None, iterations=1)

  cnts = cv.findContours(edged, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
  cnts = imutils.grab_contours(cnts)
  (cnts, _) = contours.sort_contours(cnts)

  # max area
  area = list()
  for c in cnts:
    area.append(cv.contourArea(c))
  idex = (area.index(max(area)))

  # making box
  box = cv.minAreaRect(cnts[idex])
  box = cv.cv.BoxPoints(box) if imutils.is_cv2() else cv.boxPoints(box)
  box = np.array(box, dtype="int")
  box = perspective.order_points(box)

  for i in range(4):
    for j in range(2):
      if box[i, j] < 0:
        box[i, j] = 0

  a = int(min(box[:, 1]))
  b = int(max(box[:, 1]))
  c = int(min(box[:, 0]))
  d = int(max(box[:, 0]))

  crop_img = origin[a:b, c:d]
  crop_img = Image.fromarray(crop_img)

  # img size
  img_size = crop_img.size
  x = img_size[0]
  y = img_size[1]
  size = max(x, y) + 20

  resized_img = Image.new(mode='RGB', size=(size, size), color=(0, 0, 0))
  offset = (round((abs(x - size)) / 2), round((abs(y - size)) / 2))
  resized_img.paste(crop_img, offset)
  resized_img = resized_img.resize((224, 224))
  return np.array(resized_img) / 255.0

def remove_punc(s):
  s = str(s)
  result = s.translate(str.maketrans('iIl0','111o', string.punctuation))
  # i, I, l 은 1로 변경, 0은 o로 변경
  return result


class Predict():
  # 현재 클래스는 아마 classification이 된 것을 받아서 사용
  # 후에 classification이 된다면 따로 함수 만들 예정
  jh_dict = {3: 3, 0: 0, 2: 2, 1: 1}
  my_dict = {6: 6,
                8: 8,
                9: 9,
                0: 0,
                4: 4,
                10: 10,
                3: 3,
                5: 5,
                7: 7,
                1: 1,
                2: 2}
  bh_dict = {2: 2, 1: 1, 0: 0, 3: 3}

  def __init__(self, data=None):
    # 시작하면서 data가 있으면 data에 넣어줌
    # 추후 load_model 함수들의 경로를 따로 설정해줄 필요
    if data is not None:
      self.set_data(data)
    self.my = my
    self.jh = jh
    self.bh = bh
    self.color_data_path = 'hsv_training.data'


  def set_data(self, data=None, path=None):
    # 추후에 db파일에서 읽어올 경우 함수 조정할 필요
    if data is None:
      if path is not None:
        data = pd.read_sql(path)
    self.data = data

  def predict_img(self, img=None, path=None, *, is_dict=True):
    # data는 일단 set_data나 class 만들때 data 설정해둔 것을 사용하는 것으로 만듦
    # 만약 is_dict가 True면 dataFrame이 아닌 feature들로 return
    data = self.data.copy()
    data = data.astype({ 'MY' : 'string' , 'JH' : 'string', 'BH_F' : 'string'})
    if img is None:
      if path is None:
        raise Exception('img or path is needed')
      # img = Image.open(path)
    im_raw = np.array(Image.open(BytesIO(path)).resize((img_size, img_size)), dtype=np.float).reshape(
      (-1, 224, 224, 3)) / 255.0
    mask = seg.predict(im_raw, verbose=0)
    im_seg = np.argmax(mask[0], axis=2).reshape(224, 224, 1) * im_raw[0]
    im = crop_segd(im_seg).reshape(-1, 224, 224, 3)
    pred_my = str(self.my_dict[np.argmax(self.my.predict(im, verbose=0))])
    pred_jh = str(self.jh_dict[np.argmax(self.jh.predict(im, verbose=0))])
    pred_bh = str(self.bh_dict[np.argmax(self.bh.predict(im, verbose=0))])
    pred_cr = predict_hsv((im[0]*255).astype(np.uint8),self.color_data_path)
    # pred_cr = predict_hsv(load_image_into_numpy_array(path),self.color_data_path)
    pred_txt = ocr((im[0]*255).astype(np.uint8), pred_jh)

    res = data[data['MY']==pred_my]\
              [data['JH']==pred_jh]\
              [data['BH_F']==pred_bh]\
              [data['COLOR']==pred_cr].copy()

    # res = data[data['BH_F'] == pred_bh].copy()

    temp_dic = dict()
    temp = list()
    for t in pred_txt:
      temp.append(remove_punc(t).lower())

    for i in res.index:
      rate = 0
      front = remove_punc(res.loc[i].TEXT_F).lower()
      back = remove_punc(res.loc[i].TEXT_B).lower()

      for t in temp:
        if t in front:
          rate += 1
        elif t in back:
          rate += 1
      temp_dic[i] = rate
    if is_dict:
      result = dict()
      result['shape'] = pred_my
      result['form'] = pred_jh
      result['line'] = pred_bh
      result['color'] = pred_cr
      result['text'] = pred_txt

    sort_dic = sorted(temp_dic.items(), key=lambda x:x[1], reverse=True)[:200] # 조정해서 갯수
    result = res.loc[[k for k,v in sort_dic]]

    return result