#!/bin/bash
cd /home/ec2-user
wget https://raw.githubusercontent.com/aws-samples/amazon-pinpoint-social-sentiment/master/stream-producer/producer.py
wget https://raw.githubusercontent.com/aws-samples/amazon-pinpoint-social-sentiment/master/stream-producer/requirements.txt
wget https://raw.githubusercontent.com/aws-samples/amazon-pinpoint-social-sentiment/master/stream-producer/producer.conf -P /etc/init
chown ec2-user:ec2-user producer.py
pip install -r requirements.txt
echo "" >> /etc/init/producer.conf
echo env CONSUMER_KEY=${ConsumerKey} >> /etc/init/producer.conf
echo env CONSUMER_SECRET=${ConsumerSecret} >> /etc/init/producer.conf
echo env ACCESS_TOKEN=${AccessToken} >> /etc/init/producer.conf
echo env ACCESS_TOKEN_SECRET=${AccessTokenSecret} >> /etc/init/producer.conf
start producer