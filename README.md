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

#### v2.1:    
 - Changed "association" to "template"
 - Changed "keystore" to "datastore"    
 - Removed notification if config-backup not existing    
    
    
## Installation:  
#### 1. Disable Firewall:  
sudo ufw disable  
  
#### 2. Get packages:  
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
  
#### 3. Get python modules:  
sudo pip install --upgrade pip  
sudo pip install -U setuptools  
sudo pip install fbtftp  
sudo pip install jinja2  
sudo pip install requests  
sudo pip install rq  
sudo pip install napalm  
sudo pip install ruamel.yaml    
sudo pip install rsyslog  
  
#### 4. Create system folders:    
sudo mkdir -m777 /etc/systemd/system/ztp  
sudo mkdir -m777 /var/log/ztp  
sudo mkdir -m777 /home/vadmin/images  
sudo mkdir -m777 /var/log/remotelogs  
  
#### 5. Move files to system folders:    
sudo mv /{YOUR PATH}/ZTP-main/opt/ztp /opt/  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_default_isc-dhcp-server /etc/default/isc-dhcp-server  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_dhcp_dhcp-networks.conf /etc/dhcp/dhcp-networks.conf  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_dhcp_dhcpd.conf /etc/dhcp/dhcpd.conf  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_logrotate.d_ztplogs /etc/logrotate.d/ztplogs  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_systemd_system_ztp_tasks.service /etc/system.d/system/ztp/ztp_tasks.service  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_systemd_system_ztp_tftp.service /etc/system.d/system/ztp/ztp_tftp.service  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_samba_smb.conf /etc/samba/smb.conf  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_rsyslog.conf /etc/rsyslog.conf  
sudo mv /{YOUR PATH}/ZTP-main/ubuntu16_systemfiles/etc_logrotate.d_remotelogs /etc/logrotate.d/remotelogs  
  
#### 6. Fix permissions:    
sudo chmod -R 777 /opt/ztp  
  
#### 7. Mandatory personal service settings:    
TFTP service settings (local user) -> /etc/systemd/system/ztp_tftp.service  
Taskmanager settings (local user) -> /etc/systemd/system/ztp_tasks.service  
DHCP server configuration (listening interface) -> /etc/default/isc-dhcp-server  
DHCP service configuration (global DHCP Pool settings) -> /etc/dhcp/dhcpd.conf  
DHCP network settings (pool settings for relayed networks) -> /etc/dhcp/dhcpd-networks.conf  
  
#### 8. Optional personal settings:    
ZTP global environment settings (staging and logging) -> /opt/ztp/config.yaml  
IM platform configuration (Discord/Webex) -> /opt/ztp/app/notifications.py  
Samba server configuration (protocols and paths) -> /etc/samba/smb.conf  
  
#### 9. Start services and registertration for startup after boot:  
sudo systemctl daemon-reload  
sudo systemctl start smbd  
sudo systemctl enable smbd  
sudo systemctl start rsyslog  
sudo systemctl enable rsyslog  
sudo systemctl start redis  
sudo systemctl enable redis  
sudo systemctl start ztp_tasks  
sudo systemctl enable ztp_tasks  
sudo systemctl start ztp_tftp  
sudo systemctl enable ztp_tftp  
  
#### 10. Verify services status:  
sudo systemctl status ztp_tftp  
sudo systemctl status ztp_tasks  
sudo systemctl status isc-dhcp-server  

## Storage locations:  
Jinja template files -> /opt/ztp/templates  
Fixed configuration files (pass a configuration without jinja templating) -> /opt/ztp/configfiles
Datastore (devices and keys) -> /opt/ztp/datastores  
General logfile (ZTP server and service) -> /var/log/ztp/ZTPi.log  
Remote logfiles (provisioned devices, if used) -> /var/log/ztp/remotelogs/{DEVICE-IP}.log
  
## Requirements: 
### Datastore:  
- First line is reserved for keys
- Must not include default keys/kwargs used by Jinja
- Key "devicename"  
- Key "ztp_template"  
- Key "idarray_1" (at least number one)  
  
### Jinja-Templates:  
- Must not include semicolons ( ; )  
