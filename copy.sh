#!/bin/bash
CURRENT_DIR=$(pwd)
USER=$(whoami)
CONFIG="/home/$USER/.config"
FOLDERS=("alacritty" "hypr" "fastfetch" "nvim" "rofi" "waybar" "thefuck" "hyprpanel")

if [ "$USER" = "root" ]; then
  echo "do not run as root"
  exit 0
fi

test_() {
		PARAL_D=$(cat /etc/pacman.conf | grep Paral)
		if [[ "$PARAL_D" == \#* ]]; then
			echo "You have parallel downloads disabled. For your convinience enable it before running script."
			exit 0
		fi
}

copy_local_to_dotfiles() {
    echo "Copying local configuration to dotfiles..."

		# copy from .config
		for FOLDER in "${FOLDERS[@]}"; do
		  if [ -d "$CONFIG/$FOLDER" ]; then
		    echo "$FOLDER exists in .config"
		    cp -r "$CONFIG/$FOLDER" "./"
		  else
		    echo "$FOLDER does not exist in .config"
		  fi
		done
		
		if [ ! -d "/home/$USER/.local/share/nautilus/scripts" ]; then
			echo "No /home/$USER/.local/share/nautilus/scripts exists, creating one"
			mkdir -p "/home/$USER/.local/share/nautilus/scripts"
		fi
		
		cp -r "/home/$USER/.local/share/nautilus/scripts" "./nautilus_scripts" 
		
		echo "DONE"
}

install_dotfiles() {
    echo "Installing dotfiles..."
		echo "Do you have yay installed? (y/n)"
		read user_input
		if [[ "$user_input" == "y" ]]; then
			echo "Skipping yay installation."
		elif [[ "$user_input" == "n" ]]; then
			echo "Installing yay."
			git clone "https://aur.archlinux.org/yay.git" "/home/$USER/yay" && cd "/home/$USER/yay"
			makepkg -si
			cd $CURRENT_DIR && rm -r "/home/$USER/yay"
		fi
		echo "Installing packages."
		yay -S --needed - < packages

		echo "Enabling sddm."
		sudo systemctl enable "sddm.service"
}

if [[ "$1" == "--sync-with-local" ]]; then
    copy_local_to_dotfiles
elif [[ "$1" == "--install" ]]; then
    install_dotfiles
elif [[ "$1" == "--test" ]]; then
		test_
else
    echo "Usage: $0 [--sync-with-local | --install | --test]"
    exit 1
fi

