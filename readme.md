# 🏏 T20 Ticket Sniper

An automated Python monitor that continuously checks BookMyShow for T20 ticket availability. When tickets drop, it triggers a multi-channel alarm system including local laptop sirens, Telegram alerts, and ultra-urgent `ntfy` mobile push notifications with a remote kill switch.

## ⚙️ Setup(Linux)

```bash
user@machine:~/project$ git clone https://github.com/Psychopomp3012/ticket.git
user@machine:~/project$ cd ticket
user@machine:~/project/ticket$ python3 -m venv venv
user@machine:~/project/ticket$ source venv/bin/activate
user@machine:~/project/ticket$ pip install -r requirements.txt
```

## Execute:
### Option - 1: Testing
```bash
user@machine:~/project/ticket$ python main.py # direct execution
```
### Option - 2: As background process
```bash
user@machine:~/project/ticket$ nohup python t20_monitor.py 2>&1 &  # As a background process
```
```bash
user@machine:~/project/ticket$ nohup python t20_monitor.py > log.txt 2>&1 &  # As a background process and log storage as well
```
### Option - 3: Always-On System Service
#### Create a file in this path: 

```bash
user@machine:~/project/ticket$ sudo nano /etc/systemd/system/t20-monitor.service
```

#### File content: 
```Ini, TOML
[Unit]
Description=T20 World Cup Ticket Monitor
# Wait for the network to be fully connected
After=network-online.target
Wants=network-online.target
# Crucial: Wait for your secondary drive to be mounted
RequiresMountsFor="/media/sachin/New Volume"

[Service]
# Run as your normal user, not root
User=your_username
WorkingDirectory=/path/to/your/project

# For better loging in journalctl 
Environment=PYTHONUNBUFFERED=1

Environment="DISPLAY=:0"
Environment="XDG_RUNTIME_DIR=/run/user/1000"

# Use the virtual environment's Python to run the script
ExecStart=/path/to/your/project/venv/bin/python main.py
Restart=always  # or on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

## Requirements in .env:
```Ini, TOML
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id

# NTFY Push Notification Topics
TOPIC_ALERT=your_secret_alert_topic
TOPIC_ACK=your_secret_acknowledgment_topic
```

## Check the PID running in your local machine:
```bash
user@machine:~/project/ticket$ ps aux | grep main.py 
```

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

### Moniter: 
journalctl -u t20-monitor.service -f