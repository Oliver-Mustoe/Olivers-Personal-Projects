#!/bin/bash

# Description: Bash script to generate all of the needed reqs to setup the Powershell script (Powershell install, optional user)

main () {
# Main install
    # Powershell install
    echo "[Starting Powershell Installation...]"

    # If the "pwsh" executable doesnt exist then use the designated function
    if [[ -z "$(which pwsh)"]]
    then
        InstallReqs
    fi

    # User creation (function)
    echo "[Starting user creation...]"
    UserCreation

    # Create a temporary safe directory for working with PasswordLessSSH.ps1
    temp_dir="$(mktemp -d)"

    # Copy needed files to the temporary directory
    sudo cp PasswordLessSSH.ps1 $temp_dir

    # Create an RSA key & Execute the designated .ps1 file
    sudo su - $chosen_user -c 'ssh-keygen -t rsa && sudo pwsh $temp_dir/PasswordLessSSH.ps1'
    wait

    # Cleanup
    rm -rf temp_dir
    }

    InstallReqs () {
    # Install powershell on host system

    # Use which to see which package manager executable is installed (which would indicate Debian or Red Hat)
    if [[ -n "$(which apt)" ]]
    then

        echo "[Installing Powershell for: Debian]"
        # From https://learn.microsoft.com/en-us/powershell/scripting/install/install-debian?source=recommendations&view=powershell-7.3:
        # Install system components
        sudo apt update  && sudo apt install -y curl gnupg apt-transport-https

        # Import the public repository GPG keys
        curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -

        # Register the Microsoft Product feed
        sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-debian-bullseye-prod bullseye main" > /etc/apt/sources.list.d/microsoft.list'

        # Install PowerShell
        sudo apt update && sudo apt install -y powershell


    elif [[ -n "$(which yum)" ]]
    then

        echo "[Installing Powershell for: RHEL]"
        # From https://learn.microsoft.com/en-us/powershell/scripting/install/install-rhel?source=recommendations&view=powershell-7.3:
        # Register the Microsoft RedHat repository
        curl https://packages.microsoft.com/config/rhel/7/prod.repo | sudo tee /etc/yum.repos.d/microsoft.repo

        # Install PowerShell
        sudo yum install --assumeyes powershell


    else
      echo "ERROR: not running a supported package manager/OS"
    fi

    echo "[Done]"
}


UserCreation () {
    # Optional user creation
    read -p "Would you like to use a different user instead of '$(whoami)' for SSH keys? [Y/n]" uuser_choice_1

    # Make answer uppercase
    user_choice_1=${uuser_choice_1^^}

    if [[ $user_choice_1 == "Y" ]]
    then

        read -p "Which user would you like to use (will be created if it does not exist!!!)?: " chosen_user

        check_chosen_user = "$(id $chosen_user)"

        if [[ check_chosen_user == "id: ‘$chosen_user’: no such user"]]
        then

            # Create chosen user and make then
            sudo adduser $chosen_user
            wait

            # Use which to see which package manager executable is installed (which would indicate Debian or Red Hat)
            if [[ -n "$(which apt)" ]]
            then
                sudo usermod -aG sudo $chosen_user

            elif [[ -n "$(which yum)" ]]
            then
                sudo usermod -aG wheel $chosen_user
            fi

        fi
        
         # Create $chosen_user sudoers file in the right directory (need sudo su for echo)
        sudo su -c "echo '$chosen_user     ALL=(ALL)     NOPASSWD: ALL' >> /etc/sudoers.d/$chosen_user"
    
    else

        # If user desires to use current user, set chosen_user to whoami result
        chosen_user="$(whoami)"

    fi 
}

main
