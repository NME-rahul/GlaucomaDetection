## Problem Statement -
Glaucoma is one of the main cause of blindness and is irreversible. Caused by elevated intraocular pressure, it do harm to optic nerve head which sends images to your brain. Glaucoma result in structure change of optic disk and cup. most people with glaucoma have no early symptoms or pain. WHO has estimated that 4.5 million people are blind due to glaucoma. In India, at least 12 million people affected and nearly 1.2 million people blind from the disease. More than 90 percent of cases of glaucoma remain undiagnosed in the community. There is no cure (yet) for glaucoma, but if it’s caught early, you can preserve your vision. we can prevent vision loss by the **measurement of cup-to-disk diameter ratio(CDR)** in retinal images to detect glaucoma. CDR greater than 0.65 is seen as the symbol of glaucomatous in clinical practice.

---

## required modules:
	os
	sys
	numpy
	pathlib
	opencv-python
	matplotlib.pyplot
	tensorflow==1.13.2
	tensorflow-object-detection-api		
	

* Start from main.py, run

	  python main.py [arguments]
	  
	arguments:
	> train_model - type if you wants to train model before model inference.
	
	> existing - use after argument 'train_model' if you wants to use existing model to retrain.

	> dflt / None - it loads existing model for model inference.

* While giving path as input always give directory path without file name
* While performing image processing always give path to the single image or path of directoy where you have two folder named as "Train" and "Validation"
* Path for data images if you wants to retrain model: https://drive.google.com/drive/folders/1Y6mw98eAQLHaEiYNme97PbW5LNb0CXxm?usp=sharing

### Accuracy plot
<img width="488" alt="Screenshot 2022-10-05 at 2 06 09 AM" src="https://user-images.githubusercontent.com/100432854/201436678-241b3fcb-e960-4116-9930-caf96304c17d.png">

---

### Results of previously inference model:
<img width="1312" alt="Screenshot 2022-11-06 at 3 27 45 PM" src="https://user-images.githubusercontent.com/100432854/201436836-0a60deee-0161-4eb3-9120-c61c76dc5c60.png">

---

* you can also do this by diretly running colab file: https://colab.research.google.com/drive/1owjTdPC7TvzdsDo2071omKNmHsSIO2oV
* test data used in the prpgram: https://drive.google.com/drive/folders/1Y6mw98eAQLHaEiYNme97PbW5LNb0CXxm?usp=sharing
