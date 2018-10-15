#! /bin/bash

sudo openvpn --config ~/Documents/config/GCRI-DoAB.ovpn
sudo sshfs -o allow_other,IdentityFile=~/.ssh/id_rsa trojak.m@192.168.17.200:/home/trojak.m/ /mnt/drasov_server/