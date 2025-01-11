#!/bin/bash -xeu

sudo yum update -y
sudo yum install python3-pip -y
sudo yum install git -y
sudo yum install awscli -y

git clone https://github.com/rauulrivero/GraphWord.git
cd GraphWord

cd streamlit
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

