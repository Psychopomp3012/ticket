import time
import random

# User - defined

from components.get_status import get_status
from components.telegram import send_telegram
from components.phone_siren import trigger_phone_siren
from components.phone_siren import is_acknowledged
from components.laptop_warning import trigger_laptop_siren

"""
THOUGHT PROCESS:
1. Loop through each URL
2. For each URL retrieve status of event
"""

TARGETS = [
    {
        "name": "T20 Semi-Final 2",
        "url": "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-2/ET00474271",
        "enabled": True
    },
    {
        "name": "T20 Final",
        "url": "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-final/ET00476187",
        "enabled": True
    },
    # {
    #     "name": "Chess Meetup (Test)",
    #     "url": "https://in.bookmyshow.com/sports/chess-chai-connect/ET00358311",
    #     "enabled": True
    # }
]

count = 1

print("Starting the monitor")

while True:
    CHECK_INTERVAL = random.randint(30, 60)
    
    for event in TARGETS:
        if not event["enabled"]:
            continue
        
        url = event["url"]
        status = get_status(url)

        if status == "available":
            send_telegram(f"🚨 TICKET AVAILABLE! Book NOW!: {count}\nEvent Name: {event['name']}")
            current_run_id = str(int(time.time()))
            while True:
                # 1. Trigger the loud laptop audio
                trigger_laptop_siren()
                    
                # 2. Send the phone alert with the Kill Switch button
                trigger_phone_siren(current_run_id)
                    
                # 3. Wait 30 seconds to give you time to grab your phone
                print("Waiting 30 seconds for acknowledgment...")
                time.sleep(30)
                    
                # 4. Check if you pressed the Stop button on your phone
                if is_acknowledged(current_run_id):
                    print("✅ Alarm acknowledged from phone!")
                    # No point in checking anymore
                    event["enabled"] = False
                    break
                else:
                    print("❌ Not acknowledged yet. Ringing again!")
        elif status == "coming_soon":
            # just keep on checking again and again
            
            pass
        elif status == "sold_out":
            msg = f"All tickets of this event are sold\nEvent name: {event['name']}"
            # log - laptop
            print(msg)
            # log - cell phone
            send_telegram(msg)
            # No point in checking anymore
            event["enabled"] = False
        elif status == "closed":
            msg = f"Event Closed\nEvent name: {event['name']}"
            # log - laptop
            print(msg)
            # log - cell phone
            send_telegram(msg)
            # No point in checking anymore
            event["enabled"] = False
        
        # Some gap before successive requests
        time.sleep(random.randint(3, 7))


    print(f"\nCycle {count} complete. Sleeping {CHECK_INTERVAL} seconds...\n")
    
    if count % 10 == 0:
        active_targets = sum(1 for t in TARGETS if t["enabled"])
        
        if active_targets == 0:
            print("🏁 All targets are either sold out or acknowledged. Shutting down monitor!")
            send_telegram("🏁 All targets cleared. Monitor is offline.")
            break
        
        health_msg = f"Health Report: Cycle {count} Done. {active_targets} targets still active."
        print(health_msg)
        send_telegram(health_msg)
        
    count += 1
    time.sleep(CHECK_INTERVAL)