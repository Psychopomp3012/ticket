import os
import time
import datetime
import logging
import threading
from typing import Optional

from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

# CONFIG
URL = "https://in.bookmyshow.com/sports/icc-men-s-t20-world-cup-2026-semi-final-1-kolkata/ET00483392"
CHECK_INTERVAL_MINUTES = 1

# Keep keywords lowercase for reliable matching
AVAILABLE_KEYWORDS = [k.lower() for k in [
    "book tickets", "book now", "buy tickets", "proceed", "select seats",
    "tickets available", "buy now", "proceed to book", "add to cart",
    "Book Now", "₹", "onwards"
]]
COMING_SOON_KEYWORDS = [k.lower() for k in ["coming soon", "comingsoon", "tickets soon", "more tickets soon"]]

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

# Flask app for health check (e.g. Render)
app = Flask(__name__)

@app.route("/")
def health():
    return "OK - Ticket monitor running"

def create_driver() -> webdriver.Chrome:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--window-size=1920,1080")
    options.add_argument(
        "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    )
    # Create driver once (webdriver-manager will cache binary)
    svc = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=svc, options=options)
    driver.set_page_load_timeout(30)
    return driver

def check_tickets_once(driver: webdriver.Chrome) -> bool:
    """Return True if tickets appear available."""
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    logging.info(f"[{now}] Checking ticket status...")

    try:
        driver.get(URL)
        # Wait for DOM ready (or fallback to wait for body)
        try:
            WebDriverWait(driver, 15).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
        except TimeoutException:
            # fallback: wait for presence of body (some SPA may not set readyState quickly)
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

        soup = BeautifulSoup(driver.page_source, "html.parser")
        page_text = soup.get_text(separator=" ", strip=True).lower()

        logging.debug("Page text snippet: %s", page_text[:800])
        status_found = "unknown"

        if any(kw in page_text for kw in COMING_SOON_KEYWORDS):
            status_found = "Coming Soon"
        elif any(kw in page_text for kw in AVAILABLE_KEYWORDS):
            status_found = "TICKETS AVAILABLE!"
        elif "sold out" in page_text or "unavailable" in page_text:
            status_found = "Sold Out"
        elif "₹" in page_text and "onwards" in page_text:
            status_found = "TICKETS LIKELY AVAILABLE!"

        logging.info(f"Status: {status_found}")

        if "AVAILABLE" in status_found.upper():
            alert_msg = f"ALERT! Tickets appear available!\nURL: {URL}\nStatus: {status_found}"
            logging.warning(alert_msg)
            # TODO: call notify(alert_msg) -> email / telegram / webhook
            return True

        return False

    except WebDriverException as e:
        logging.error("WebDriver error: %s", e)
        raise

def monitor_loop():
    driver: Optional[webdriver.Chrome] = None
    while True:
        try:
            if driver is None:
                logging.info("Starting Chrome driver...")
                driver = create_driver()

            found = check_tickets_once(driver)
            if found:
                # If found, you may choose to stop monitoring, or continue.
                logging.info("Alert triggered — consider stopping or increasing interval.")
                # example: break
                # break
        except Exception as e:
            logging.exception("Exception in monitor loop: %s", e)
            # try to recreate the driver on error
            if driver:
                try:
                    driver.quit()
                except Exception:
                    pass
                driver = None
            # back off a bit before retrying
            time.sleep(60)
        finally:
            time.sleep(CHECK_INTERVAL_MINUTES * 60)

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    # Start Flask (health) and monitor in background threads (Flask runs in main thread here by default)
    monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
    monitor_thread.start()

    # Run Flask in main thread (Render expects a web process)
    run_flask()