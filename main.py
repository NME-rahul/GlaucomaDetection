#user defined modules
import plot
import train_model
import image_preprocess

#pre-defined modules
import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.models import Model

def start():
  if len(sys.argv) > 2:
    sys.exit("\nError: main.py except only 1 argument 'trai_model'")
  elif len(sys.argv) == 2 and sys.argv[1] == 'train_model':
    train_model.load_data()
    model = train_model.train()
    if model == False:
      sys.exit('\nError: model not found make sure the model is present inside the current working directory')
    else:
      train_model.fit_model(model)
  elif len(sys.argv) == 1 or sys.argv[1] == 'dflt':
    if os.path.exists('GlaucomaDetection.h5') == True:
      path = 'GlaucomaDetection.h5'
    else:
      path = input('\nModel not found in current working directory \n\nEnter path of model directory: ')
      if os.path.exists(path+'GlaucomaDetection.h5') == False:
          print('\nError: Model not found')
    try:
      model = tf.keras.models.load_model(path+'GlaucomaDetection.h5')
    except:
      sys.exit('\nError: unable to load model')


  path = input('\nEnter path of image/s: ')
  if os.path.isdir() == True:
    for image_Path in range(len(os.listdir(path))):
      image_instance = image_preprocess.resize_(image_Path) #resize_ function is defined in image_resize.py
      try:
        predictions = model.predict(image_instance)
        predictions.append(predictions)
      except:
        print('\nError: unable to fetch images')
        
  else:
    image_instance = image_preprocess.resize_(path)
    try:
      predictions = model.predict(image_instance)
    except:
      print('\nError: Courrupt image or size is not 300x300x3')

  plot.plot_predictions(predictions) #plot_ function is defined in plot.py

start()
