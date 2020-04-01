FROM python:3.5.2

WORKDIR /usr/src/vgiws

COPY ./requirements.txt ./

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils && \
    apt-get install -qqy software-properties-common --no-install-recommends && \
    apt-get update && \
    apt-get install -y python-gdal python3-gdal gdal-bin

RUN pip install --no-cache-dir -r requirements.txt

ENV TZ=America/Sao_Paulo

EXPOSE 8888

CMD [ "python", "main.py" ]
