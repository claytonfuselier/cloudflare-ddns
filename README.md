# ☁️ cloudflare-ddns

A simple Dockerized dynamic DNS updater for Cloudflare with built-in logging, config file, and notifications via email, Discord, or Pushover.

## ⚙️ Configuration

Place a `config.yml` file in a local `./config` folder. Sample:

```yaml
update_interval_seconds: 300

cloudflare:
  api_token: "your_token"
  zone_id: "your_zone_id"
  record_id: "your_record_id"
  record_name: "home.example.com"

notifications:
  email:
    enabled: true
    smtp_server: "smtp.example.com"
    smtp_port: 587
    username: "you@example.com"
    password: "your_password"
    to: "recipient@example.com"

  discord:
    enabled: true
    webhook_url: "https://discord.com/api/webhooks/..."

  pushover:
    enabled: true
    token: "your_app_token"
    user: "your_user_key"
```

## 🐳 Running the container

```bash
docker run   -v $(pwd)/logs:/logs   -v $(pwd)/config:/config:ro   ghcr.io/yourusername/cloudflare-ddns:latest
```

### Or via Docker Compose

```yaml
version: "3.8"
services:
  ddns:
    image: ghcr.io/yourusername/cloudflare-ddns:latest
    volumes:
      - ./logs:/logs
      - ./config:/config:ro
    restart: always
```

## 🔔 Notifications

Send alerts when IP changes using:

- 📧 SMTP Email
- 💬 Discord webhook
- 📱 Pushover app

## 📝 License

This project is licensed under the [MIT License](LICENSE).

_The author reserves the right to relicense future versions under a stronger copyleft license (e.g., GPLv3) to protect long-term software freedom._