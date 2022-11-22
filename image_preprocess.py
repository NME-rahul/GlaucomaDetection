'''
this file is use for the purpose of image preprocessing
* image resize
* adpaptive histogram flattening
'''

import cv2 as cv
import numpy as np
import os

#default height and width for model training and inference
dflt_img_height = 300
dflt_img_width = 300

#always give path to the directory of "train" and "validation"
def fetch_path(folder_path):
  data_path = os.listdir(folder_path)
  for i in data_path: #run two times, in "train" or "validation" folder
    data = os.listdir(folder_path + '/' + i)
    for j in data: #run two times, in "Glaucoma_Negative" or "Glaucoma_Positive" folder
      Glaucoma_data = os.listdir( folder_path + '/' + i + '/' + j + '/')
      for k in Glaucoma_data: #run on according the no of images 
        img_path = folder_path + '/' + i + '/' + j + '/' + k
        resize_(img_path)
        adaptive_hist_flattening(img_path)


#function which gets the image path from main.py and resize it according to model requirments
def resize_(path):
  if os.path.isdir(path) == True: #check if path is directory or not
    fetch_path(path) #then fatch the images from directory
  
  if os.path.exists(path) == True: #check if path is image or not
    img = cv.imread(path) #then read the image and store it in numpy array
    image_instance = cv.resize(img, (dflt_img_height, dflt_img_width)) #resize image accroding to given height and width
    image_instance = np.expand_dims(image_instance, 0) #expand the shape of array
    
  print('Image: ', path)
  return image_instance #return resized image/s


#function for performing adaptive histogram flattening
def adaptive_hist_flattening(path):
  if os.path.isdir(path) == True: #check if path is directory or not
    fetch_path(path) #then fatch the images from directory

  if os.path.exists(path) == True: #check if path is image or not      
    img = cv.imread(path) #then read the image and store it in numpy array
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV) #convert color scale of image from RGB(0-255) to HSV(0-360) and save in hsv
    h,s,v = cv.split(hsv) #split the hsv in h, s and v variables
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(3,3)) #create the algo for improving the contrast of image
    result = clahe.apply(v) #apply changes on v(stands for value of color)
      
    #postprocessing
    hsv = cv.merge((h, s, result)) #merge the results of after improving the contrast in h and s  again
    rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR) #convert again from HSV to RGB
    cv.imwrite(path, rgb) #overwrite the improved image

  print('Image: ', path)
