# syntax=docker/dockerfile:1

# === Docker Image Definition === #

FROM python:3.9.13-slim-buster

WORKDIR /app
# COPY requirements.txt requirements.txt