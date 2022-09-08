# syntax=docker/dockerfile:1

# === Docker Image Definition === #

FROM python:3.8-slim-buster

# Creating working directory
WORKDIR /app
# Adding source code to image
COPY . .
# Installing requirements
RUN pip3 install -r requirements.txt

CMD [ "python3", "sync.py" ]