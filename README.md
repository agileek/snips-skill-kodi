# Snips UPNP forward
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](https://raw.githubusercontent.com/agileek/snips-skill-upnp/master/LICENSE.txt)

This is a Snips action written in Python and is compatible with `snips-skill-server`.
This action forwards any sound played locally on any UPNP server (KODI,...) .

## Setup

### SAM (preferred)
To install the action on your device, you can use [Sam](https://snips.gitbook.io/getting-started/installation)

`sam install action -g https://github.com/agileek/snips-skill-upnp.git`

### Manually

Copy it manually to the device to the folder `/var/lib/snips/skills/`
You'll need `snips-skill-server` installed on the pi

`sudo apt-get install snips-skill-server`

Stop snips-skill-server & generate the virtual environment
```
sudo systemctl stop snips-skill-server
cd /var/lib/snips/skills/snips-skill-upnp/
sh setup.sh
sudo systemctl start snips-skill-server
```

## Logs
Show snips-skill-server logs with sam:

`sam service log snips-skill-server`

Or on the device:

`journalctl -f -u snips-skill-server`

Check general platform logs:

`sam watch`

Or on the device:

`snips-watch`
