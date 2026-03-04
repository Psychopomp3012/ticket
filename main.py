import time
import random

# User - defined

from components.check_ticket import check_ticket
from components.telegram import send_telegram

count = 1

while True:
    CHECK_INTERVAL = random.randint(30, 60)
    found = check_ticket(count)

    if found:
        print("Stopping script.")
        break

    print(f"Sleeping {CHECK_INTERVAL} seconds...\n")
    
    if count % 10 == 0:
        print(f"{count} Checks Done")
        send_telegram(f"{count} Checks Done")
        
    count += 1
    time.sleep(CHECK_INTERVAL)