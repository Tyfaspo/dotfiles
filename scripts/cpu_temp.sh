#!/usr/bin/zsh
for (( ; ; ))
do
    sensors | grep Tctl: | cut -d "+" -f 2
    sleep 5
done
