#!/bin/sh
sudo cp oscgpio.service /etc/systemd/system/oscgpio.service
sudo systemctl enable oscgpio.service
