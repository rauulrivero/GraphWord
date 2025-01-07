#!/bin/bash -xeu

apt update
apt install -y python3
apt-get install -y python3-pip curl git
git clone https://github.com/rauulrivero/GraphWord.git
cd api
pip3 install flask
python3 app.py