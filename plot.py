import matplotlib.pyplot as plt

def plot_predictions(predictions):
  plt.style.use('seaborn-whitegrid')
    
  if len(predictions) > 1:
        
    length = len(predictions)
    rows = length/2
    coloums = int(length/rows)
        
    for i in range(length):
      try:
        plt.subplots(rows, columns, i+1)
        fun(predictions[i], i)
      except:
        print('Error: unable to plot image %d'%(i))
                
  else:
    fun(predictions[0], 1)
  
  def fun(predictions, i):
    plt.bar(['GlaucomaNegative', 'GlaucmaPositive'], predictions[0], color=['#42f557', '#f54242'], label='Negative: predictions[0][0] \nPositive: predictions[0][0]')
    plt.ylim(0, 1)
    plt.legend()
    plt.title(f'image: {i}')
    
  plt.savefig('results.pdf')
  print('Results are saved as result.pdf in same directory')
  plt.show()
  plt.close()
    
def plot_accuracy(history, epochs):
  plt.style.use('seaborn-whitegrid')
    
  acc = history.history['accuracy']
  val_acc = history.history['val_accuracy']
    
  loss = history.history['loss']
  val_loss = history.history['val_loss']
    
  epochs_range = range(epochs)
    
  plt.figure(figsize=(8,8))
  plt.subplot(1, 2, 1)
  plt.plot(epochs_range, acc, label='Training Accuracy')
  plt.plot(epochs_range, val_acc, label='Validation Accuracy')
  plt.legend(loc='lower right')
  plt.title('Training and Validation Accuracy')
    
  plt.subplot(1, 2, 2)
  plt.plot(epochs_range, loss, label='Training loss')
  plt.plot(epochs_range, val_loss, label='Validation loss')
  plt.legend()
  plt.title('Training and Validation loss')
  
  plt.show()
    
def plot_samples():
  print('function not available')
  pass
