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
nohup python main.py 2>&1 &  # As a background process
```
```bash
nohup python main.py > log.txt 2>&1 &  # As a background process and log storage as well
```
### Option - 3: Always-On User System Service
#### Create a Background service file in this path: 

```bash
mkdir -p ~/.config/systemd/user
nano ~/.config/systemd/user/t20-monitor.service
```

#### File content: 
```Ini, TOML
[Unit]
Description=T20 World Cup Ticket Monitor
# Wait for the network to be fully connected
After=network-online.target
Wants=network-online.target
# Crucial: Wait for your secondary drive to be mounted
RequiresMountsFor="/path/to/disk"

[Service]
WorkingDirectory=/home/your_username/path/to/your/project   # ← full absolute path
ExecStart=/home/your_username/path/to/your/project/venv/bin/python main.py

Restart=on-failure
RestartSec=10
Environment=PYTHONUNBUFFERED=1

# Usually NOT needed in user services, but can add if still issues
Environment=DISPLAY=:0
Environment=XDG_RUNTIME_DIR=/run/user/1000

[Install]
WantedBy=graphical-session.target
# or default.target — but graphical-session.target is safer for GUI things

```

#### Run below sequentially:
```bash
systemctl --user daemon-reload  # Reload the systemd manager to read your new file
systemctl --user enable t20-monitor.service  # Enable it to start automatically on every boot
systemctl --user start t20-monitor.service  # Start it right now without having to reboot
```

### Monitor the logs: 
```bash
journalctl --user -u t20-monitor.service -f
systemctl --user status t20-monitor.service
```

## Termination
#### Kill the Service:
```bash
systemctl --user stop t20-monitor.service  # Stop the service
systemctl --user disable t20-monitor.service  # Disable automatic start on boot
```
#### Kill the background process | To see PID:
```bash
ps aux | grep main.py 
kill -9 <PID>
```

## Restart(if changes made)
```bash
systemctl --user daemon-reload
systemctl --user restart t20-monitor.service
```

## Clear the previous logs
```bash
journalctl --user --rotate
journalctl --user --vacuum-time=1s
```
