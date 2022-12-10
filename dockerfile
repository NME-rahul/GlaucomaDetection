# System
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=interactive  

# Installing Dependancies
RUN apt update
RUN apt-get clean

RUN apt-get install -y python3
RUN apt-get install -y git wget python3-dev python3-pip unzip
RUN apt-get update && apt-get install -y python3-opencv

#RUN apt install -y libgl1-mesa-glx
RUN python3 -m pip install pip --upgrade
RUN pip3 install scikit-build
RUN apt-get update
RUN apt install -y cmake curl

RUN pip3 install opencv-python
RUN pip3 install tensorflow
RUN pip3 install matplotlib
RUN pip3 install numpy
RUN pip3 install scipy

ENV PYTHONIOENCODING=utf8 
RUN echo "$FOO $BAR $PYTHONIOENCODING"

ADD main.py .
ADD plot.py .
ADD train_model.py .
ADD image_preprocess.py .

CMD ["python3", "./main.py", "train_model"]
