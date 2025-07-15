#!/bin/bash
mavproxy.py \
  --master=/dev/ttyACM0 \
  --out=udp:<GCS_ZEROTIER_IP>:14550 \
  --daemon

Give permissions and add to cron for auto-startup at reboot:

chmod +x ~/start_mavproxy.sh
crontab -e
@reboot /home/pi/start_mavproxy.sh

