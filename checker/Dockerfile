FROM python:3.8-buster as builder

ENV TZ=Europe/Moscow
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get install --no-install-recommends -y wget unzip

#WORKDIR /default_datasets
#RUN wget --no-verbose -O datasets.zip https://storage.yandexcloud.net/hackai-datasetrsv/profsa.zip && \
#    unzip -qq datasets.zip && rm datasets.zip

WORKDIR /default_datasets
COPY fixed_datasets.zip .
RUN unzip -qq fixed_datasets.zip && rm fixed_datasets.zip
COPY requirements.txt .
RUN pip3 install -r requirements.txt && rm requirements.txt

WORKDIR /checker

ENV FLASK_APP=app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python3", "-m", "flask", "run"]
