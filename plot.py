import matplotlib.pyplot as plt

def plot_predictions(predictions):
  plt.style.use('seaborn-whitegrid') #grid style is used

  def fun(predictions, i): #creates the bar plot on predictions
    plt.bar(['GlaucomaNegative', 'GlaucmaPositive'], predictions[0], color=['#42f557', '#f54242'], label='Negative: predictions[0][0] \nPositive: predictions[0][0]')
    plt.ylim(0, 1)
    plt.legend() #put the lable/legend on images
    plt.title(f'image: {i}') #put the title on images
  
  length = len(predictions)
  if length > 1: #if there is predictions are available for more then one images
    pass
    #determine no of rows and columns in output figure
    rows = length/2
    coloums = int(length/rows)
    
    for i in range(length):
      try:
        plt.subplots(rows, columns, i+1) #create subplots in based on number of predictions available
        fun(predictions[i][0], i)
      except:
        print('Error: unable to plot image %d'%(i))
                
  else: #othewise for single image prediction
    fun(predictions[0], 1)
    
  plt.savefig('results.pdf') #save figure before showing it
  print('Results are saved as result.pdf in same directory')
  plt.show() #shoe the figure
  plt.close()  #close the figure
    
def plot_accuracy(history, epochs): #this function will plot the aacuracy of model in line graph
  plt.style.use('seaborn-whitegrid') #grid style is used
    
  acc = history.history['accuracy'] #fetch training accuracy of model
  val_acc = history.history['val_accuracy'] #fetch validation accuracy of model
    
  loss = history.history['loss'] #fetch training loss of model
  val_loss = history.history['val_loss'] #fetch validation loss of model
    
  epochs_range = range(epochs)
    
  plt.figure(figsize=(8,8)) #detrmine the size of output figure
  plt.subplot(1, 2, 1) #create 2 subplots in same row
  plt.plot(epochs_range, acc, label='Training Accuracy') #plot training acuracy on line graph
  plt.plot(epochs_range, val_acc, label='Validation Accuracy') #plot validation on line graph
  plt.legend(loc='lower right') #put the label on graph
  plt.title('Training and Validation Accuracy') #put the title on graph
    
  plt.subplot(1, 2, 2)
  plt.plot(epochs_range, loss, label='Training loss') #plot training loss on line graph
  plt.plot(epochs_range, val_loss, label='Validation loss') #plot validation loss on line graph
  plt.legend() #put the label on graph
  plt.title('Training and Validation loss') #put the title on graph
  
  fig = plt.gcf() #get current figure
  fig.savefig('accuracyPlot.pdf') #will save the figure
  plt.show() #show the figure
    
def plot_samples():
  print('function not available')
  pass
