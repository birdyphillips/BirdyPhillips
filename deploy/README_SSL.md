BirdyPhillips — nginx + Gunicorn + Let's Encrypt (Certbot)

This README walks you through deploying `birdyphillips` behind nginx and enabling HTTPS with Let's Encrypt.

Prerequisites
- A public domain name (example: your-domain.example) pointing to your Raspberry Pi's public IP (A record).
- Ports 80 and 443 forwarded from your router to the Pi.
- You ran: `sudo apt update && sudo apt install nginx certbot python3-certbot-nginx -y` (if not yet, run it).

Steps
1) Create a Python virtualenv and install gunicorn

```bash
cd /home/pi/projects/birdyphillips
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install gunicorn flask
# install any other requirements from requirements.txt if present
[ -f requirements.txt ] && pip install -r requirements.txt || true
```

2) Create the systemd unit (copy the provided unit file)

```bash
# As root (or sudo)
sudo cp deploy/birdyphillips.service /etc/systemd/system/birdyphillips.service
sudo systemctl daemon-reload
sudo systemctl enable --now birdyphillips.service
sudo systemctl status birdyphillips.service
```

If gunicorn started successfully you should see it listening on 127.0.0.1:8000:

```bash
ss -tlnp | grep 8000
```

3) Install the nginx site

```bash
# copy nginx sample and edit server_name in the file
sudo cp deploy/nginx_birdyphillips.conf /etc/nginx/sites-available/birdyphillips
sudo nano /etc/nginx/sites-available/birdyphillips    # edit server_name to your domain and save
sudo ln -s /etc/nginx/sites-available/birdyphillips /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

4) Obtain a Let's Encrypt certificate (Certbot nginx plugin)

Replace `your-domain.example` with your actual domain. Certbot will update nginx config to add TLS.

```bash
sudo certbot --nginx -d your-domain.example -d www.your-domain.example
```

Follow the interactive prompts (email, agree to TOS, choose redirect or not). Certbot will also enable automatic renewal.

Test renewal (dry-run):

```bash
sudo certbot renew --dry-run
```

5) Post-install notes
- If you used âredirectâ option, nginx will redirect HTTP->HTTPS automatically.
- Certbot will reload nginx after renewing; if you need to also reload the app service on renew, add a deploy hook or a small script under `/etc/letsencrypt/renewal-hooks/deploy/` that runs `systemctl reload birdyphillips.service`.

Example deploy hook (make executable):

```bash
sudo tee /etc/letsencrypt/renewal-hooks/deploy/reload-birdy.sh > /dev/null <<'EOF'
#!/bin/sh
systemctl reload nginx
systemctl reload birdyphillips.service || true
EOF
sudo chmod +x /etc/letsencrypt/renewal-hooks/deploy/reload-birdy.sh
```

Troubleshooting
- DNS not pointing: use `dig your-domain.example` or `ping` to check.
- Ports blocked: verify router port forwarding and `sudo ss -tlnp | grep -E ":80|:443"`.
- Certbot fails because port 80 is used: stop nginx or the service using port 80 temporarily, or use `--webroot`.

Security note
- Your `app.py` currently runs Flask's built-in server when invoked directly. For production, do NOT run the built-in dev server. Use Gunicorn (this README uses it) and nginx as reverse proxy.
- Consider moving secrets (app.secret_key and admin password) to environment variables or a secure config file.

If you'd like, I can:
- Copy the systemd unit and nginx config into place and run the certbot command for you (I will need your domain and confirmation to run `sudo` commands).
- Or walk you through each command interactively.
