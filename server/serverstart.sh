#!/bin/sh

echo "Initiating Broker..."

# Kill stale Avahi publish
ps ax | grep avahi-publish | awk '{ print $1 }' | xargs kill -9
ps ax | grep leshan | xargs kill -9
# start leshan demo server
java -jar leshan-server-demo-1.0.0-SNAPSHOT-jar-with-dependencies.jar & # -lh 192.168.0.8 &

sleep 5 # wait for the LWM2mServer to be started

avahi-publish-service ParkingTUE _coap._udp 5683 “/PARKINGBROKER” --sub _floor1._sub._coap._udp &

echo "SERVER READY!!"
