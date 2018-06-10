#!/bin/bash
cp taut-server.service /etc/systemd/system/
systemctl enable taut-server.service
systemctl start taut-server.service