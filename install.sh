#!/bin/bash

set -e
set -x

PYTHONVERSION="python3.8"
LOGFOLDER="/var/log/sysc3010"
SCRIPTFOLDER="/opt/sysc3010"
GITREPO="https://github.com/roger-selzler/SYSC3010"
DATE=$(date '+%Y%m%d-%H%M%S')
echo $DATE
LOGFILE="$LOGFOLDER/${DATE}_SYSC3010install.log"

echo $LOGFILE

#delete older logs
#rm -rf $LOGFOLDER/*

exec &> >(tee $LOGFILE)

if (($EUID != 0));
  then echo -e "This file should run as root.\n\t Type: sudo ./install.sh"
  exit
fi

apt-get -y update
apt dist-upgrade -y
apt-get -y upgrade
apt-get -y autoremove

apt-get -y install $PYTHONVERSION python3-pip


#[ -f ~/.bash_aliases ] || touch ~/.bash_aliases
#if grep -q "alias python" ~/.bash_aliases
#then
#  echo -e "python alias already exist"
#  if ! grep -Fxq "alias python=${PYTHONVERSION}" ~/.bash_aliases
#  then
#    echo -e "\e[33mPython alias using different version than course. Changing it to ${PYTHONVERSION}"
#    sed -i "/alias python=*/c\alias python=${PYTHONVERSION}" ~/.bash_aliases
#  fi
#else
#  echo "alias python=${PYTHONVERSION}" >> ~/.bash_aliases
#fi
#
#if grep -q "alias pip" ~/.bash_aliases
#then
#  sed -i "/alias pip=*/c\alias pip=pip3"
#else
#  echo -e "alias pip=pip3" >> ~/.bash_aliases
#fi

#source ~/.bashrc

pip install netifaces coloredlogs sense_hat

cd /home/pi
[ -d SYSC3010 ] && echo "SYSC3010 already cloned." || git clone ${GITREPO}
cd SYSC3010/
cp showip.py ${SCRIPTFOLDER}/showip.py


