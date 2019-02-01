#!/bin/sh

echo "Avahi resolver"

avahi-browse -rtp _floor1._sub._coap._udp >avahi.txt

sleep 1

ip=$(python IPresolver.py)

sleep 1
java -jar leshan-client-demo-1.0.0-SNAPSHOT-jar-with-dependencies.jar -u $ip &
echo "CLIENT READY! Run Camera now"

python alpr_camera.py