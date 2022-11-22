#user defined modules
import plot
import train_model as tm
import image_preprocess as ip

#pre-defined modules
import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model
from tensorflow.keras.applications.resnet50 import decode_predictions

#available Error types in this file
Error1 = '\nError: model not found make sure the model is present inside the current working directory.'
Error2 = '\nError: Courrupt image or size is not 300x300x3'
Error3 = '\nError: unable to fetch images.'

def start_predictions(model):
  path = input('\nEnter path of image/s: ') #take path for image/s
  predictions = []
  if os.path.isdir(path) == True:  #if given path is directory(it must be in the form of "Glaucoma_Negative" and "Glaucoma_Positive")
    for i in range(len(os.listdir(path))): #fetch path of images
      image_instance = ip.resize_(path + '/' + [image_path for image_path in os.listdir(path)][i]) #resize_ function is defined in image_resize.py, resize the images
      try:
        predictions = model.predict(image_instance)
        #predictions.append(model.predict(image_instance)) #start prediction one images one by one and append results in list prediction
        print('GlaucomaNegative:', predictions[0][0]*100,'%  ', 'GlaucomaPositive:', predictions[0][1]*100,'%')
      except:
        print(Error3)
  
  else:
    image_instance = ip.resize_(path) #resize the images
    try:
      predictions = model.predict(image_instance) #start prediction one images
    except:
      print(Error2)
  plot.plot_predictions(predictions) #plot_ function is defined in plot.py, plot the prediction/s for visual understanding

def start(model=False):
  if len(sys.argv) > 3: #if more then two arguments given
    sys.exit("\nError: main.py except only 1 argument 'train_model'")
  elif len(sys.argv) >= 2: #else if 2 arguments given and the first one is "train_model" 
    tm.load_data()
    tm.create_data()
    tm.create_generator()
    if len(sys.argv) == 3 and sys.argv[2] == 'existing': #if 2 arguments were given and the last one is "existing"
      model = tm.load_existing_model() #will load the existing model
    if len(sys.argv) == 2 and sys.argv[1] == 'train_model': #else create the new model and compile
      model = tm.create_model_ResNet50()
      model = tm.compile_model(model)

    if model == False: #if model creation or loading failed
      sys.exit(Error1) #stop the execution
    else: #else fit the model on data and save
      tm.fit_model(model)
      model.save('GlaucomaDetection.h5')
    return model

  elif len(sys.argv) == 1 or sys.argv[1] == 'make_predictions': #if no arguments or one arugment "make_prediction" were given
    model = tm.load_existing_model() #load the existing model
    if model == False: #if model creation or loading failed
      sys.exit(Error1) #stop the execution
    return model #return model

#code will start from here
model = start(model=False) #this returns the model(existed or newly created based on users choice)
if input("\npress 'P' for making predictions: ") == 'P': #if user press "p" then start predictions on image/s
  start_predictions(model)
