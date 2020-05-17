from keras.models import load_model
#from tkinter import *
#import tkinter as tk
#import win32gui
from PIL import ImageGrab, Image
import numpy as np
import os



model = load_model("mnist.h5")


def predictDigit(img_name):
    img = Image.open(img_name)
    #resize image to 28x28 pixels
    img = img.resize((28,28))
    #convert rgb to grayscale
    #img = img.convert('L')
    img = np.array(img)
    #reshaping to support our model input and normalizing
    img = img.reshape(1,28,28,1)
    img = img/255.0
    #predicting the class
    res = model.predict([img])[0]
    return np.argmax(res), max(res)
