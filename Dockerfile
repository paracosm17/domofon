FROM python:3.10-slim

WORKDIR /usr/src/app/domofon

COPY requirements.txt /usr/src/app/domofon
RUN pip install cmake
RUN pip install -r /usr/src/app/domofon/requirements.txt
COPY . /usr/src/app/domofon
