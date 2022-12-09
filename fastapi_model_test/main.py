from typing import Union

from fastapi import FastAPI, File, UploadFile
from knn_ColorDetection import *
from PIL import Image
from io import BytesIO
from predict import predict
import cv2
import uvicorn
import tensorflow as tf

app = FastAPI()

my = tf.keras.models.load_model('clss_model/my/efnet1')
jh = tf.keras.models.load_model('clss_model/jh/efnet1')
bh = tf.keras.models.load_model('clss_model/bh/efnet1')

img_size = 224



def load_image_into_numpy_array(data):
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame

@app.post('/prediction')
async def prediction_route(file: UploadFile = File(...)):
    contents = await file.read()
    pill_image = Image.open(BytesIO(contents))
    pill_image = pill_image.resize((img_size, img_size))
    pill_image = np.array(pill_image).reshape(-1,224,224,3)
    prediction = predict(pill_image, my, jh, bh)
    color_prediction = predict_hsv(load_image_into_numpy_array(contents),'hsv_training.data')
    prediction += (color_prediction,)
    return prediction



