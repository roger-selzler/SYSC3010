#!/bin/bash

activateshowip=false
while getopts :y flag
do
  case "${flag}" in
    y) activateshowip=true
  esac
done


showipfile="/opt/sysc3010/showip"
if [ $activateshowip == true ]
then
  [ -f ${showipfile} ] && rm -rf "/opt/sysc3010/showip"
   echo "SenseHat will show the ip from the interfaces on reboot"
else
  touch ${showipfile}
  #pkill -f -9 showip.py
  echo "SenseHat will not show the ip from the interfaces after reboot"
fi