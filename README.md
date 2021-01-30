# fortnitetracker-stats

Stats and tools for fortnitetracker.com

## Setup

* Clone the repo
* Copy `sample/config` as `config`
* Edit `config.json`
* Build the Docker image with `docker-compose build`

### config.json

```json
{
    "profiles": [
        {
            "username": "first_user",
            "trn_username": "first_user",
            "platform": "kbd"
        },
        {
            "username": "other_user_not_epic",
            "trn_username": "psn(other_user_not_epic)",
            "platform": "gamepad"
        },
        {
            "username": "third_user",
            "trn_username": "third_user",
            "platform": "gamepad"
        }
    ],
    "profilePinger": {
        "active": true,
        "trackerURL": "https://fortnitetracker.com/profile/all/{user}/matches",
        "notificationsURL": "https://notifications.thetrackernetwork.com/api/notifications/?site=Fortnite&userName={ip}",
        "requestDelay": 0.5,
        "profileUpdateDelay": 300
    },
    "apiHeaders": {
        "TRN-Api-Key": "add_here_your_api_key"
    },
    "apiStatsGetter": {
        "active": true,
        "trackerURL": "https://api.fortnitetracker.com/v1/",
        "profileURL": "https://api.fortnitetracker.com/v1/profile/{platform}/{trn_username}",
        "matchesURL": "https://api.fortnitetracker.com/v1/profile/account/{user_id}/matches",
        "requestDelay": 100
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
    * `requestDelay`: TO-DO: add desc


## Usage

Once the image has been built you can start the service with `docker-compose up -d`.

This will start the container in _detached_ mode.

If you want to see its logs, use `docker-compose logs -f`

You can stop the service with `docker-compose down`

## Development

### Build image
```bash
$ dev/build.sh
```

### Build image (force full rebuild)
```bash
$ dev/build.sh --no-cache
```

### Run container with code mapped to local copy
```bash
$ dev/run.sh
```

### Run container with code mapped to local copy (with restart on changes)
```bash
$ dev/devwatch.sh
```

### Restart container
```bash
$ dev/restart.sh
```

### Stop container
```bash
$ dev/stop.sh
```

### Run a container starting with a bash shell
```bash
$ dev/shell.sh
```

### Get a bash shell in a running container
```bash
$ docker exec -it fortnitetracker-stats bash
```
