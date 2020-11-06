
https://thepi.io/how-to-use-your-raspberry-pi-as-a-wireless-access-point/

```bash

sudo apt-get update
sudo apt-get upgrade

reboot

# create a wireless hotspot 
sudo apt-get install hostapd
# dnsmasq is an easy-to-use DHCP and DNS server
sudo apt-get install dnsmasq


sudo systemctl stop hostapd
sudo systemctl stop dnsmasq

# Configure a static IP for the wlan0 interface

sudo nano /etc/dhcpcd.conf


# Now that you’re in the file, add the following lines at the end:

interface wlan0
static ip_address=192.168.0.10/24
denyinterfaces eth0
denyinterfaces wlan0


# Configure the DHCP server (dnsmasq)

sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf

# Type these lines into your new configuration file:
interface=wlan0
  dhcp-range=192.168.0.11,192.168.0.30,255.255.255.0,24h


# Configure the access point host software (hostapd)

sudo nano /etc/hostapd/hostapd.conf

# This should create a brand new file. Type in this:

interface=wlan0
bridge=br0
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
ssid=NETWORK
wpa_passphrase=PASSWORD


# We still have to show the system the location of the configuration file:

sudo nano /etc/default/hostapd

# In this file, track down the line that says #DAEMON_CONF=”” – delete that # and put the path to our config file in the quotes, so that it looks like this:

DAEMON_CONF="/etc/hostapd/hostapd.conf"

# Set up traffic forwarding
sudo nano /etc/sysctl.conf

# Now find this line:
#net.ipv4.ip_forward=1

# …and delete the “#” – leaving the rest, so it just reads:
net.ipv4.ip_forward=1


# Add a new iptables rule
# Next, we’re going to add IP masquerading for outbound traffic on eth0 using iptables:
sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# …and save the new iptables rule:
sudo sh -c "iptables-save > /etc/iptables.ipv4.nat"

# To load the rule on boot, we need to edit the file /etc/rc.local and add the following
line just above the line exit 0:

iptables-restore < /etc/iptables.ipv4.nat


# Enable internet connection

# Now the Raspberry Pi is acting as an access point to which other devices can connect. However, those devices can’t use the Pi to access the internet just yet. To make the possible, we need to build a bridge that will pass all traffic between the wlan0 and eth0 interfaces.

# To build the bridge, let’s install one more package:

sudo apt-get install bridge-utils

# We’re ready to add a new bridge (called br0):

sudo brctl addbr br0

# Next, we’ll connect the eth0 interface to our bridge:

sudo brctl addif br0 eth0

# Finally, let’s edit the interfaces file:

sudo nano /etc/network/interfaces

# …and add the following lines at the end of the file:

auto br0
iface br0 inet manual
bridge_ports eth0 wlan0



sudo reboot


```
