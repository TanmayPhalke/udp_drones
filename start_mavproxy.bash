#!/bin/bash
mavproxy.py \
  --master=/dev/ttyACM0 \
  --out=udp:100.113.114.176:14550 \
  --daemon