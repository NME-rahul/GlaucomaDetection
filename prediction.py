#user defined modules
import image_preprocess as ip
import plot

#pre-defined modules
import os
import glob
import numpy as np
import tensorflow as tf
from tensorflow.keras.applications.resnet50 import decode_predictions

class_names = ['Glaucoma_Negative', 'Glaucoma_Positive']


def start_predictions(model):

  def classify(image_instance):
    #if image_instance != False:
    image_instance = np.expand_dims(image_instance, 0)
    predictions = model.predict(image_instance)
    score = tf.nn.softmax(predictions[0])
    print("This image most likely belongs to {} with a {:.2f} percent confidence.\n".format(class_names[np.argmax(score)], 100 * np.max(score)))
    #plot.plot_predictions(predictions) #plot_ function is defined in plot.py

  path = input('\nEnter path of image/s: ')

  if os.path.isdir(path) == True:
    image_path = glob.glob(path + '/**/*.png', recursive=True)
    for image_instance in image_path:
      image_instance = ip.resize_(image_instance)
      classify(image_instance)
  elif os.path.exists(path):
    image_instance = ip.resize_(path)
    classify(image_instance)
