FROM python:3.9.6-buster

WORKDIR /trade_web_app

# python environment
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . /trade_web_app/

ADD /docs/requirements.txt /trade_web_app/
RUN pip install --upgrade pip && pip install -r requirements.txt