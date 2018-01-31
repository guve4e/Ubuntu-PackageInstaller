# Ubuntu-PackageInstaller
Python script that installs packages

# How to run?
Compile installer.c
```
gcc -o installer runscript.c
```
Then give it permission.
```
sudo chown root:root installer installer.py
sudo chmod 4755 installer installer.py
```
Run  
```
./installer
```

Or execute:
```
chmod +x run_first.sh
./run_first.sh
```
And then Run  
```
./installer <NAME_OF_CONFIG>
```

# How it works?

### Installing packages
The configuration files are located in folder "configs".  
In each configuration folder there are json files.
* json file "packages.json" contains information how to install packages as:
```
sudo add-apt-repository ppa:wireshark-dev/stable
sudo apt update
sudo apt install wireshark
```

### Installing from source
* json file "programs.json" contains information how to download,   
or extract a tar to a specific folder and then extract the source.  
If "download_url" is not specified, the scripts is looking for a file in  
"alternative_dir" to unarchive to "directory". Note if you choose to work  
with already downloaded files, they have to be downloaded prior to running  
the script. The filed "commands" is used if the donloaded file needs  
additional commands. 

```
{
    "name" : "No-IP",
    "prerequisites" : "",
    "download_url" : "http://www.no-ip.com/client/linux/noip-duc-linux.tar.gz",
    "alternative_dir" : "",
    "commands" : [
      {
        "commandDescription" : "install",
        "command" : "some command -y"
      }
    ],
    "directory" : "/usr/local/bin"
  }
```