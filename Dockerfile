# This must match version in requirements.txt
FROM mcr.microsoft.com/playwright/python:v1.40.0-jammy
# https://stackoverflow.com/questions/63936578/docker-how-to-make-python-3-8-as-default
# FROM ubuntu:bionic

# RUN apt update && apt install software-properties-common -y
# RUN add-apt-repository ppa:deadsnakes/ppa && apt install python3.8-dev -y
# RUN ln -s /usr/bin/python3.8 /usr/bin/python3

# BEWARE: your OS is not officially supported by Playwright; installing dependencies for Ubuntu as a fallback.
# FROM python:3.8-slim-buster

WORKDIR /app

ARG PORT=5080
ENV FLASK_APP "app.py"
ENV FLASK_DEBUG "1"
ENV PORT ${PORT}

# https://github.com/regebro/tzlocal#notes-on-docker
ENV TZ "Asia/Taipei"
ARG DEBIAN_FRONTEND="noninteractive"

# https://dev.to/0xbf/set-timezone-in-your-docker-image-d22
RUN apt-get update && \
    apt-get install -y tzdata && \
    ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime && \
    dpkg-reconfigure -f noninteractive tzdata

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN playwright install
# RUN playwright install-deps

# https://stackoverflow.com/questions/35560894/is-docker-arg-allowed-within-cmd-instruction
CMD python3 -m flask run --host 0.0.0.0 --port ${PORT}
