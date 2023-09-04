#!/bin/bash

xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/alex/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/alex/.config/chromium/Default/Preferences

pushd /home/alex/raspi-frag-frame; screen -d -m python -m http.server

/usr/bin/chromium-browser --noerrdialogs --disable-infobars --kiosk http://0.0.0.0:8000/ &

while true; do
   xdotool keydown ctrl+Tab; xdotool keyup ctrl+Tab;
   sleep 10
done
