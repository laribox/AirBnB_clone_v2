#!/usr/bin/env bash
# web server for deploying web_static.

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/releases/test/
mkdir -p /data/web_static/shared/
echo "Welcome to web_static!" > /data/web_static/releases/test/index.html

sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

sudo service nginx restart
