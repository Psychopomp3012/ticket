## Requirements in .env:
BOT_TOKEN
CHAT_ID

TOPIC_ALERT
TOPIC_ACK

RUN: nohup python t20_monitor.py > log.txt 2>&1 &

Look for PID : ps aux | grep test.py

./components
    /check_ticket.py => check the availability of ticket
    /telegram.py => sends msg to telegram bot
    /laptop_warning.py => laptop siren
    /phone_siren => ntfy

Background service file:
sudo nano /etc/systemd/system/t20-monitor.service

# Reload the systemd manager to read your new file
sudo systemctl daemon-reload

# Enable it to start automatically on every boot
sudo systemctl enable t20-monitor.service

# Start it right now without having to reboot
sudo systemctl start t20-monitor.service

Moniter:
journalctl -u t20-monitor.service -f