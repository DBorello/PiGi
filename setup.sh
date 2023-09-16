## This is DietPi
# Enable SPI & bluetooth (TODO Fine dietpi-config way)

# Install BerryLan
echo "deb http://repository.nymea.io bullseye rpi" | tee /etc/apt/sources.list.d/nymea.list
apt-key adv --keyserver keyserver.ubuntu.com --recv-key A1A19ED6
apt update
apt -y install bluez nymea-networkmanager dirmngr 

# Install python dependencies
apt -y install gcc-arm-linux-gnueabihf python3-pil
pip install spidev boto3

# Clone repository
git clone https://github.com/DBorello/PiGi.git

## Berry Lan
# Burn BerryLan Image from https://github.com/nymea/berrylan
# Used bullseye-2023-08-18

# Find using BerryLan iOS App.  Join WiFi network
# SSH to IP Shown.  Username: nymea Password: nymea

# Install dependencies
sudo apt -y install git python3-pil python3-boto3

# Install python depencencies
pip install boto3

# Enable SPI
echo "dtparam=spi=on" |sudo tee -a /boot/config.txt

# Configure nymea Berrylane
sudo sed -i 's/Mode=offline/Mode=always/g' /etc/nymea/nymea-networkmanager.conf
sudo sed -i 's/AdvertiseName=BT WLAN setup/AdvertiseName=PiGi/g' /etc/nymea/nymea-networkmanager.conf
