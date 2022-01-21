#!/usr/bin/python3
import sys
import requests
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import logging
from os import path, environ
from dotenv import load_dotenv
import json

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

INFLUX_SERVER   = environ.get("INFLUX_SERVER", '192.168.1.15')
INFLUX_PORT     = environ.get("INFLUX_PORT", 8086)
INFLUX_DB       = environ.get("INFLUX_DB", 'sensors')
INFLUX_USER     = environ.get("INFLUX_USER", 'root')
INFLUX_PASS     = environ.get("INFLUX_USER", 'root')
MQTT_SERVER     = environ.get("MQTT_SERVER", 'localhost')
MQTT_PORT       = environ.get("MQTT_PORT", 31883)
MQTT_USER       = environ.get("MQTT_USER", 'mqtt_user')
MQTT_PASS       = environ.get("MQTT_PASS", 'mqtt_password')

LOGGING_LEVEL   = environ.get("LOGGING_LEVEL", 'INFO')

MQTT_TOPICS     = {}
ct_errors       = 0


def influx_post (db, measurement, value, server=INFLUX_SERVER, port=INFLUX_PORT, tag1_name=None, tag1_value=None, dt=None):
        r = None
        try:
            ts = '' if dt is None else ' ' + str(int(dt.timestamp())) + "000000000"
            url_string = 'http://' + server + ':' + str(port) + '/write?db=' + db
            tags = "," + tag1_name + "=" + str(tag1_value) if tag1_name is not None else ''
            data_string = measurement + tags + " value=" + str(value) + ts
            logging.debug("url=" + url_string + " data = " + data_string)
            r = requests.post(url_string, data=data_string)
            if r.status_code != 204:
                raise ValueError("influx_post: status_code=" + str(r.status_code) + " txt=" + str(r.text))
        except Exception as e:
            logging.exception(str(e))



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    logging.info ("on_connect: result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    for topic in MQTT_TOPICS:
        client.subscribe(topic)
        logging.debug("subscribed: " + str(topic))




# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    global ct_errors
    measurement = MQTT_TOPICS[msg.topic]
    payload = msg.payload.decode('utf8')
    if payload.replace(".", "").isnumeric() : #payload_type is int or payload_type is float or payload_type is bool:
        influx_post(server=INFLUX_SERVER, port=INFLUX_PORT, db=INFLUX_DB, measurement=MQTT_TOPICS[msg.topic], tag1_value=None,value=float(payload), dt=None)
    else:
        json_object = None
        try:
            json_object = json.loads(payload, parse_float=float)
            for x in json_object:
                if "mac" not in x.lower() and "rssi" not in x.lower():
                    influx_post(server=INFLUX_SERVER, port=INFLUX_PORT, db=INFLUX_DB,
                                  measurement=measurement + "_"+x, tag1_value=None, value=json_object[x], dt=None)

        except Exception as e:
            logging.exception ("on_message: " + str(e))
            ct_errors += 1
            if ct_errors > 50:
                logging.error("error count: " + str(ct_errors) + ", exiting...")
                sys.exit(1)


if __name__ == "__main__":
    if   str(LOGGING_LEVEL) == "DEBUG":
         _LOGGING_LEVEL = logging.DEBUG
    elif str(LOGGING_LEVEL) == "INFO":
         _LOGGING_LEVEL = logging.INFO
    elif str(LOGGING_LEVEL) == "WARN":
            _LOGGING_LEVEL = logging.WARN
    elif str(LOGGING_LEVEL) == "ERROR":
            _LOGGING_LEVEL = logging.ERROR
    elif str(LOGGING_LEVEL) == "EXCEPTION":
            _LOGGING_LEVEL = logging.EXCEPTION
    else: _LOGGING_LEVEL = logging.DEBUG

    logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y/%m/%d %I:%M:%S %p', level=_LOGGING_LEVEL)
    logging.info("starting...")
    logging.info("LOGGING_LEVEL = " + str(LOGGING_LEVEL))

    d = {}
    config_file = "/config/topics.txt"
    if not path.isfile(config_file): config_file = "topics.txt"
    logging.debug("checking for " + config_file + "...")
    if path.isfile(config_file):
        logging.info("loading "+config_file + "...")
        with open(config_file) as f:
            for line in f:
                (key, val) = line.split()
                logging.info (key + " : " + val)
                d[key] = val
    if len(d) > 0:
        MQTT_TOPICS = d


    logging.info("connecting to influx (" + INFLUX_SERVER + ":" + str(INFLUX_PORT) + " db: " + INFLUX_DB + ") ...")
    influx_client = InfluxDBClient(INFLUX_SERVER, INFLUX_PORT, database=INFLUX_DB)
    try:
        logging.info("creating database if not exist...")
        influx_client.create_database(INFLUX_DB)
    except Exception as ex:
        logging.warning(ex)

    logging.info("connecting to mqqt broker (" + MQTT_SERVER + ":" + str(MQTT_PORT)  + ") ...")
    mqtt_client = mqtt.Client()
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message

    mqtt_client.connect(MQTT_SERVER, int(MQTT_PORT), 60)
    mqtt_client.username_pw_set(MQTT_USER, MQTT_PASS)

    mqtt_client.loop_forever()
