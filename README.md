# ZTPi
ZTPi is a Zero Touch Provisioning System developed for Cisco IOS devices.
Cisco's Autoinstall feature is used to provide a device with an initial, template-based configuration in two steps. The first template is used to enable SSH to make the device accessible and assign a unique host name. After the device is connecting and identified by serial number, it is provided with a unique template-based configuration.

Current Version: 2.2  
## Features:  
  - Python based jinja2 configuration templating  
  - Status notification in Discord or WebEx (Webhook required)  
  - DHCP Server (isc-dhcp)  
  - TFTP Server (fbtftp)  
  - Syslog collector (rsyslog)  
  - Samba server for SCP download/upload of large files (e.g. Firmware)  
  
## Changelog:  
#### v2.2:    
 - Python2 is no longer be supported  
 - Changed dispatcher.py and tasks.py to use cachefile  
 - Changed tasks.py and notifications.py to use f-Strings  
 - Standardized input for rendering module in templating.py  
 - Removed 2nd rendering module  
 - Changed Discord-Webhook module to requests  
 - Failure Handling for IM implemented  

### v2.1:    
 - Changed "association" to "template"
 - Changed "keystore" to "datastore"    
 - Removed notification if config-backup not existing    
    
    
## Installation:  
### 1. Disable Firewall:  
sudo ufw disable  
  
### 2. Get packages:  
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
  
### 3. Get python modules:  
sudo pip install --upgrade pip  
sudo pip install -U setuptools  
sudo pip install fbtftp  
sudo pip install jinja2  
sudo pip install requests  
sudo pip install rq  
sudo pip install napalm  
sudo pip install ruamel.yaml    
sudo pip install rsyslog  
  
### 4. tbd:    
  
  
### 5. tbd:    
  
    
### 6. tbd:    
 
 
 
Requirements Datastore:  
- First line is reserved for keys
- Must not include keys/kwargs used by Jinja
- Key: devicename  
- Key: ztp_template  
- Key: idarray_1 (at least number one)  
  
  
Requirements Jinja-Templates:  
- Must not include semicolons ( ; )  
