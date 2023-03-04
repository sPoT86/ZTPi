# ZTPi
ZTPi is a Zero Touch Provisioning System devieloped for Cisco IOS and IOS-XE devices.
Cisco's Autoinstall feature is utilized to provide a device in two steps with a initial, template-based configuration. The first template will enable SSH to make the device accessible and assign a unique hostname. After connecting and identifying the device by serial number, it is provided with a unique template-based configuration.

Current Version: 2.1  
Features:  
  - Python based jinja2 configuration templating  
  - Status notification in Discord or WebEx (Webhook required)  
  - DHCP Server (isc-dhcp)  
  - TFTP Server (fbtftp)  
  - Syslog collector (rsyslog)  
  - Samba server for SCP download/upload of large files (e.g. Firmware)  
  
Changelog:  
v2.2:    
 - Changed dispatcher.py and tasks.py to use cachefile for ZTP-confg
 - Standardized templating.py jinja rendering call  
v2.1:    
 - Changed "association" to "template"
 - Changed "keystore" to "datastore"    
 - Removed notification if config-backup not existing    
    
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
  
  
Requirements Datastore:  
- First line is reserved for keys
- Key: devicename  
- Key: ztp_template  
- Key: idarray_1 (at least one)  
  
  
Requirements Jinja-Templates:  
- Must not include semicolons ( ; )  
