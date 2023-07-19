FROM python:3.8-slim-buster

WORKDIR /app

ARG PORT=5080
ENV PORT ${PORT}

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

CMD python3 server.py
