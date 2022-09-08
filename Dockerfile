# syntax=docker/dockerfile:1

# === Docker Image Definition === #

FROM python:3.8-slim-buster

# === Image metadata === #
LABEL vendor="UPCnet"
LABEL author="wasym.atieh@upcnet.es"
LABEL name="PuppetSync"
LABEL version="1.0.0"
LABEL description="Syncing app between Puppet & CMDB Databases."

# Creating working directory
WORKDIR /app
# Adding source code to image
COPY . .
# Installing requirements
RUN pip3 install -r requirements.txt

CMD [ "python3", "sync.py" ]