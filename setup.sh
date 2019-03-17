#!/usr/bin/env bash

mkdir -p thirdparty
cd thirdparty

# Advanced GNOME integration
notify_send_version=1.0
wget https://github.com/vlevit/notify-send.sh/archive/v${notify_send_version}.tar.gz
tar -xzf v${notify_send_version}.tar.gz
rm v${notify_send_version}.tar.gz
rm -r notify-send
mv notify-send.sh-${notify_send_version} notify-send
