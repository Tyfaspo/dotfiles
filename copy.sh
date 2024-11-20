#!/bin/zsh
USER=$(whoami)

if [ "$USER" = "root" ]; then
  echo "do not run as root"
  exit 0
fi

CONFIG="/home/$USER/.config"

FOLDERS=("kitty" "qtile" "dunst" "hypr" "fastfetch" "nvim" "rofi" "waybar" "thefuck" "wlogout")

# copy from .config
for FOLDER in "${FOLDERS[@]}"; do
  if [ -d "$CONFIG/$FOLDER" ]; then
    echo "$FOLDER exists in .config"
    cp -r "$CONFIG/$FOLDER" "./"
  else
    echo "$FOLDER does not exist in .config"
  fi
done

# since i use .vimrc
if [ -f "/home/$USER/.vimrc" ]; then 
  cp "/home/$USER/.vimrc" "./"
fi

echo "DONE"
