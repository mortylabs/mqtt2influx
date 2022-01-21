docker build --tag mqtt2influx .
docker tag mqtt2influx mortyone/mqtt2influx:latest
docker push mortyone/mqtt2influx:latest

#docker login
#kubectl create secret generic regcred --from-file=.dockerconfigjson=/home/pi/.docker/config.json --type=kubernetes.io/dockerconfigjson
#kubectl create cm cm-mqtt2influx --from-file=topics.txt --dry-run -o yaml
