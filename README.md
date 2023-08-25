## Problem Statement -
Glaucoma is one of the main cause of blindness and is irreversible. Caused by elevated intraocular pressure, it do harm to optic nerve head which sends images to your brain. Glaucoma result in structure change of optic disk and cup. most people with glaucoma have no early symptoms or pain. WHO has estimated that 4.5 million people are blind due to glaucoma. In India, at least 12 million people affected and nearly 1.2 million people blind from the disease. More than 90 percent of cases of glaucoma remain undiagnosed in the community. There is no cure (yet) for glaucoma, but if it’s caught early, you can preserve your vision. we can prevent vision loss by the **measurement of cup-to-disk diameter ratio(CDR)** in retinal images to detect glaucoma. CDR greater than 0.65 is seen as the symbol of glaucomatous in clinical practice.


<img src = "https://www.mdpi.com/mathematics/mathematics-09-02237/article_deploy/html/images/mathematics-09-02237-g001-550.jpg"
     alt = "image"
     align = "middle">


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
	

* Start from installing miniconda(recomended).
	
* run miniconda terminal and create conda environment.
	
	  conda create --name tf python=3.10

* Clone the directory and change in it.
	  
	  git clone https://github.com/NME-rahul/GlaucomaDetection.git
	  
	  cd GlaucomaDetection
	  
* install required modules, run.

	  pip install -r requirments.txt
	
* run command,

	  python main.py [arguments]
	  
	arguments:
	> train_model - type if you wants to train model before model inference.
	
	> existing - use after argument 'train_model' if you wants to use existing model to retrain.

	> make_predictions / None - it loads existing model for model inference.
	
<br>
<a href="https://youtu.be/hpKa6J_U2fw">Demo Video</a>
<br><br>

**Note-** this will not work in macos due to errors occuring while installing tensorflow module whenever this error resolve this might works.

---


* While giving path as input always remember it consists only tow class one is Negative and other is Positive.
* Perform image preprocesssing if you think it's necessary otherwise skip it.
* Path for data images if you wants to retrain model: https://drive.google.com/drive/folders/1gL1e6TDdsdxCjJHID2WSYtt6McG2Ci-U?usp=sharing

### Accuracy plot
<img width="488" alt="Screenshot 2022-10-05 at 2 06 09 AM" src="https://user-images.githubusercontent.com/100432854/201436678-241b3fcb-e960-4116-9930-caf96304c17d.png">

---

### Results of previously inference model:
<img width="1312" alt="Screenshot 2022-11-06 at 3 27 45 PM" src="https://user-images.githubusercontent.com/100432854/201436836-0a60deee-0161-4eb3-9120-c61c76dc5c60.png">

---

* [you can also do this by diretly running colab file](https://colab.research.google.com/drive/1uugqIAeCxN32L4P7tOAuXZbIw3YfHM1J?usp=sharing)
* [test data used in the prpgram](https://drive.google.com/drive/folders/1gL1e6TDdsdxCjJHID2WSYtt6McG2Ci-U?usp=sharing)

<details>

* Clone the repositoy in brainypi.
* Change directory to Glaucoma Detection(remove space from directory name if any).
* Run following commands in brainypi(before this you must have docker installed).

		docker build -f dockerfile -t proj:GlaucomaDetection ~/GlaucomaDetection/

		docker run -ti {projectName|projID}

* The container will run in interactive mode, perfrom actions as given in menu(appears after running container), initialy the container doesn't have any model so start by training model or add the model from the link given in 1.

> project file size: 3.23 GB <br>
> project file size with added model: 3.23 + 2.65 GB

<summary>Click to view implemetation steps in brainypi</summary>
</details>

---

![030](https://github.com/NME-rahul/GlaucomaDetection/assets/100432854/24a1608b-36bb-4e60-80ed-dc76a1efb719)

