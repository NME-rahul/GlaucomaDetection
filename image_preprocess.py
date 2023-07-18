import cv2 as cv
import os

dflt_img_height = 300
dflt_img_width = 300

Error3 = 'Error: unable to fetch images or Courrupt image or size is not 300x300x3\n'

#function which gets the image path from main.py and resize it according model requirments
def resize_(image_path):
  if type(image_path) == list:
    for i in image_path:
      resize_(i)

  img = cv.imread(str(image_path))
  try:
    image_instance = cv.resize(img, (dflt_img_height, dflt_img_width))
    print('Image: ', image_path)
  except:
    print(Error3)
    image_instance = False

  return image_instance


def adaptive_hist_flattening(image_path):
  if type(image_path) == list:
    for i in image_path:
      adaptive_hist_flattening(i)

  print('loading Image...\n ',image_path)
  img = cv.imread(str(image_path))
  try:
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    h,s,v = cv.split(hsv)
    clahe = cv.createCLAHE(clipLimit=2.0, tileGridSize=(3,3))
    result = clahe.apply(v)
      
    #postprocessing
    hsv = cv.merge((h, s, result))
    rgb = cv.cvtColor(hsv, cv.COLOR_HSV2BGR)
    cv.imwrite(path, rgb)
  except:
    print(Error3)
