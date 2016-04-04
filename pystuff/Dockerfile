FROM ubuntu:14.04
RUN apt-get -y update
RUN apt-get -y install git

# Install Python Setuptools
RUN apt-get install -y python-setuptools
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential
RUN apt-get install -y python python-dev python-distribute python-pip

# install ffmpeg
RUN apt-get install -y software-properties-common python-software-properties
RUN add-apt-repository -y ppa:mc3man/trusty-media
RUN apt-get -y update
RUN apt-get -y dist-upgrade
RUN apt-get -y install ffmpeg

ADD . /compressor
WORKDIR /compressor

CMD python main.py /root docker http://img.berkeley-pbl.com
