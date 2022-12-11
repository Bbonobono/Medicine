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
my = tf.keras.models.load_model('clss_model/my/efnet1')
jh = tf.keras.models.load_model('clss_model/jh/efnet1')
bh = tf.keras.models.load_model('clss_model/bh/efnet1')


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

def load_image_into_numpy_array(data):
  npimg = np.frombuffer(data, np.uint8)
  frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
  frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  return frame


def remove_punc(s):
  s = str(s)
  result = s.translate(str.maketrans('iIl0','111o', string.punctuation))
  # i, I, l 은 1로 변경, 0은 o로 변경
  return result


class Predict():
  # 현재 클래스는 아마 classification이 된 것을 받아서 사용
  # 후에 classification이 된다면 따로 함수 만들 예정
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
        data = pd.read_csv(path)
    self.data = data

  def predict_img(self, img=None, path=None, *, is_dict=None):
    # data는 일단 set_data나 class 만들때 data 설정해둔 것을 사용하는 것으로 만듦
    # 만약 is_dict가 True면 dataFrame이 아닌 feature들로 return
    data = self.data.copy()
    if img is None:
      if path is None:
        raise Exception('img or path is needed')
      img = Image.open(BytesIO(path))
    im = np.array(img.resize((224,224)),dtype=np.float).reshape(-1,224,224,3)
    pred_my = self.my_dict[np.argmax(self.my.predict(im))]
    pred_jh = self.jh_dict[np.argmax(self.jh.predict(im))]
    pred_bh = self.bh_dict[np.argmax(self.bh.predict(im))]
    pred_cr = predict_hsv(load_image_into_numpy_array(path),self.color_data_path)
    pred_txt = ocr(img, pred_jh)

    res = data[data['의약품제형']==pred_my]\
              [data['제형코드명']==pred_jh]\
              [data['앞분할선']==pred_bh]\
              [data['color']==pred_cr].copy()

    temp_dic = dict()
    temp = list()
    for t in pred_txt:
      temp.append(remove_punc(t).lower())

    for i in res.index:
      rate = 0
      front = remove_punc(res.loc[i].표시앞).lower()
      back = remove_punc(res.loc[i].표시뒤).lower()

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

    sort_dic = sorted(temp_dic.items(), key=lambda x:x[1], reverse=True)[:10] # 조정해서 갯수
    result = res.loc[[k for k,v in sort_dic]]

    return result