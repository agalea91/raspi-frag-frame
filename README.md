# Raspberry PI Fragment Frame

Digital display of rotating book fragments from Notion.

## Setup raspberry PI

Follow guide:

https://www.raspberrypi.com/tutorials/how-to-use-a-raspberry-pi-in-kiosk-mode/

Copy `kiosk.sh` to home dir on raspberry pi.

Copy `kiosk.service` from this repo to `/lib/systemd/system/kiosk.service`

Install service

```
sudo systemctl enable kiosk.service
```

## Update HTML with fragment from Notion DB

Install dependencies

```
pip install requests python-dotenv
```

Run script

```
python update_html.py
```

## Start/stop kiosk

```
sudo systemctl start kiosk.service
sudo systemctl stop kiosk.service
```

## Cron job to swap daily

Must install as root

```
>>> sudo su
>>> crontab -e
```

Run daily at midnight EST

```
0 5 * * * /bin/bash /home/alex/raspi-frag-frame/swap_fragment.sh >> /home/alex/raspi-frag-frame/cron.log 2>&1
```
