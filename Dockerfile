# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

WORKDIR /panel
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=panel

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
