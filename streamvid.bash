#!/bin/bash

GCS_IP=$1
DRONE_ID=$2
PORT=$((8000 + DRONE_ID))

ffmpeg \
  -f v4l2 -input_format mjpeg -video_size 640x480 -framerate 10 -i /dev/video0 \
  -c:v libx264 -preset ultrafast -tune zerolatency -pix_fmt yuv420p \
  -f mpegts "udp://${GCS_IP}:${PORT}?pkt_size=1316"
