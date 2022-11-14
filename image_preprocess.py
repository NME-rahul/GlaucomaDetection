import cv2 as cv
import numpy as np
import os

dflt_img_height = 300
dflt_img_width = 300

#aalways give path to the directory of train and validation
def fetch_path(folder_path):
  data_path = os.listdir(folder_path)
  for i in data_path:
    print(i)
    data = os.listdir(folder_path + '/' + i)
    for j in data:
      Glaucoma_data = os.listdir( folder_path + '/' + i + '/' + j + '/')
      for k in Glaucoma_data:
        img_path = folder_path + '/' + i + '/' + j + '/' + k
        resize_(img_path)
        adaptive_hist_flattening(img_path)

#function which gets the image path from main.py and resize it according model requirments
def resize_(path):

  if os.path.isdir(path) == True:
    fetch_path(path)
  
  if os.path.exists(path) == True:
    img = cv.imread(path)
    image_instance = cv.resize(img, (dflt_img_height, dflt_img_width))
    image_instance = np.expand_dims(image_instance, 0)
    
  print('Image: ', path)
  return image_instance


def adaptive_hist_flattening(path):
  if os.path.isdir(path) == True:
    fetch_path(path)

  if os.path.exists(path) == True:       
    img = cv.imread(path)
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
    result = clahe.apply(v)
      
    #postprocessing
    hsv = cv.merge((h, s, result))
    rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    cv.imwrite(path, rgb)

  print('Image: ', path)
