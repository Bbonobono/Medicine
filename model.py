import tensorflow as tf
import tensorflow.keras as keras
import cv2 as cv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from collections import defaultdict
from DataProcess.py import csv_process, load_img

class PillModel(tf.keras.Model):
    
    def __init__(self, class_num):
        super().__init__()
        self.conv1 = tf.keras.layers.Conv2D(96, (11, 11), strides=(4,4), padding='valid', activation='relu', input_shape=(227, 227, 3))
        self.conv2 = tf.keras.layers.Conv2D(256, (5, 5), strides=(1,1), padding='same', activation='relu')
        self.conv3 = tf.keras.layers.Conv2D(384, (3, 3), strides=(1,1), padding='same',activation='relu')
        self.conv4 = tf.keras.layers.Conv2D(256, (3, 3), strides=(1,1), padding='same',activation='relu')
        self.bn = tf.keras.layers.BatchNormalization()
        self.maxpool = tf.keras.layers.MaxPooling2D((3, 3), strides=(2,2))
        self.flatten = tf.keras.layers.Flatten()
        self.dense1 = tf.keras.layers.Dense(4096, activation='relu')
        self.dense2 = tf.keras.layers.Dense(class_num,activation='softmax')

    def call(self, input):
        x = self.conv1(input)
        x = self.bn(x)
        x = self.maxpool(x)
        x = self.conv2(input)
        x = self.bn(x)
        x = self.maxpool(x)
        x = self.conv3(x)
        x = self.bn(x)
        x = self.conv3(x)
        x = self.bn(x)
        x = self.conv4(x)
        x = self.bn(x)
        x = self.flatten(x)
        x = self.dense1(x)
        x = self.dense2(x)
        
        return x

    if __name__ == "__main__":
        y1_train, y1_test, y1_val, moyang_dict = csv_process('merged_med_4.csv', '의약품제형')
        y2_train, y2_test, y2_val, moyang_dict = csv_process('merged_med_4.csv', '제형코드명')
        X_train, X_val, X_test = load_img('./cropped_pills/')

        model1 = PillModel(class_num=11)
        model1.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy'])
        history1 = model1.fit(X_train, y1_train, epochs=100, batch_size=32, validation_data=(X_val, y1_val))
        model1.predict(X_test,y1_test)
        model1.save('model1')

        model2 = PillModel(class_num=4)
        model2.compile(
            optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
            loss=tf.keras.losses.SparseCategoricalCrossentropy(),
            metrics=['accuracy'])
        history2 = model2.fit(X_train, y2_train, epochs=100, batch_size=32, validation_data=(X_val, y1_val))
        model2.predict(X_test,y1_test)
        model2.save('model2')
        

