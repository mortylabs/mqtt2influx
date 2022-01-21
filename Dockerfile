FROM python:3.9.4-slim-buster
#FROM python:3.9.4-alpine3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY mqtt2influx.py .
#COPY topics.txt .

#influx
EXPOSE 8086
#mqtt
EXPOSE 31883

CMD [ "python3", "mqtt2influx.py" ]
