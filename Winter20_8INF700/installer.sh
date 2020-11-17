#!/bin/bash

#Installation of the external modules with pip3
echo
pip3 install darkskylib
echo
pip3 install keyring
echo
pip3 install spotify-token
echo
pip3 install fbchat
echo
sudo apt-get install python3-pyqt5
echo
sudo apt-get install mpg123
echo



#raspotify installation
sudo apt update
echo
echo
sudo apt upgrade

#To make sure that curl and apt-transport https are installed
sudo apt install -y apt-transport-https curl
echo
echo

#Add the raspotify GPG key and its repository
curl -sSL https://dtcooper.github.io/raspotify/key.asc | sudo apt-key add -v -
echo 
echo 'deb https://dtcooper.github.io/raspotify raspotify main' | sudo tee /etc/apt/sources.list.d/raspotify.list
echo
echo

#Install raspotify
sudo apt-get update
echo
echo
sudo apt-get install raspotify
echo
echo

#Install sed
sudo apt-get install sed
echo
echo

#To make sure that git is installed
sudo apt-get install git 
echo
echo

#Create an hidden folder for the git repository
cd ~/Documents
mkdir .RPI-Alarm-Clock
cd ~/Documents/.RPI-Alarm-Clock

#Download the repository
git clone https://github.com/map555/Winter2020-8INF700.git #Download the programm and save it into the hidden folder
echo
echo


cd ~/Documents/.RPI-Alarm-Clock/Winter2020-8INF700/Winter20_8INF700
./setAutorisationTokens.sh #Setting the keyrings

#Move the .rules file to allow to have the read and write permission on the config file of the touch screen's backlight
sudo mv backlight-permissions.rules /etc/udev/rules.d/

#Move the .desktop shortcut to the desktop directory
sudo mv ~/Documents/.RPI-Alarm-Clock/Winter2020-8INF700/Winter20_8INF700/8INF700.desktop ~/Desktop

echo -e "\tInstallation completed\n\tBefore executing the program, please configure the raspotify's config file by following the instructions to configure the Spotify Connect Software on this website:\n\thttps://pimylifeup.com/raspberry-pi-spotify/"




