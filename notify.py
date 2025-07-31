import requests
import smtplib
from email.mime.text import MIMEText

def send_notifications(config, message, logger):
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

    if notif.get("gotify", {}).get("enabled"):
        try:
            gotify = notif["gotify"]
            requests.post(f"{gotify['url']}/message", json={
                "title": "DDNS Update",
                "message": message,
                "priority": 5
            }, headers={"Authorization": f"Bearer {gotify['token']}"})
            logger.info("Gotify notification sent.")
        except Exception as e:
            logger.error(f"Gotify notification failed: {e}")

    if notif.get("ntfy", {}).get("enabled"):
        try:
            ntfy = notif["ntfy"]
            url = f"{ntfy['url'].rstrip('/')}/{ntfy['topic']}"
            auth = (ntfy.get("user"), ntfy.get("password")) if ntfy.get("user") else None
            requests.post(url, data=message.encode('utf-8'), auth=auth)
            logger.info("ntfy.sh notification sent.")
        except Exception as e:
            logger.error(f"ntfy.sh notification failed: {e}")

    if notif.get("slack", {}).get("enabled"):
        try:
            slack = notif["slack"]
            requests.post(slack["webhook_url"], json={"text": message})
            logger.info("Slack notification sent.")
        except Exception as e:
            logger.error(f"Slack notification failed: {e}")

    if notif.get("webhook", {}).get("enabled"):
        try:
            webhook = notif["webhook"]
            headers = webhook.get("headers", {})
            method = webhook.get("method", "POST").upper()
            if method == "POST":
                requests.post(webhook["url"], json={"message": message}, headers=headers)
            else:
                requests.get(webhook["url"], headers=headers)
            logger.info("Custom webhook notification sent.")
        except Exception as e:
            logger.error(f"Custom webhook failed: {e}")

    if notif.get("http_post", {}).get("enabled"):
        try:
            http_post = notif["http_post"]
            body = http_post.get("body", {})
            requests.post(http_post["url"], json=body)
            logger.info("HTTP POST notification sent.")
        except Exception as e:
            logger.error(f"HTTP POST failed: {e}")

    if notif.get("mqtt", {}).get("enabled"):
        try:
            import paho.mqtt.publish as publish
            mqtt = notif["mqtt"]
            publish.single(mqtt["topic"], payload=message, hostname=mqtt["host"],
                           port=mqtt.get("port", 1883),
                           auth={"username": mqtt["username"], "password": mqtt["password"]})
            logger.info("MQTT message published.")
        except Exception as e:
            logger.error(f"MQTT publish failed: {e}")
