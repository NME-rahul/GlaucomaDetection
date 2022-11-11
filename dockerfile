# System
FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive  

# Installing Dependancies
RUN apt update
RUN apt-get clean 

RUN apt-get update
RUN apt-get install -y python3
RUN apt-get install -y git wget python3-dev python3-pip unzip

RUN python3 -m pip install pip --upgrade
RUN pip3 install scikit-build
RUN apt-get update
RUN apt install -y cmake curl

RUN pip3 install opencv-python

#RUN pip install https://storage.googleapis.com/tensorflow/mac/cpu/tensorflow-1.13.1-py3-none-any.whl
#RUN pip install https://storage.googleapis.com/tensorflow/raspberrypi/tensorflow-1.14.0-cp34-none-linux_armv7l.whl
#RUN pip3 install tensorflow-object-detection-api

RUN pip3 install matplotlib
RUN pip3 install numpy

ENV PYTHONIOENCODING=utf8 
RUN echo "$FOO $BAR $PYTHONIOENCODING"

# Copy neccessary file like inference program etc to docker image
COPY ./ /opt/
