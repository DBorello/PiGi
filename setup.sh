# Enable SPI (TODO Fine dietpi-config way)

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
