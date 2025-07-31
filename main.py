import os
import sys
import yaml
import time
import requests
import smtplib
import logging
from logging.handlers import RotatingFileHandler
from email.mime.text import MIMEText

CONFIG_FILE = "/config/config.yml"
LOG_DIR = "/logs"
LOG_FILE = os.path.join(LOG_DIR, "ddns.log")

os.makedirs(LOG_DIR, exist_ok=True)

logger = logging.getLogger("ddns")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")

stream = logging.StreamHandler(sys.stdout)
stream.setFormatter(formatter)
logger.addHandler(stream)

file_handler = RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=3)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

IP_APIS = [
    "https://api.ipify.org",
    "https://checkip.amazonaws.com",
    "https://ifconfig.me/ip"
]

def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return yaml.safe_load(f)
    except Exception as e:
        logger.error(f"Failed to load config: {e}")
        sys.exit(1)

def get_public_ip():
    for url in IP_APIS:
        try:
            ip = requests.get(url, timeout=5).text.strip()
            if ip:
                logger.info(f"Retrieved public IP from {url}: {ip}")
                return ip
        except Exception as e:
            logger.warning(f"Failed to get IP from {url}: {e}")
    logger.error("All IP services failed.")
    sys.exit(1)

def send_notifications(config, message):
    notif = config.get("notifications", {})

    if notif.get("email", {}).get("enabled"):
        try:
            smtp = notif["email"]
            msg = MIMEText(message)
            msg["Subject"] = "DDNS Update Notification"
            msg["From"] = smtp["username"]
            msg["To"] = smtp["to"]

            with smtplib.SMTP(smtp["smtp_server"], smtp["smtp_port"]) as server:
                server.starttls()
                server.login(smtp["username"], smtp["password"])
                server.send_message(msg)
            logger.info("Email notification sent.")
        except Exception as e:
            logger.error(f"Email notification failed: {e}")

    if notif.get("discord", {}).get("enabled"):
        try:
            discord = notif["discord"]
            requests.post(discord["webhook_url"], json={"content": message})
            logger.info("Discord notification sent.")
        except Exception as e:
            logger.error(f"Discord notification failed: {e}")

    if notif.get("pushover", {}).get("enabled"):
        try:
            po = notif["pushover"]
            requests.post("https://api.pushover.net/1/messages.json", data={
                "token": po["token"],
                "user": po["user"],
                "message": message
            })
            logger.info("Pushover notification sent.")
        except Exception as e:
            logger.error(f"Pushover notification failed: {e}")

def update_dns_record(config):
    cf = config["cloudflare"]
    current_ip = get_public_ip()
    headers = {
        "Authorization": f"Bearer {cf['api_token']}",
        "Content-Type": "application/json"
    }

    record_url = f"https://api.cloudflare.com/client/v4/zones/{cf['zone_id']}/dns_records/{cf['record_id']}"
    resp = requests.get(record_url, headers=headers).json()
    if not resp["success"]:
        logger.error(f"Error fetching record: {resp}")
        return

    existing_ip = resp["result"]["content"]
    if current_ip == existing_ip:
        logger.info("IP unchanged.")
        return

    payload = {
        "type": "A",
        "name": cf["record_name"],
        "content": current_ip,
        "ttl": 300,
        "proxied": False
    }

    resp = requests.put(record_url, headers=headers, json=payload).json()
    if resp["success"]:
        msg = f"DNS record updated: {existing_ip} → {current_ip}"
        logger.info(msg)
        send_notifications(config, msg)
    else:
        logger.error(f"Update failed: {resp}")

def main():
    config = load_config()
    interval = config.get("update_interval_seconds", 300)

    while True:
        update_dns_record(config)
        time.sleep(interval)

if __name__ == "__main__":
    main()