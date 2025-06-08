# mqtt2influx

> A lightweight Python tool (and companion Docker image) to bridge your MQTT sensor streams into InfluxDB for time-series analysis.  
> Easily configured with a `.env` file and a topic map.
> Run from the command line or docker/k3s. 
> Ideal for self-hosted dashboards, IoT monitoring, and Grafana.


[![Python Version](https://img.shields.io/badge/python-3.9%2B-blue.svg)]()
[![License](https://img.shields.io/badge/license-GPL--3.0-red.svg)]()

---

## 🤔 Why This Repo Exists

MQTT is a go-to protocol for IoT and sensor data transmission - but it doesn't store data.  
InfluxDB is perfect for storing time-series data - but it doesn't talk MQTT out of the box.



**mqtt2influx** bridges that gap:

- ✅ Subscribes to MQTT topics with minimal setup
- ✅ Writes values directly into InfluxDB with timestamps
- ✅ Enables easy graphing and querying with Grafana or Chronograf
- ✅ Eliminates the need for custom Node-RED flows or Python scripts

Whether you're monitoring temperature sensors, home automation events, or custom devices - this repo gives you a fast path from **MQTT to metrics**.


---

## 📖 Table of Contents

- [Features](#features)  
- [Quickstart](#quickstart)  
- [Configuration](#configuration)  
- [Usage](#usage)  
- [Topics Mapping](#topics-mapping)  
- [Docker Support](#docker-support)  

---

## 🧰 Features

- Simple yet powerful script to bridge MQTT → InfluxDB  
- Configurable via environment variables or `.env` file  
- Flexible topic-to-measurement mapping (`topics.txt`)  
- Ideal for IoT setups, telemetry collection, or sensor dashboards  

---

## 🚀 Quickstart

```bash
git clone https://github.com/mortylabs/mqtt2influx.git
cd mqtt2influx
cp .env.example .env
nano .env  # configure MQTT + Influx credentials
pip install -r requirements.txt
python mqtt2influx.py
```

## ⚙️ Configuration

Start by copying the example config:

```bash
cp .env.example .env
```
Then edit .env to set your connection and subscription parameters:
| Variable        | Description                      | Required | Example                    |
| --------------- | -------------------------------- | -------- | -------------------------- |
| `MQTT_HOST`     | MQTT broker hostname or IP       | ✅        | `mqtt.local`               |
| `MQTT_PORT`     | MQTT broker port                 | ✅        | `1883`                     |
| `MQTT_USER`     | MQTT username (optional)         | ❌        | `myuser`                   |
| `MQTT_PASS`     | MQTT password (optional)         | ❌        | `mypassword`               |
| `INFLUX_URL`    | Full URL to your InfluxDB server | ✅        | `http://influx.local:8086` |
| `INFLUX_ORG`    | InfluxDB organization name       | ✅        | `homelab`                  |
| `INFLUX_BUCKET` | InfluxDB bucket to store data    | ✅        | `mqtt_data`                |
| `TOPICS_FILE`   | Path to topic mapping file       | ✅        | `topics.txt`               |

Next, define the topics you wish to subscribe to in the text file **`topics.txt`** as follows:<BR>
```
MY_TOPIC1    SHORT_NAME1
MY_TOPIC2    SHORT_NAME2
```
### 🗂️ MQTT Topics to Influx Mapping

Define which MQTT topics to subscribe to and how they map to InfluxDB measurements using a simple `topics.txt` file.

#### 🔧 Example `topics.txt`
```
home/sensors/temperature temperature
home/sensors/humidity    humidity
garden/moisture/level    soil_moisture
```

Each line follows the format:
```
<mqtt_topic> <influx_measurement>
```

#### 💡 Notes
- Whitespace separates the MQTT topic from the desired InfluxDB measurement name.
- Wildcards (e.g., home/+/temperature, sensors/#) can be used for grouped subscriptions.
- The payload of each MQTT message is assumed to be a numeric value (e.g., temperature, voltage, etc.).
- All data is timestamped automatically when written to InfluxDB.

💡 Pro tip: You can use wildcards like home/+/temperature in topics.txt to subscribe to topic groups.


## 🐳 Docker Support

Run `mqtt2influx` using Docker for easy deployment:

### 🔨 Build the Docker image

```
bash
./build.sh
```
This will build a minimal Python image with the required dependencies and your current config.

### ▶️ Run the container
```
./run.sh
```
Make sure your .env file and topics.txt are available in the container's context (or volume-mounted).

