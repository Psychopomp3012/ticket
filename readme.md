# 🏏 T20 Ticket Sniper

An automated Python monitor that continuously checks BookMyShow for T20 ticket availability. When tickets drop, it triggers a multi-channel alarm system including local laptop sirens, Telegram alerts, and ultra-urgent `ntfy` mobile push notifications with a remote kill switch.

## ⚙️ Setup

```bash
user@machine:~/project$ git clone https://github.com/Psychopomp3012/ticket.git
user@machine:~/project$ cd ticket
user@machine:~/project/ticket$ python3 -m venv venv
user@machine:~/project/ticket$ source venv/bin/activate
user@machine:~/project/ticket$ pip install -r requirements.txt
```

## Execute:
```bash
user@machine:~/project/ticket$ python main.py # direct execution
```

## Requirements in .env:
BOT_TOKEN 
CHAT_ID 

TOPIC_ALERT 
TOPIC_ACK 

RUN: nohup python t20_monitor.py > log.txt 2>&1 & 

Look for PID : ps aux | grep test.py 

## Structure:

./components
    /check_ticket.py => check the availability of ticket 
    /telegram.py => sends msg to telegram bot 
    /laptop_warning.py => laptop siren 
    /phone_siren => ntfy 

./assets 
    /alert.wav => siren audio 

Background service file: 
sudo nano /etc/systemd/system/t20-monitor.service

### Reload the systemd manager to read your new file
sudo systemctl daemon-reload

### Enable it to start automatically on every boot
sudo systemctl enable t20-monitor.service

### Start it right now without having to reboot
sudo systemctl start t20-monitor.service

Moniter: 
journalctl -u t20-monitor.service -f