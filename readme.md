# 🏏 T20 Ticket Sniper

An automated Python monitor that continuously checks BookMyShow for T20 ticket availability. When tickets drop, it triggers a multi-channel alarm system including local laptop sirens, Telegram alerts, and ultra-urgent `ntfy` mobile push notifications with a remote kill switch.

## 🗂️ Structure
```text
.
├── main.py                  # Entry point & main loop
├── requirements.txt         # Python dependencies
├── .env                     # Secrets (Do not commit!)
├── components/
│   ├── check_ticket.py      # Core scraping & availability logic
│   ├── telegram.py          # Telegram bot messaging
│   ├── laptop_warning.py    # Local system volume & audio control
│   └── phone_siren.py       # ntfy API for mobile alerts
└── assets/
    └── alert.wav            # Siren audio file
```

## ⚙️ Setup(Linux)
### Run below sequentially:
```bash
git clone https://github.com/Psychopomp3012/ticket.git
cd ticket
python3 -m venv venv # virtual environment so your system does not break
source venv/bin/activate # activate the virtual environment
pip install -r requirements.txt # install dependencies
```

### Create .env:
```Ini, TOML
# Telegram Bot Configuration
BOT_TOKEN=your_telegram_bot_token
CHAT_ID=your_telegram_chat_id

# NTFY Push Notification Topics
TOPIC_ALERT=your_secret_alert_topic
TOPIC_ACK=your_secret_acknowledgment_topic
```

## Execute:
### Option - 1: Testing
```bash
python main.py # direct execution
```
### Option - 2: As background process
```bash
nohup python t20_monitor.py 2>&1 &  # As a background process
```
```bash
nohup python t20_monitor.py > log.txt 2>&1 &  # As a background process and log storage as well
```
### Option - 3: Always-On System Service
#### Create a Background service file in this path: 

```bash
sudo nano /etc/systemd/system/t20-monitor.service
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

#### Run below sequentially:
```bash
sudo systemctl daemon-reload  # Reload the systemd manager to read your new file
sudo systemctl enable t20-monitor.service  # Enable it to start automatically on every boot
sudo systemctl start t20-monitor.service  # Start it right now without having to reboot
```

## Moniter the logs: 
```bash
user@machine:~/project/ticket$ journalctl -u t20-monitor.service -f
```

## Termination
### Kill the background process:
```bash
ps aux | grep main.py 
kill -9 <PID>
```
### Kill the Service:
```bash
sudo systemctl stop t20-monitor.service  # Stop the service
sudo systemctl disable t20-monitor.service  # Disable automatic start on boot
```
### To see PID:
```bash
ps aux | grep main.py 
kill -9 <PID>
```