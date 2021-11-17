#!/bin/bash

activateshowip=false
#while getopts y: flag
#do
#  case "${flag}" in
#    y) activateshowip=true
#  esac
#done
for i in "$@";do
  if [[$i==y]]; then
    activateshowip=true
  fi
done


showipfile="/opt/sysc3010/showip"
if activateshowip
then
  touch ${showipfile}
else
  [ -f ${showipfile} ] && sudo rm -rf "/opt/sysc3010/showip"
fi