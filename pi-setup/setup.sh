#!/bin/bash

# Masjid Clock Setup Script
# This script automates the installation and configuration of the Masjid Clock on a Raspberry Pi Zero W.

echo "Starting Masjid Clock installation..."

# Update and upgrade system packages
echo "Updating system..."
sudo apt update && sudo apt full-upgrade -y

# Install necessary dependencies
echo "Installing dependencies..."
sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev \
libreadline-dev libsqlite3-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev libopenblas-dev \
python3-pip python3-venv

# Define paths
PI_NAME="raspberrypisoc"
USER_HOME="/home/$PI_NAME"
PROJECT_DIR="$USER_HOME/MasjidClock"
BOOT_DIR="/boot/firmware/MasjidClock"

# Check if the MasjidClock folder exists in /boot and copy it to home directory
if [ -d "$BOOT_DIR" ]; then
    echo "Copying MasjidClock folder from /boot to $USER_HOME..."
    cp -r "$BOOT_DIR" "$PROJECT_DIR"
else
    echo "Error: MasjidClock folder not found in /boot! Please copy the folder into the boot partition and try again."
    exit 1
fi

# Navigate to project directory
cd "$PROJECT_DIR"

# Set up virtual environment
echo "Creating virtual environment..."
python3 -m venv myenv
wget https://bootstrap.pypa.io/get-pip.py
source myenv/bin/activate
python get-pip.py

# Install Python packages
echo "Installing Python libraries..."
pip install --upgrade pip
sudo chown -R raspberrypisoc /home/raspberrypisoc/MasjidClock/
sudo chown -R raspberrypisoc /home/raspberrypisoc/MasjidClock/myenv/lib/python3.11/
pip install numpy pandas Pillow customtkinter bs4 selenium arabic_reshaper python-bidi

# Deactivate virtual environment
deactivate

# Create the run script
echo "Creating run_clock.sh..."
cat <<EOF > $PROJECT_DIR/run_clock.sh
#!/bin/bash
cd $PROJECT_DIR
source myenv/bin/activate
python GUI-static.py
deactivate
EOF

# Make the script executable
chmod +x $PROJECT_DIR/run_clock.sh

# Create the systemd service file
echo "Creating systemd service..."
cat <<EOF | sudo tee /etc/systemd/system/masjid_clock.service
[Unit]
Description=Run MasjidClock GUI on startup
After=network.target

[Service]
Environment=DISPLAY=:0
ExecStart=/bin/bash $PROJECT_DIR/run_clock.sh
Restart=always
User=raspberrypisoc
WorkingDirectory=$PROJECT_DIR

[Install]
WantedBy=multi-user.target
EOF

# Enable and start the systemd service
echo "Enabling systemd service..."
sudo systemctl enable masjid_clock.service
sudo systemctl start masjid_clock.service

# Configure screen settings (Resolution & Orientation)
echo "Configuring screen settings..."
sudo raspi-config nonint do_resolution 1920 1080
sudo raspi-config nonint do_display_orientation 1  # 1 = 90 degrees (left)

echo "Masjid Clock setup completed!"
echo "Rebooting system..."
sudo reboot
