#!/bin/bash

set -e
set -x

PYTHONVERSION="python3.8"
LOGFOLDER="/var/log/sysc3010"
SCRIPTFOLDER="/opt/sysc3010"
GITREPO="https://github.com/roger-selzler/SYSC3010"
DATE=$(date '+%Y%m%d-%H%M%S')
echo $DATE
[ ! -d ${LOGFOLDER} ] && mkdir ${LOGFOLDER}
[ ! -d ${SCRIPTFOLDER} ] && mkdir ${SCRIPTFOLDER}

LOGFILE="$LOGFOLDER/${DATE}_SYSC3010install.log"

echo $LOGFILE

[ ! -d ${SCRIPTFOLDER} ] && mkdir ${SCRIPTFOLDER}

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

sudo -u pi pip install netifaces coloredlogs sense_hat

cd /home/pi
if [ -d SYSC3010 ]
then
  echo "SYSC3010 already cloned."
  cd SYSC3010
  sudo -u pi git clean -df
  sudo -u pi git checkout -- .
  sudo -u pi git pull --rebase --quiet origin main
else
  sudo -u pi git clone ${GITREPO}
  cd SYSC3010
fi
sysc3010repofolder=$(pwd)

[ -f ${SCRIPTFOLDER}/showip ] && sudo rm -rf ${SCRIPTFOLDER}/showip.py
cp showip.py ${SCRIPTFOLDER}/showip.py
chmod 777 showip.sh


echo "cd ${sysc3010repofolder}
sudo -u pi git clean -df
sudo -u pi git checkout -- .
sudo -u pi git pull --rebase --quiet origin main
cp showip.py ${SCRIPTFOLDER}/showip.py
" | sudo tee ${SCRIPTFOLDER}/pullgit.sh

crontabtime="00 08 * * * pi"
croncmd1="$crontabtime sudo bash ${SCRIPTFOLDER}/pullgit.sh"
croncmd2="@reboot sleep 30 && sudo bash ${SCRIPTFOLDER}/pullgit.sh"
sudo -u pi crontab -l | grep -Fxq "$croncmd1" && echo "$croncmd1 already exist" || (sudo -u pi crontab -l ; echo "${croncmd1}") | sudo -u pi crontab -
sudo -u pi crontab -l | grep -Fxq "$croncmd2" && echo "$croncmd2 already exist" || (sudo -u pi crontab -l ; echo "${croncmd2}") | sudo -u pi crontab -

#check if showip is in crontab, and write to it if not.
crontabcmd="@reboot sleep 40 && [ ! -f ${SCRIPTFOLDER}/showip ] && python ${SCRIPTFOLDER}/showip.py &"
sudo -u pi crontab -l | grep -Fxq "${crontabcmd}" && echo "${crontabcmd} already exist" || (sudo -u pi crontab -l ; echo ${crontabcmd}) | sudo -u pi crontab -



sudo chmod o+w ${SCRIPTFOLDER} #permission to delete files

