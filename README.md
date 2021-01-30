# fortnitetracker-stats

Stats and tools for fortnitetracker.com

## Setup

* Clone the repo
* Copy the `sample/config` folder in the main repo folder as `config`
* Edit `config/config.json`
* Build the Docker image with `scripts/build.sh`

### config.json

```json
{
    "profiles": [
        {
            "username": "first_user",
            "trn_username": "first_user",
            "platform": "kbm"
        },
        {
            "username": "other_user_not_epic",
            "trn_username": "psn(other_user_not_epic)",
            "platform": "gamepad"
        },
        {
            "username": "third_user",
            "trn_username": "third_user",
            "platform": "touch"
        }
    ],
    "profilePinger": {
        "active": true,
        "trackerURL": "https://fortnitetracker.com/profile/all/{trn_username}/matches",
        "notificationsURL": "https://notifications.thetrackernetwork.com/api/notifications/?site=Fortnite&userName={public_ip}",
        "requestDelay": 0.5,
        "profileUpdateDelay": 300
    },
    "apiHeaders": {
        "TRN-Api-Key": "add_here_your_api_key"
    },
    "apiStatsGetter": {
        "active": true,
        "profileURL": "https://api.fortnitetracker.com/v1/profile/{platform}/{trn_username}",
        "matchesURL": "https://api.fortnitetracker.com/v1/profile/account/{user_id}/matches",
        "statsUpdateDelay": 100,
        "requestDelay": 2
    }
}
```

* `profiles`: list of profiles to be checked
    * `username`: TO-DO: add desc
    * `trn_username`: TO-DO: add desc
    * `platform`: TO-DO: add desc
* `profilePinger`: settings for the _pinger_
    * `active`: is the module active?
    * `trackerURL`: TO-DO: add desc
    * `notificationsURL`: TO-DO: add desc
    * `requestDelay`: TO-DO: add desc
    * `profileUpdateDelay`: TO-DO: add desc
* `apiHeaders`: TO-DO: add desc
    * `TRN-Api-Key`: TO-DO: add desc
* `apiStatsGetter`: settings for the _stats getter_
    * `active`: is the module active?
    * `trackerURL`: TO-DO: add desc
    * `profileURL`: TO-DO: add desc
    * `matchesURL`: TO-DO: add desc
    * `statsUpdateDelay`: TO-DO: add desc
    * `requestDelay`: TO-DO: add desc


## Usage

### Start the service
```
$ scripts/start.sh
```

### Stop the service
```
$ scripts/stop.sh
```

### Restart the service
```
$ scripts/restart.sh
```

### Update the service
```
$ scripts/update.sh
```

### View service logs
```
$ scripts/logs.sh
```

### Build the container
```
$ scripts/build.sh
```


## Development

### Build image
```
$ dev/build.sh
```

### Build image (force full rebuild)
```
$ dev/build.sh --no-cache
```

### Run container with code mapped to local copy
```
$ dev/run.sh
```

### Run container with code mapped to local copy (with restart on changes)
```
$ dev/devwatch.sh
```

### Restart container
```
$ dev/restart.sh
```

### Stop container
```
$ dev/stop.sh
```

### Run a container starting with a bash shell
```
$ dev/shell.sh
```

### Get a bash shell in a running container
```
$ docker exec -it fortnitetracker-stats bash
```
