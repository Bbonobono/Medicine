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

    data[col_name]=data[col_name].astype('category')
    data[col_name]=data[col_name].cat.codes

    dict_col = defaultdict(str)

    for a, b in zip(data[col_name].value_counts().keys(), data[col_name].value_counts().keys()):
        dict_col[b] = a 
   
    train_labels = data[:14000].copy()
    train_labels.reset_index(inplace=True)

    test_labels = data[14000:].copy()
    test_labels.reset_index(inplace=True)

    y_train = train_labels[col_name][:11000]
    y_val = train_labels[col_name][11000:14000]
    y_test = test_labels[col_name]


    return (y_train, y_val, y_test, dict_col)

def load_img(img_path, img_size=227, verbose=True):
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
            train_img.append(np.array(Image.open(img_path+'{}_f.jpg'.format(cnt)).resize((img_size,img_size)),dtype=np.float))
        except:
            train_img.append(np.zeros((img_size,img_size,3)))
        cnt += 1

        if i%600==0 and verbose:
            print(i,' Train Done')

    test_img = list()

    for i in range(4776):

        try:
            test_img.append(np.array(Image.open(img_path+'{}_f.jpg'.format(cnt)).resize((img_size,img_size)),dtype=np.float))
        except:
            test_img.append(np.zeros((img_size,img_size,3)))

        cnt += 1
        if i%200==0 and verbose:
            print(i,' Test Done')

    X_train = tf.convert_to_tensor(train_img[:11000])
    X_val = tf.convert_to_tensor(train_img[11000:14000])

    X_test = tf.convert_to_tensor(test_img)

    return (X_train, X_val, X_test)

    if __name__ == "__main__":
        y1_train, y1_test, y1_val, moyang_dict = csv_process('merged_med_4.csv', '의약품제형')
        y2_train, y2_test, y2_val, moyang_dict = csv_process('merged_med_4.csv', '제형코드명')
        X_train, X_val, X_test = load_img('/cropped_pills/')