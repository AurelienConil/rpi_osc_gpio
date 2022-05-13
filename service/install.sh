#!/bin/sh
sudo cp oscpgio.service /etc/systemd/system/oscgpio.service
sudo systemctl enable oscgpio.service
