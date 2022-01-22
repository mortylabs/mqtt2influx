# mqtt2influx

This simple python app subscribes to topics on a MQTT Broker of your choice, and saves the data to InfluxDB.

Environment variables such as server names, port, credentials etc can be configured in .env for convenience if running from the command line.

A text file "topics.txt" holds a map of MQTT topics to subscribe to and the associated Influx measurement name:
*topics.txt*
MY_TOPIC1 SHORT_NAME1
MY_TOPIC2 SHORT_NAME2

To build a docker image, see buid.sh as an example.

See k3s_link_here for an example of using the docker image in kubernetes.
