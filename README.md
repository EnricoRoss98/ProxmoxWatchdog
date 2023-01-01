# Proxmox Watchdog
Python Script that checks if VMs gets stuck, if one is detected, the script stop the VM and restart it
using Proxmox REST API. The script checks also if VMs are running before resetting them (a stopped VM
is not restored).
Keep in mind that this script must be placed on a machine separated by the Proxmox host. 

```bash
su -
git pull https://github.com/EnricoRoss98/ProxmoxWatchdog.git
cd ProxmoxWatchdog
sudo apt-get install python3-venv
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

Now is time to edit the variables inside the main script:
```bash
nano main.py
```

After that, add this script to crontab to let the machine execute it repeatedly:
```bash
crontab -e
```

And add the following line (the script is executed every 2 minutes, you can change that by modifying
the number at the third char):
```bash
*/2 * * * * ProxmoxWatchdog/venv/bin/python3 ProxmoxWatchdog/main.py >> ProxmoxWatchdog/WatchdogOUT.txt
```

Logs for all reboots can be consulted by opening WatchdogOUT.txt with nano for example.
