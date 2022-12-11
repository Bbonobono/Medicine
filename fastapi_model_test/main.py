from typing import Union

from fastapi import FastAPI, File, UploadFile
from PIL import Image
from io import BytesIO
from predict import *

import cv2
import uvicorn
import pandas as pd


app = FastAPI()

img_size = 224

csv = pd.read_csv('merged_med_8.csv')

def load_image_into_numpy_array(data):
    npimg = np.frombuffer(data, np.uint8)
    frame = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return frame




@app.post('/prediction')
async def prediction_route(file: UploadFile = File(...)):
    contents = await file.read()
    p = Predict(csv)
    prediction = p.predict_img(path = contents)
    return prediction



