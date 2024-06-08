#!/usr/bin/zsh

if [[ "$?" == "0" ]]; then
  ip -4 -br a | grep wlan0 | cut -d "P" -f 2 | awk '{$1=$1;print}'
else
  printf "disconnected"
fi

