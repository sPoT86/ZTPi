# ZTPi
ZTPi is a Zero Touch Provisioning System devieloped for Cisco IOS and IOS-XE devices.
Cisco's Autoinstall feature is used to provide every device with a initial, template-based configuration, to enable SSH access and identify the device by serial number.

Current Version: 2.1  
Features:  
  - Python based jinja2 configuration templating  
  - Status notification in Discord or WebEx (Webhook required)  
  - DHCP Server (isc-dhcp)  
  - TFTP Server (fbtftp)  
  - Syslog collector (rsyslog)  
  - Samba server for SCP download/upload of large files (e.g. Firmware)  
  

Installation:  
1. Disable Firewall:  
sudo ufw disable  
  
2. Get packages:  
sudo apt-get update && sudo apt-get dist-upgrade  
sudo apt-get upgrade  
sudo apt install -y python-minimal  
sudo apt-get install -y --force-yes libssl-dev libffi-dev python-dev python-cffi  
sudo apt-get install software-properties-common  
sudo apt-get install isc-dhcp-server  
sudo apt-get install samba samba-common-bin  
sudo apt-get install redis-server  
sudo apt-get install redis  
sudo apt install python-pip  
sudo apt install python3-pip  
sudo pip install --upgrade pip  
sudo pip install -U setuptools  
sudo pip install fbtftp  
sudo pip install jinja2  
sudo pip install requests  
sudo pip install rq  
sudo pip install napalm  
sudo pip install ruamel.yaml  
sudo pip install discord-webhook  
sudo pip install rsyslog  
sudo pip install loguru  
  
