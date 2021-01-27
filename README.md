# fortnitetracker-stats

Stats and tools for fortnitetracker.com

## Setup on the Raspberry Pi

* Clone the repo somewhere on your Pi.
* Run `scripts/setup.sh` from the project folder.

This will create a few new files:
* `app/config.json`: edit this one after setup
* `logs/setup/setup-completed.txt`: flag to avoid re-installing
* `logs/setup/setup.log`: log of the setup process
* `scripts/start.sh`: customized start script (called by systemd)
* `scripts/devrun.sh`: customized development start script (see [Run in development mode](#run-in-development-mode))

## Usage

The app is started as a `systemd` service, so there's not much to do besides starting your Pi...

### Web interface

`TO-DO`

### Stats storage

`TO-DO`

### Service logs

Service logs are stored in `/var/log/fortnitetracker-stats/servicelog` and rotated with `logrotate` (see `resources/setup/logrotate` for details)

## Development

### Disable the systemd service

To be able to start developing you must first stop and disable the service.

```
$ sudo systemctl stop fortnitetracker-stats.service
$ sudo systemctl disable fortnitetracker-stats.service
```

### Run in development mode

Run `scripts/devrun.sh` from the project folder.

This will start the program in `watch` mode: if you change any `py` file the program will automatically restart.

### Edit the source files from your computer

If you want to edit the source files with your editor you can use `sshfs` to mount the `fortnitetracker-stats` folder from your Pi on a folder in your local system.

Let's assume:
* The Pi is on 192.168.1.100
* The code folder at the Pi is `/home/pi/fortnitetracker-stats`
* The code folder at the computer is `/home/myuser/source/fortnitetracker-stats`

To mount the folder on your local system, run this **on your computer**:
```
$ sudo sshfs -o allow_other pi@192.168.1.100:/home/pi/fortnitetracker-stats/ /home/myuser/source/fortnitetracker-stats
```

While the folder is mounted you can use your editor of choice in your host computer to edit files on the Pi.

This works together with `devrun.sh` so when you save the file on your computer the program will automatically restart on the Pi.

Once you are finished you should unmount the folder:

```
$ sudo umount /home/myuser/source/fortnitetracker-stats
```

### Re-enable the systemd service

To re-enable the service:

```
$ sudo systemctl enable fortnitetracker-stats.service
$ sudo systemctl start fortnitetracker-stats.service
```

