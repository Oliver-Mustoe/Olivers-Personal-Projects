#!/bin/bash
# Version 1.0
# Description: Creates a simple Apache web server on a CentOS & Ubuntu server systems (currently only tested on Ubuntu)

# Ask whether to disable root SSH
read -p "Would you like to disable root SSH? y/N: " prootssh

# Make answer uppercase
rootssh=${prootssh^^}

# If user answers "Y" or "YES" -
if [[ $rootssh == "Y" ]] || [[ $rootssh == "YES" ]]
then
    #- use sed to replace a certain string, after first /, with another string to not allow root login, after second /y (".*" regex for any amount of characters after made string)
    sudo sed -i 's/#PermitRootLogin .*/PermitRootLogin no/' /etc/ssh/sshd_config
    # After this process, restart sshd service
    sudo systemctl restart sshd
fi

# Test if the result of the command "$(which yum)" as a string is non-zero, -n, if so do yum installation
if [[ -n "$(which yum)" ]]
then
    # Install and start webserver; setup firewall with port 80 open; and make an example "index.html" file as sudo
    sudo su -c "yum install httpd -y && \
    systemctl start httpd && \
    firewall-cmd --permanent --add-port=80/tcp && \
    firewall-cmd --reload && \
    echo '<html>
    <head>
    <style>
    h1 {text-align: center;}
    p {text-align: center;}
    </style>
    </head>
    <h1>TEST FOR WEBSITE</h1>
    <p>If you are seeing this the webserver works!!!</p>
    </html>

    ' > /var/www/html/index.html"

# Test if the result of the command "$(which apt)" as a string is non-zero, -n, if so do yum installation
elif [[ -n "$(which apt)" ]]
then
    # Install and start webserver; setup firewall with port 80 open; and make an example "index.html" file as sudo
    sudo su -c "apt update && \
    apt install apache2 -y&& \
    ufw enable && ufw allow 'Apache' && \
    echo '<html>
    <head>
    <style>
    h1 {text-align: center;}
    p {text-align: center;}
    </style>
    </head>
    <h1>TEST FOR WEBSITE</h1>
    <p>If you are seeing this the webserver works!!!</p>
    </html>

    ' > /var/www/html/index.html"

else
echo "ERROR: not running a supported package manager/OS"
fi

# Find full IPv4 & IPV6, then cut using the delimiter space, only save the first field (which will be just IPv4)
hostip=$(hostname -I | cut -d " " -f 1)

echo "



Website should now be accessible @ 'http://${hostip}'
"
