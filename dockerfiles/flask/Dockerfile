# Dockerfile-Flask

# set python alpine as base images
FROM python:3.7

# set maintaner
MAINTAINER KELVIN

# set environment variable
ENV APP /app

# run command to create directory
# instruct docker to operate there
RUN mkdir $APP
WORKDIR $APP

# copy requirements file 
COPY requirements.txt .
RUN pip install -r requirements.txt

# copy everything exluding the one listed in .dockerignore
COPY . .