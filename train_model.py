#user defined modules
import plot
import image_preprocess

#pre-defined modules
import os
import sys
import pathlib
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input

#available Errors types in this file
Error4 = '\nError: wrong path'
Error5 = '\nError: unable to load model'

batch_size = 8
img_height = 300
img_width = 300

def load_data():
  path = input('Enter path for data for training: ')

  if os.path.exists(path):
    #Data RIMONE
    global data_train, data_val, image_count_train, image_count_val
    data_train = pathlib.Path(path+'/Train')
    data_val = pathlib.Path(path+'/Validation')

    #Data RIMONE
    image_count_train = len(list(data_train.glob('**/*.png')))
    image_count_val = len(list(data_val.glob('**/*.png')))
    print("\ndata size - \nTrain: ",image_count_train, "\nValidation: ",image_count_val)
    if image_count_train + image_count_val == 0:
      sys.exit(Error4)
  else:
    print(Error4)

  choose = input('\nImage preprocessing(y/n)?: ')
  choose = choose.lower()
  if choose == 'y' or choose == 'yes':
    image_preprocess.resize_(path)
    image_preprocess.adaptive_hist_flattening(path)


#if you want to see sample images
#plot.plot_samples() #defined in plot.py

def create_data():
  global train_ds, val_ds
  
  print('\nloaded Dataset - ')

  #training dataset
  train_ds = tf.keras.utils.image_dataset_from_directory(
        data_train,
        validation_split = 0.2,
        subset = 'training',
        seed = 123,
        image_size = (img_height, img_width),
        batch_size = batch_size
      )

  #validation dataset
  val_ds = tf.keras.utils.image_dataset_from_directory(
        data_val,
        validation_split = 0.2,
        subset = 'validation',
        seed = 123,
        image_size = (img_height, img_width),
        batch_size = batch_size
      )

def create_generator():
  global train_generator, val_generator
    
  train_dataGen = ImageDataGenerator(
    preprocessing_function = preprocess_input,
    rotation_range = 90,
    horizontal_flip = True,
    vertical_flip = True,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    zoom_range = 0.1
  )

  test_dataGen = ImageDataGenerator(
    preprocessing_function = preprocess_input,
    rotation_range = 90,
    horizontal_flip = True,
    vertical_flip = True,
    width_shift_range = 0.2,
    height_shift_range = 0.2,
    zoom_range = 0.1
    )

  print('\nData after generator - ')
  train_generator = train_dataGen.flow_from_directory(data_train,
                                                      target_size = (img_height, img_width),
                                                      batch_size = batch_size)

  val_generator = test_dataGen.flow_from_directory(data_val,
                                                  target_size = (img_height, img_width),
                                                  batch_size = batch_size)

def create_model_ResNet50():
  #ResNet50 model
  dropout = 0.5
  num_classes = 2
  fc_layers = [1024, 512, 256]

  def build_model(base_model, dropout, fc_layers, num_classes):
    for layer in base_model.layers:
      layer.trainable = False

    x = base_model.output
    x = layers.Flatten()(x)
    for fc in fc_layers:
        x = layers.Dense(fc, activation='relu')(x)
        x = layers.Dropout(dropout)(x)
    preditions = layers.Dense(num_classes, activation='softmax')(x)
    finetune_model = Model(inputs = base_model.input, outputs = preditions)
    return finetune_model


  base_model_1 = tf.keras.applications.resnet50.ResNet50(
    weights = 'imagenet',
    include_top = False,
    input_shape = (img_height, img_width, 3)
  )

  model = build_model(
    base_model_1,
    dropout = dropout,
    fc_layers = fc_layers,
    num_classes = num_classes
  )
  return model

def load_existing_model():
  #if you wants to retrain existed trained model
  if os.path.exists('GlaucomaDetection.h5') == True:
    try:
      model = tf.keras.models.load_model('GlaucomaDetection.h5')
    except:
      print()
  else:
    model = False

  return model
    
def compile_model(model):
  adam = tf.keras.optimizers.Adam(learning_rate=0.00001)
  model.compile(
      adam,
      loss = 'binary_crossentropy',
      metrics = ['accuracy']
    )

  return model

def fit_model(model):
  epochs = int(input('\nEnter epoches: '))
  validation_steps = 10
  history = model.fit(
      train_generator,
      epochs = epochs,
      steps_per_epoch = len(train_generator),
      validation_data = val_generator,
      validation_steps = image_count_val//batch_size,
      shuffle = True
    )
  
  #will plot accuracy of trained model
  plot.plot_accuracy(history, epochs)

