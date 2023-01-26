#user defined modules
import plot
import prediction
import train_model as tm
import image_preprocess as ip

#pre-defined modules
import sys

#available Error types in this file
Error1 = '\nError: model not found make sure the model is present inside the current working directory'
Error2 = "\nError: maximum argument limit exceeds."

def start():
  length = len(sys.argv)
  if length > 3:
    sys.exit(Error2)
  elif (length == 2 and sys.argv[1] == 'train_model') or length > 2:
    tm.load_data()
    tm.create_data()
    tm.create_generator()
    if len(sys.argv) == 3 and sys.argv[2] == 'existing':
      model = tm.load_existing_model()
    else:
      model = tm.create_model_ResNet50()
      model = tm.compile_model(model)

    if model == False:
      sys.exit(Error1)
    else:
      tm.fit_model(model)
      tm.show_accuracy(model)
    return model

  elif length == 1 or sys.argv[1] == 'make_predictions':
    model = tm.load_existing_model()
    #tm.show_accuracy(model)
    if model == False:
      sys.exit(Error1)
    return model

model = start()
if input("\npress 'P' for making predictions: ") == 'P':
  while True:
    prediction.start_predictions(model)
