#user defined modules
import plot
import image_preprocess as ip

#pre-defined modules
import os
import sys
import pathlib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input

#available Errors types in this file
Error4 = '\nError: wrong path'
Error5 = '\nError: unable to load model, model not found cuurent working directory or given path try with new path'

batch_size = 32
img_height = 300
img_width = 300
image_cnt_train = 0
image_cnt_val = 0

def load_data(): #load data for model
  train_dir = input('Enter path of train images: ')
  val_dir = input('Enter path of val images: ')

  if os.path.exists(train_dir) and os.path.exists(val_dir):
    train_dir = pathlib.Path(train_dir)
    val_dir = pathlib.Path(val_dir)

    image_cnt_train = len(list(train_dir.glob('**/*')))
    image_cnt_val = len(list(val_dir.glob('**/*')))
    print("\ndata size: \ntrain Images: %d \nvalidation Images: %d" %(image_cnt_train, image_cnt_val))
    if image_cnt_train == 0 or image_cnt_val == 0:
      sys.exit(Error4)
  else:
    sys.exit(Error4)

  choose = input('\nImage preprocessing(y/n)?: ')
  choose = choose.lower()
  if choose == 'y' or choose == 'yes':
    ip.resize_(path)
    ip.adaptive_hist_flattening(path)

  return [train_dir, val_dir]


#if you want to see sample images
#plot.plot_samples() #defined in plot.py

def create_data(): #prepare data for model  
  print('\nloaded Dataset - ')

  #training dataset
  train_ds = tf.keras.utils.image_dataset_from_directory(
        dataDir,
        validation_split = 0.2,
        subset = 'training',
        seed = 123,
        image_size = (img_height, img_width),
        batch_size = batch_size
      )

  #validation dataset
  val_ds = tf.keras.utils.image_dataset_from_directory(
        dataDir,
        validation_split = 0.2,
        subset = 'validation',
        seed = 123,
        image_size = (img_height, img_width),
        batch_size = batch_size
      )
  print('\nClasses: ', train_ds.class_names)

def create_generator(train_dir, val_dir): #perform data augmentation    
  train_dataGen = ImageDataGenerator(
    rotation_range = 30,
    horizontal_flip = True,
    vertical_flip = True,
  )

  test_dataGen = ImageDataGenerator(
    rotation_range = 30,
    horizontal_flip = True,
    vertical_flip = True,
    )

  print('\nData generator - ')
  train_gen = train_dataGen.flow_from_directory(train_dir,
                                                      target_size = (img_height, img_width),
                                                      batch_size = batch_size)

  val_gen = test_dataGen.flow_from_directory(val_dir,
                                                  target_size = (img_height, img_width),
                                                  batch_size = batch_size)
  return [train_gen, val_gen]

def create_model_ResNet50(): #create the model Resnet50
  print('\nCreating model EfficientNet...')
  dropout = 0.0
  num_classes = 2
  fc_layers = [512, 256, 128]

  def build_model(base_model, dropout, fc_layers, num_classes):
    for layer in base_model.layers:
        layer.trainable = False

    x = base_model.output
    x = layers.GlobalAveragePooling2D()(x)
    x = layers.Flatten()(x)
    for fc in fc_layers:
        x = layers.Dense(fc, activation='relu')(x)
        #x = layers.Dropout(dropout)(x)
    preditions = layers.Dense(num_classes, activation='softmax')(x)
    finetune_model = Model(inputs = base_model.input, outputs = preditions)
    return finetune_model


  base_model_1 = tf.keras.applications.efficientnet_v2.EfficientNetV2L(
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
  print('Done model Creation.')
  return model #return newly created model

def load_existing_model(): #load existing model
  #if you wants to retrain existed trained model
  def fun(path):
    model = False #initially
    try:
      model = tf.keras.models.load_model(path)
      print('\nDone loading.')
    except:
      print(Error5)
    return model
      
  print('\nLoading model...')
  path = 'GlaucomaDetection.h5' 
  while True:
    model = fun(path)
    if model == False:
      path = input('\nEnter another path: ')
    else:
      break
  return model
    
def compile_model(model): #compile the model
  adam = tf.keras.optimizers.Adam(learning_rate=0.00001)
  model.compile(
      adam,
      loss = 'binary_crossentropy',
      metrics = ['accuracy']
    )

  return model

def fit_model(model, train_gen, val_gen): #fit the model on data
  epochs = int(input('\nEnter epoches: '))
  validation_steps = 10
  history = model.fit(
      train_gen,
      epochs = epochs,
      steps_per_epoch = len(train_gen),
      validation_data = val_gen,
      validation_steps = image_cnt_val//batch_size,
      shuffle = True
    )
  
  plot.plot_accuracy(history, epochs) #will plot accuracy of trained model

def show_accuracy(model):
  model.save('GlaucomaDetection.h5') #save the trained model
  #evaluate the model
  print('\n\nAccuracy achieved:')
  test_results = model.evaluate(train_generator, steps=len(train_generator))
  val_results = model.evaluate(val_generator, steps=len(val_generator))
  print('training loss: %f, training acc: %f' %(test_results[0], test_results[1]))
  print('validation loss: %f, validation acc: %f' %(val_results[0], val_results[1]))
