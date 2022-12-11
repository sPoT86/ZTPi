# ZTPi
ZTPi is a Zero Touch Provisioning System devieloped for Cisco IOS and IOS-XE devices.
Cisco's Autoinstall feature is used to provide every device with a initial, template-based configuration, to enable SSH access and identify the device by serial number.

Current Version: 2  
Features:  
  - Python based jinja2 configuration templating  
  - Status notification in Discord or WebEx (Webhook required)  
  - DHCP Server (isc-dhcp)  
  - TFTP Server (fbtftp)  
  - Syslog collector (rsyslog)  
  - Samba server for SCP download/upload of large files (e.g. Firmware)  
