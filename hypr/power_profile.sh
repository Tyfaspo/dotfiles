#!/bin/zsh

CURRENT=$(powerprofilesctl get)
cycle() {
    if [[ "$CURRENT" = "power-saver" ]]; then
        echo "Changing to Balanced"
        powerprofilesctl set balanced
        CURRENT=$(powerprofilesctl get) # Update CURRENT
				pkill -SIGRTMIN+10 waybar
    elif [[ "$CURRENT" = "balanced" ]]; then
        echo "Changing to Performance"
        powerprofilesctl set performance
        CURRENT=$(powerprofilesctl get) # Update CURRENT
        echo "Enabling shadows and blur"
        cat <<EOF > ~/.config/hypr/power_related.conf
decoration:blur:enabled = true
decoration:shadow:enabled = true
misc:vfr = false
EOF
				pkill -SIGRTMIN+10 waybar
    elif [[ "$CURRENT" = "performance" ]]; then
        echo "Changing to Power Saving"
        powerprofilesctl set power-saver
        CURRENT=$(powerprofilesctl get) # Update CURRENT
        echo "Disabling shadows and blur"
        cat <<EOF > ~/.config/hypr/power_related.conf
decoration:blur:enabled = false
decoration:shadow:enabled = false
misc:vfr = true
EOF
				pkill -SIGRTMIN+10 waybar
    fi
}

if [[ "$1" == "--cycle" ]]; then
    cycle
elif [[ "$1" == "--current" ]]; then
    if [[ "$CURRENT" == "power-saver" ]]; then
			echo ""
		elif [[ "$CURRENT" == "balanced" ]]; then
			echo ""
		elif [[ "$CURRENT" == "performance" ]]; then
			echo ""
		fi
else
    echo "Usage: $0 [--cycle | --current]"
    exit 1
fi

