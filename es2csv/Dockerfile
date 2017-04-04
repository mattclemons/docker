
FROM debian:latest

MAINTAINER matt.clemons@gmail.com

RUN apt-get -y update && apt-get install -y python-pip

RUN pip install es2csv

ADD . /root/
