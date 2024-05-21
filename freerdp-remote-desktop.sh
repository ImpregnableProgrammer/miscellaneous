#! /bin/bash
# FreeRDP: https://github.com/FreeRDP/FreeRDP/wiki/PreBuilds
# Script to connect to any remote desktop using xfreerdp, prompting the user for desired information
# Used by me to connect to GNOME remote login (port 3389) on my Arch linux desktop, since that seems to result in unexplainable
# TLS handshake rejections when connected to using the Microsoft remote desktop client, but ONLY on macOS and not on iOS for some reason!
# HOWEVER, port 3390 (desktop sharing) DOES work with the Micrsoft client...
read -p "Enter username (blank for none): " USER
read -s -p "Enter password (blank for none): " PASS
echo # Newline
read -p "Enter host address (ip:port): " ADDR
read -p "Enter desired resolution (default 1920x1080): " SIZE
# Bash parameter expansion/substitution: https://www.gnu.org/software/bash/manual/html_node/Shell-Parameter-Expansion.html
export DISPLAY=:0 # Ensure that the XOrg display server is running on display ":0"!!! (Launch XQuartz on macOS)
xfreerdp /u:${USER} /p:${PASS} /v:${ADDR} /size:${SIZE:-1920x1080} +dynamic-resolution +clipboard /sound