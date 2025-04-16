#!/bin/zsh

hyprctl devices | grep -A 5 "Keyboard" | grep "active keymap" | tail -n 1
