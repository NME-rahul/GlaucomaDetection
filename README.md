## required modules:
	os
	sys
	numpy
	pathlib
	opencv-python
	matplotlib.pyplot
	tensorflow==1.13.2
	tensorflow-object-detection-api		
	

* start from main.py run
	> python main.py [arguments]
		
	  train_model - type if you wants to train model before model inference
	
	  dflt / None - it loads existing model for model inference

* while giving path as input always give directory path without file name
* while performing image processing always give path to the single image or path of directoy where you have two folder named as "Train" and "Validation"
* path for data images if you wants to retrain model: https://drive.google.com/drive/folders/1Y6mw98eAQLHaEiYNme97PbW5LNb0CXxm?usp=sharing

### Accuracy plot
<img width="488" alt="Screenshot 2022-10-05 at 2 06 09 AM" src="https://user-images.githubusercontent.com/100432854/201436678-241b3fcb-e960-4116-9930-caf96304c17d.png">

---

### Results of previously inference model:
<img width="1312" alt="Screenshot 2022-11-06 at 3 27 45 PM" src="https://user-images.githubusercontent.com/100432854/201436836-0a60deee-0161-4eb3-9120-c61c76dc5c60.png">
