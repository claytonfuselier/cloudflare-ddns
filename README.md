# ☁️ Cloudflare DDNS

A no-nonsense, config-driven Dynamic DNS updater for Cloudflare.
Runs in a Docker container, logs to file, and pings you when your IP changes — via email, Discord, or Pushover. Set it and forget it.

## 🧠 Why?

Because your ISP thinks giving you a static IP is *too much to ask*.
This app makes sure your domain always points to your home network — without relying on a third-party DDNS service you can’t control.

No shady middlemen. No weird UIs. No "freemium" traps.
Just you, your IP, and Cloudflare's API.

<br>

## ⚙️ Configuration

This app is powered by a single YAML file.

📁 Create a `config.yml` in a local `./config` folder.
📌 Here’s a full example:

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

<br>

## 🐳 Deploying

### Docker CLI

```bash
docker run \
  -v $(pwd)/logs:/logs \
  -v $(pwd)/config:/config:ro \
  ghcr.io/claytonfuselier/cloudflare-ddns:latest
```

### Docker Compose

```yaml
services:
  cloudflare-ddns:
    image: ghcr.io/claytonfuselier/cloudflare-ddns:latest
    volumes:
      - ./logs:/logs
      - ./config:/config:ro
    restart: always
```

Logs are written to both stdout and `./logs/ddns.log` (rotated).

<br>

## 🔔 Notifications

Get notified when your public IP changes via:

* 📧 Email (SMTP)
* 💬 Discord Webhook
* 📱 Pushover

You can enable/disable any combination via the config file.
Each method works independently — no dependencies between them.

<br>

## 🔐 About Credentials

This app requires a [Cloudflare API Token](https://developers.cloudflare.com/api/tokens/create/) with permissions to:

* Read zone details
* Edit DNS records

Your credentials live **only on your Docker host** inside `config.yml`.
They are **not** baked into the image or stored in the repo.

<br>

## ☁️ Cloudflare Disclaimer

This project uses the official Cloudflare v4 REST API, but is **not affiliated with Cloudflare** in any way.
You're just talking directly to the API, like the sovereign DNS warrior you are.

<br>

## 👤 Author

Created with spite for dynamic IPs and a love for self-hosting by [claytonfuselier](https://github.com/claytonfuselier)

<br>

## 📜 License

This project is licensed under the [MIT License](LICENSE).

*The author reserves the right to relicense future versions under a stronger copyleft license (e.g., GPLv3) to protect long-term software freedom.*

<br>

## 🤘 Support

Found this useful? Toss a star on the repo. Or don't. I'm not your DNS boss.
