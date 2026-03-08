#!/bin/bash

echo "Installing Battery History Monitor..."

# Make the Python script executable
chmod +x ,/battery_history.py

# Copy systemd service file
sudo cp ./battery-monitor.service /etc/systemd/system/

# Reload systemd and enable the service
sudo systemctl daemon-reload
sudo systemctl enable battery-monitor.service

echo "Installation complete!"
echo ""
echo "Usage:"
echo "  Start monitoring: sudo systemctl start battery-monitor"
echo "  Stop monitoring:  sudo systemctl stop battery-monitor"
echo "  View status:      sudo systemctl status battery-monitor"
echo ""
echo "Manual usage:"
echo "  Current status:   ./battery_history.py --current"
echo "  View history:     ./battery_history.py --history 24"
echo "  View stats:       ./battery_history.py --stats"
echo "  Monitor manually: ./battery_history.py --monitor"
