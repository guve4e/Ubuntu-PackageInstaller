#!/bin/sh

echo "Compiling and Changing permission of the script"

gcc -o runscript runscript.c
sudo chown root:root runscript installer.py
sudo chmod 4755 runscript installer.py

echo "Done"
