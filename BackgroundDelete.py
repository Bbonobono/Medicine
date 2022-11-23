import pandas as pd
import numpy as np 
import math          
import seaborn as sns
import matplotlib.pyplot as plt
import tensorflow as tf

def background_delete_save_ver2(_img,save_path,cnt):
  dir = cnt//1000
  img = cv.imread(_img)
  height, width, channel = img.shape
  rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
  hsv = cv.cvtColor(rgb, cv.COLOR_RGB2HSV)/255.0
  h,s,v = cv.split(hsv)
  metric = (h>h[0][0]+0.015) | (h<h[0][0]-0.015) | (s>s[0][0]+0.045) | (s<s[0][0]-0.045)
  metric = metric.reshape(height,width,1)
  new_img = img*metric
  cv.imwrite(save_path + '{}.jpg'.format(cnt), new_img)

cnt = 0
img_path = ''
save_path = ''
for i in range(0,18776):
  background_delete_save_ver2(img_path + '{}.jpg'.format(i),cnt)
  cnt += 1
  if i%187==186:
    print(i,'Done \n')
  