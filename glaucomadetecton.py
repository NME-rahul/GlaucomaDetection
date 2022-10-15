# -*- coding: utf-8 -*-
"""GlaucomaDetecton.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1yvP-T-hoUI1RjZQm1bjIcdcBEXiLbUUC
"""

import matplotlib.pyplot as plt
from matplotlib import image
import numpy as np
import pathlib
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from tensorflow.keras.models import Model
from keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications.resnet50 import preprocess_input, decode_predictions

from google.colab import drive
drive.mount('/content/drive/')

'''
perform resizing and adaptive histogram flattening on images
'''

import cv2 as cv
import os

img_height = 300
img_width = 300
folder_path = '/content/drive/My Drive/Colab Notebooks/partitioned_by_hospital/'

def image_processing(img_path):
      img = cv.imread(img_path)
      #resizing
      cv.resize(img, (img_height,img_width))
      '''
      hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
      h,s,v = cv.split(hsv)
      clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
      result = clahe.apply(v)
      #postprocessing
      hsv = cv.merge((h, s, result))
      rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
      cv.imwrite(img_path, rgb)
      '''
      print('Image: ',img_path)

data_path = os.listdir(folder_path)
for i in range(len(data_path)):
  data = os.listdir(folder_path + data_path[i])
  for j in range(len(data)):
    Glaucoma_data = os.listdir( folder_path + data_path[i] + '/' + data[j] + '/')
    for k in range(len(Glaucoma_data)):
      img_path = folder_path + data_path[i] + '/' + data[j] + '/' + Glaucoma_data[k]
      image_processing(img_path)

#Data RIMONE
data_train = pathlib.Path('/content/drive/My Drive/Colab Notebooks/partitioned_randomly/Train/')
data_val = pathlib.Path('/content/drive/My Drive/Colab Notebooks/partitioned_randomly/Validation/')

#Data RIMONE
image_count_train = len(list(data_train.glob('**/*.png')))
image_count_val = len(list(data_val.glob('**/*.png')))
print(image_count_train, image_count_val)
num_samples = image_count_train + image_count_val

fig = plt.figure()
fig.set_figheight(15)
fig.set_figwidth(15)

Glaucoma_Positive = list(data_train.glob('Glaucoma_Positive/*'))
plt.subplot(2, 2, 1)
sample = plt.imshow(image.imread(str(Glaucoma_Positive[0])))
plt.title('Training \n\n\n Glaucoma Positive')

Glaucoma_Negative = list(data_train.glob('Glaucoma_Negative/*'))
plt.subplot(2, 2, 3)
plt.imshow(image.imread(str(Glaucoma_Negative[0])))
plt.title('Glaucoma Negative')

Glaucoma_Positive = list(data_val.glob('Glaucoma_Positive/*'))
plt.subplot(2, 2, 2)
plt.imshow(image.imread(str(Glaucoma_Positive[0])))
plt.title('Validation \n\n\n Glaucoma Positive')

Glaucoma_Negative = list(data_val.glob('Glaucoma_Negative/*'))
plt.subplot(2, 2, 4)
plt.imshow(image.imread(str(Glaucoma_Negative[0])))
plt.title('Glaucoma Negative')

plt.show()

batch_size = 8
img_height = 300
img_width = 300

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

train_generator = train_dataGen.flow_from_directory(data_train,
                                                    target_size = (img_height, img_width),
                                                    batch_size = batch_size)

val_generator = test_dataGen.flow_from_directory(data_val,
                                                  target_size = (img_height, img_width),
                                                  batch_size = batch_size)

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

adam = tf.keras.optimizers.Adam(learning_rate=0.00001)

model.compile(
    adam,
    loss = 'binary_crossentropy',
    metrics = ['accuracy']
)

keras.utils.plot_model(model, 'Model summary.pdf', show_shapes=True)

epochs = 500
validation_steps = 10

#train_generator = tf.repeat(train_generator, repeats=3)
#val_generator = tf.repeat(val_genertor, repeats=3)

#train_generator = tf.data.Dataset(train_generator)
#val_generator = tf.data.Dataset(val_generator)


history = model.fit(
    train_generator,
    epochs = epochs,
    steps_per_epoch = len(train_generator),
    validation_data = val_generator,
    validation_steps = image_count_val//batch_size,
    shuffle = True
)

acc = history.history['accuracy']
val_acc = history.history['val_accuracy']

loss = history.history['loss']
val_loss = history.history['val_loss']

epochs_range = range(epochs)

plt.figure(figsize=(8, 8))
plt.subplot(1, 2, 1)
plt.plot(epochs_range, acc, label='Training Accuracy')
plt.plot(epochs_range, val_acc, label='Validation Accuracy')
plt.legend(loc='lower right')
plt.title('Training and Validation Accuracy')

plt.subplot(1, 2, 2)
plt.plot(epochs_range, loss, label='Training Loss')
plt.plot(epochs_range, val_loss, label='Validation Loss')
plt.legend(loc='upper right')
plt.title('Training and Validation Loss')
plt.show()

model.save('/content/drive/MyDrive/Colab Notebooks/GlaucomaDetection.h5')

model = tf.keras.models.load_model('/content/drive/My Drive/Colab Notebooks/GlaucomaDetection.h5')

test_results = model.evaluate(train_generator, steps=len(train_generator))
val_results = model.evaluate(val_generator, steps=len(val_generator))
print('training loss: %f, training acc: %f' %(test_results[0], test_results[1]))
print('validation loss: %f, validation acc: %f' %(val_results[0], val_results[1]))

from google.colab import files
files.upload()

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/

!ls -l

# Commented out IPython magic to ensure Python compatibility.
!pip install kaggle
!mkdir ~/.kaggle
!cp /content/kaggle.json ~/.kaggle/
# %cd ~/.kaggle/
!chmod 777 kaggle.json
!kaggle datasets download -d sshikamaru/glaucoma-detection
!unzip glaucoma-detection
# %cd ~

from tensorflow.keras.preprocessing import image
import matplotlib.pyplot as pl

img_path = '/root/.kaggle/ORIGA/ORIGA/Images/540.jpg'
img = image.load_img(img_path, target_size=(224, 224))
img_array = image.img_to_array(img)
img_batch = np.expand_dims(img_array, axis=0)
img_preprocesed = preprocess_input(img_batch)

prediction = model.predict(img_preprocesed)
print(decode_predictions(prediction, top=3)[0])