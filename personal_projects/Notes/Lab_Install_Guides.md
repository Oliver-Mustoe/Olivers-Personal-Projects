Below are the install guides I used in setting up various environments in VMWare lab testing during my personal projects, including a base image and a lab (linked clone) used for actual testing

### Network settings:
![image](https://user-images.githubusercontent.com/71083461/210112269-a327bd4c-6e95-416e-8899-4fcc3a415792.png)

Vyos
====

NOTE: "delete" can be used instead of "set" to essentially do the opposite!!!

### Device Settings:
![image](https://user-images.githubusercontent.com/71083461/210112118-8367c99e-da64-4059-9c38-118c0d437c7e.png)

Vyos-base install:
------------------

<https://docs.vyos.io/en/equuleus/installation/virtual/gns3.html#vm-setup>

Logged in with "vyos" "vyos"

Booted up image, ran "install image", then ran through the install with default options, used password in list below

After install, powered off and then removed the cd with the install medium

Ran the following

```
configure
show interfaces
delete interfaces ethernet eth0 hw-id
delete interfaces ethernet eth1 hw-id
commit
save
```

Then powered off, made a snapshot, and created a linked clone.

Vyos Lab setup:
---------------

On the linked clone ran the following to setup basic networking:

```
configure
set interfaces ethernet eth0 address '192.168.153.10/24'
set interfaces ethernet eth0 description 'NAT'
set interfaces ethernet eth1 address '172.16.0.1/24'
set interfaces ethernet eth1 description 'VMNET2-RANGE'
set protocols static route 0.0.0.0/0 next-hop 192.168.153.2
set service ssh listen-address '172.16.0.1'
set system name-server '192.168.153.2'
commit
save
```

Pinged google and it works!

<https://docs.vyos.io/en/equuleus/quick-start.html>

Should be able to SSH from a controller with a static IP in the 172.16.0.0/24 range

DNS setup:

```
configure
set service dns forwarding system
set service dns forwarding listen-address '172.16.0.1'
set service dns forwarding allow-from 172.16.0.0/24
commit
```

NAT setup

```
configure
set nat source rule 100 outbound-interface 'eth0'
set nat source rule 100 source address '172.16.0.0/24'
set nat source rule 100 translation address masquerade
commit
```

DHCP setup:

```
configure
set service dhcp-server global-parameters 'local-address 172.16.0.1;'
set service dhcp-server shared-network-name DHCPPOOL authoritative
set service dhcp-server shared-network-name DHCPPOOL subnet 172.16.0.0/24 default-router '172.16.0.1'
set service dhcp-server shared-network-name DHCPPOOL subnet 172.16.0.0/24 domain-name 'range.local'
set service dhcp-server shared-network-name DHCPPOOL subnet 172.16.0.0/24 lease '86400'
set service dhcp-server shared-network-name DHCPPOOL subnet 172.16.0.0/24 name-server 172.16.0.1
set service dhcp-server shared-network-name DHCPPOOL subnet 172.16.0.0/24 range LPOOL start '172.16.0.50'
set service dhcp-server shared-network-name DHCPPOOL subnet 172.16.0.0/24 range LPOOL stop '172.16.0.100'
commit
```

Linux Mint
==========
### Device Settings:
![image](https://user-images.githubusercontent.com/71083461/210112159-6fb63af8-e812-46c5-89b2-9967507bb10a.png)

Mint-base install:
------------------

Used base install defaults, created the om user from the logins below

Once logged in, installed vmware tools

![](https://lh5.googleusercontent.com/Ok9KIvYgp8Cln9sBiS1avfjCSSvGlHuSnnr4Z29rNE3Cov9GocVxYg8xv2QGpS460dA9Wt_UO0naxCAKuz7CRw3l7np5-cGFwzcj0WOd8c46ORflSr5lZl3sVTlTYPulbEA4VVWy6OuM-gePwzSbjIRpsbtJsWoY3JCg7vKPVHCqXwuS3ECATy296a9c0A)

* Did enable copy and paste

Then I logged in and out

Afterwards I deleted the set up connection with the following command:

```
nmcli connection delete Wired\ connection\ 1
```

Then powered off, made a snapshot, and created a linked clone.

Mint-Lab install:
-----------------

On the linked clone, used the following commands to ensure a different uuid and hwaddr from base

```
nmcli con show # Shows connection name for later as well
nmcli device show ens33
 ```

Using the following command, set a temporary static IP for setting up vyos-lab:

```
nmcli con mod Wired\ connection\ 1 ipv4.addresses 172.16.0.49/24
nmcli con mod Wired\ connection\ 1 ipv4.gateway 172.16.0.1
nmcli con mod Wired\ connection\ 1 ipv4.method manual
nmcli con up Wired\ connection\ 1
ip a
 ```

With this setup, the following should be possibly:

![](https://lh3.googleusercontent.com/kFdrQmVAQxSrv4gL5lEaytVREenn0NSAA7HigJZ3HOYln3J7sCK5d6zjCUCYagXfpAvUetwoSpLoBCWJcHMrFZjvVJ4zczzWNObUesht6n5nEj9xXscPTQbUu5IFCSYycwbMdMpIaiD2Kc4o7hTJMAEKvFQXLMSmaqGbxeRnv-1yAUvoiyQeXIn1W29fiw)

Would then use the above prompt to configure vyos :)

I then used the following to enable DHCP on the host:

```
nmcli con mod Wired\ connection\ 1 ipv4.method auto
nmcli con up Wired\ connection\ 1
sudo dhclient
 ```

Rocky
=====
### Device Settings:
![image](https://user-images.githubusercontent.com/71083461/210112313-81c12ace-5cc3-4db2-b940-fbeb8d7366a8.png)

Rocky-base install:
-------------------

<https://docs.rockylinux.org/guides/network/basic_network_configuration/>

NOTE: This install infers that a firewall/router is setup and DHCP is supplied on the network, if this is not the case then either VMware tools can be skipped or a static IP can be setup to establish connection needed to install tar.

Went along the base config, see below for passwords

Once logged in, ran the following commands:

```
# Create "om" user
adduser om
passwd om # See password below!
usermod -aG wheel om
 ```

Then used the following command to install tar:

```
yum install tar
 ```

Installed VMware tools:

```
yum install open-vm-tools
 ```

Then I used the following delete the network connection:

```
nmcli connection delete Wired\ connection\ 1
 ```

Then powered off, made a snapshot, and created a linked clone. (No more work required on the clone, so setup skipped)

Windows server
==============
### Device Settings:
![image](https://user-images.githubusercontent.com/71083461/210112367-b1851997-252b-40ae-8de4-bdd441235121.png)

Windows server 2019 base install:
---------------------------------

Follow along with basic prompts, set password below for Administrator, shutdown and link cloned and all is good (different uuid and mac address check with powershell commands below)

```
(Get-WmiObject -Class Win32_ComputerSystemProduct).UUID
Get-NetAdapter
 ```