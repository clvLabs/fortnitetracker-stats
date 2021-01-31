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
    "fortniteTracker": {
        "api": {
            "key": "add_your_api_key_here",
            "requestDelay": 0,
            "baseUrl": "https://api.fortnitetracker.com/v1",
            "paths": {
                "profile": "profile/{platform}/{trn_username}",
                "matches": "profile/account/{user_id}/matches"
            }
        },
        "trackerURL": "https://fortnitetracker.com/profile/all/{trn_username}/matches",
        "notificationsURL": "https://notifications.thetrackernetwork.com/api/notifications/?site=Fortnite&userName={public_ip}"
    },
    "profilePinger": {
        "active": false,
        "profilePingInterval": 300
    },
    "apiStatsGetter": {
        "active": true,
        "statusGetInterval": 100
    }
}
```

* `profiles`: list of profiles to be checked
    * `username`: User name
    * `trn_username`: [TRN](https://fortnitetracker.com/article/23/trn-rating-you) username
    * `platform`: User platform
        * Accepted values:
            * `kbm`
            * `gamepad`
            * `touch`
* `fortniteTracker`: fortnitetracker.com settings
    * `api`: api section
        * `key`: api key
        * `requestDelay`: delay between requests
        * `baseUrl`: base url
        * `paths`: path list
            * `profile`: profile path
            * `matches`: matches path
* `profilePinger`: settings for the _profile pinger_
    * `active`: is the module active?
    * `profilePingInterval`: time between _pings_
* `apiStatsGetter`: settings for the _stats getter_
    * `active`: is the module active?
    * `statusGetInterval`: time between _gets_


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
