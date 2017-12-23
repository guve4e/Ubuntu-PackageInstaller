#!/bin/sh

echo "Compiling and Changing permission of the script"

gcc -o installer installer.c
sudo chown root:root installer installer.py
sudo chmod 4755 installer installer.py

echo "Done"
