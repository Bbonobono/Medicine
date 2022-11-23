import tensorflow as tf
import tensorflow.keras as keras
import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import defaultdict

def csv_process(csv_path, col_name, verbose = False):
    """
        csv에서 train에 필요한것만 정제
        input : csv path, col_name(str)
        output : y_train, y_val, y_test , category dict
    """
    data = pd.read_csv(csv_path)

    data['의약품제형']=data['의약품제형'].astype('category')
    data['제형코드명']=data['제형코드명'].astype('category')

    data['모양코드']=data['의약품제형'].cat.codes
    data['제형코드']=data['제형코드명'].cat.codes

    dict_moyang = defaultdict(str)
    dict_jehyung = defaultdict(str)

    for a, b, c, d in zip(data['의약품제형'].value_counts().keys(), data['모양코드'].value_counts().keys(),\
                            data['제형코드명'].value_counts().keys(), data['제형코드'].value_counts().keys()):
        dict_moyang[b] = a 
        dict_jehyung[d] = c
    
    train_labels = data[:14000].copy()
    train_labels.reset_index(inplace=True)

    test_labels = data[14000:].copy()
    test_labels.reset_index(inplace=True)

    y1_train = train_labels['모양코드'][:11000]
    y2_train = train_labels['제형코드'][:11000]

    y1_val = train_labels['모양코드'][11000:14000]
    y2_val = train_labels['제형코드'][11000:14000]

    y1_test = test_labels['모양코드']
    y2_test = test_labels['제형코드']

    return y1_train, y2_train, y1_val, y2_val, y1_test, y2_test , dict_moyang, dict_jehyung

def load_img(img_path, verbose=True):
    """
        train img, val img, test img 생성
        input : img_path
        output : X_train, X_val, X_test
    """
    if not img_path.endswith('/'):
        img_path += '/'

    train_img = list()
    cnt = 0
    for i in range(14000):
  
        try:
            train_img.append(np.array(Image.open(path+'{}_f.jpg'.format(cnt)).resize((227,227)),dtype=np.float))
        except:
            train_img.append(np.zeros((227,227,3)))
    cnt += 1

    if i%600==0 and verbose:
        print(i,' Train Done')

    test_img = list()

    for i in range(4776):

    try:
        test_img.append(np.array(Image.open(path+'{}_f.jpg'.format(cnt)).resize((227,227)),dtype=np.float))
    except:
        test_img.append(np.zeros((227,227,3)))

    cnt += 1
    if i%200==0 and verbose:
        print(i,' Test Done')

    X_train = tf.convert_to_tensor(train_img[:11000])
    X_val = tf.convert_to_tensor(train_img[11000:14000])

    X_test = tf.convert_to_tensor(test_img)

    return X_train, X_val, X_test

    if __name__ == "__main__":
        y1_train, y1_test, y1_val, moyang_dict = csv_process('merged_med_4.csv', '의약품제형')
        y2_train, y2_test, y2_val, moyang_dict = csv_process('merged_med_4.csv', '제형코드명')
        X_train, X_val, X_test = load_img('/cropped_pills/')