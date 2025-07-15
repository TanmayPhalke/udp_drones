#!/bin/bash
mavproxy.py \
  --master=/dev/ttyACM0 \
  --out=udp:<GCS_ZEROTIER_IP>:14550 \
  --daemon
