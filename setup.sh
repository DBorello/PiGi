## Berry Lan
# Burn BerryLan Image from https://github.com/nymea/berrylan
# Used bullseye-2023-08-18

# Find using BerryLan iOS App.  Join WiFi network
# SSH to IP Shown.  Username: nymea Password: nymea
# Run this command 
#  curl -s https://raw.githubusercontent.com/DBorello/PiGi/main/setup.sh | bash


# Install dependencies
sudo apt -y install git python3-pil python3-boto3

# Install PiGi
git clone https://github.com/DBorello/PiGi.git

# Enable SPI
echo "dtparam=spi=on" |sudo tee -a /boot/config.txt

# Configure nymea Berrylane
sudo sed -i 's/Mode=offline/Mode=always/g' /etc/nymea/nymea-networkmanager.conf
sudo sed -i 's/AdvertiseName=BT WLAN setup/AdvertiseName=PiGi/g' /etc/nymea/nymea-networkmanager.conf

# Setup service
sudo cp /home/nymea/PiGi/PiGi.service  /etc/systemd/system/PiGi.service
sudo chmod 644 /etc/systemd/system/PiGi.service
sudo systemctl enable PiGi.service

# Set SD Card read-only
sudo raspi-config nonint do_overlayfs 0
sudo sed -i /etc/fstab -e "s/\(.*\/boot.*\)defaults\(.*\)/\1defaults,ro\2/"

# Reboot
sudo reboot
