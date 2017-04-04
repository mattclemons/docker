
#docker run -v /home/matt/Downloads:/root mattclemons/es2csv es2csv 
FROM debian:latest
RUN apt-get -y update && apt-get install -y python-pip
RUN pip install es2csv
ADD . /root/
