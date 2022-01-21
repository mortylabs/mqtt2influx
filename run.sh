export container_id=`docker run -d -p 8086:8086 -p 31884:31883 mqtt2influx`
sleep 10
docker logs $container_id
docker exec -it $container_id sh
