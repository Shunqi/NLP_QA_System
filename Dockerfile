# Ubuntu Linux as the base image
FROM ubuntu:16.04
# Set UTF-8 encoding
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
# Install packages, you should modify this based on your program
RUN apt-get -y update && \
    apt-get -y upgrade && \
    apt-get -y install python3-pip python3-dev


RUN pip3 install spacy=="2.0.12" && \
    pip3 install nltk && \
    pip3 install numpy && \
    pip3 install gensim && \
    pip3 install bs4

RUN python3 -m spacy download en_core_web_lg
RUN python3 -m nltk.downloader punkt
RUN python3 -m nltk.downloader wordnet

RUN mkdir QA

# Change the permissions of programs, you may add other command if needed
CMD ["chmod 777 ask"]
CMD ["chmod 777 answer"]

# Add the files into container, under QA folder, modify this based on your need
ADD answer /QA
ADD ask /QA
ADD src /QA

# Set working dir as /QA
WORKDIR /QA

# ENTRYPOINT ["/bin/bash", "-c"]