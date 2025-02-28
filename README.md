# Masjid Clock

## Description
Masjid Clock is a Raspberry Pi-based prayer time display system designed for masajid. It provides a clear and dynamic interface for prayer timings using a **CustomTkinter** GUI. The system is intended to run on a **Raspberry Pi Zero W**, displaying prayer times and relevant updates automatically on a connected screen.

However, due to the limitations of the Raspberry Pi Zero W, some performance issues exist. This guide covers installation, setup, usage, and known issues, along with instructions to auto-start the system on boot.

---

## Features
- Displays prayer times dynamically using **CustomTkinter**.
- Auto-starts on boot using a **systemd service**.
- Simple shell script for launching the application.
- Supports screen orientation and resolution configuration.

---

## Known Issues
The current implementation has the following issues:
**Raspberry Pi Zero W limitations**: 
1. **Computational Limitations**: Cannot run GUI-toggle.py, have to stick to GUI-static.py as it's light-weight, and **crashes or freezes** at certain prayer times.
2. **No Real-Time Clock (RTC)**: The system’s time buffers and delays, causing time inconsistencies.
3. **No Arabic Font Support**: Arabic text is not rendered correctly.
4. **Slow RAM/Processing**: Status updates are slow or unresponsive.

---

## Installation & Setup
### 1. Install Raspberry Pi OS & Update Packages
Ensure your Raspberry Pi is running the latest OS:
```bash
sudo apt update
sudo apt full-upgrade -y
```
Install necessary dependencies:
```bash
sudo apt install -y build-essential libssl-dev zlib1g-dev libncurses5-dev libncursesw5-dev \
libreadline-dev libsqlite3-dev libgdbm-dev libc6-dev libbz2-dev libffi-dev
sudo apt-get install libopenblas-dev
```

### 2. Set Up Virtual Environment & Install Python Libraries
Download and install pip:
```bash
wget https://bootstrap.pypa.io/get-pip.py
myenv/bin/python get-pip.py
```

Install the required Python libraries:
```bash
pip install numpy pandas Pillow customtkinter bs4 selenium
```

---

## Running the Program
Create a shell script to start the application:
```bash
nano run_clock.sh
```
Add the following content:
```bash
#!/bin/bash
cd /home/raspberrypisoc/MasjidClock/
source myenv/bin/activate
python GUI-static.py
deactivate
```
Give the script execution permissions:
```bash
chmod +x run_clock.sh
```

---

## Screen Configuration
Ensure the display settings are correct:
- **Resolution**: Set to `1920x1080`.
- **Orientation**: Change to **left** in the Raspberry Pi display settings.

---

## Auto-Start on Boot
Create a systemd service to run the Masjid Clock automatically:
```bash
sudo nano /etc/systemd/system/masjid_clock.service
```
Add the following configuration:
```
[Unit]
Description=Run MasjidClock GUI on startup
After=network.target

[Service]
Environment=DISPLAY=:0
ExecStart=/bin/bash /home/raspberrypisoc/run_clock.sh
Restart=always
User=raspberrypisoc
WorkingDirectory=/home/raspberrypisoc/MasjidClock

[Install]
WantedBy=multi-user.target
```

Enable and start the service:
```bash
sudo systemctl enable masjid_clock.service
sudo systemctl start masjid_clock.service
```

---

## Credits
Developed by **[Your Name]**. Feel free to contribute or suggest improvements.

---

## License
This project is licensed under **MIT License**. See the LICENSE file for details.

---

### Additional Notes
- If the system crashes or freezes frequently, consider **upgrading to a Raspberry Pi 4** for better performance.
- To fix **Arabic font issues**, install proper fonts and ensure right-to-left text rendering support is enabled.
- If experiencing delays, consider implementing an **RTC module** to maintain accurate time.

---

This README provides a complete guide to installing, configuring, and running the Masjid Clock. If you encounter issues, feel free to modify or enhance the script based on your requirements.
