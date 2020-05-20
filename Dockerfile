FROM python:3.7.4

WORKDIR /usr/src/vgiws

COPY ./requirements.txt ./

# Lines to avoid problems related to build image (https://github.com/phusion/baseimage-docker/issues/319)
# ENV DEBIAN_FRONTEND noninteractive
# ENV DEBIAN_FRONTEND teletype
# RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -qqy software-properties-common --no-install-recommends && \
    apt-get update && \
    apt-get install -y python-gdal python3-gdal gdal-bin

RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=America/Sao_Paulo

EXPOSE 8888

CMD [ "python", "main.py" ]
