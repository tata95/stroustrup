FROM python:3.5  
RUN mkdir /src
ADD ./src /src/
RUN mkdir /config
ADD ./config/requirements.txt /config/
RUN pip install -r /config/requirements.txt
WORKDIR /src