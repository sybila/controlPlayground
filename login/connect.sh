#! /bin/bash

# use in separate terminals
sudo umount -l /mnt/drasov_server
sudo sshfs -o allow_other,IdentityFile=~/.ssh/id_rsa trojak.m@192.168.17.200:/home/trojak.m/ /mnt/drasov_server/

#
sudo openvpn --config ~/Documents/config/GCRI-DoAB.ovpn