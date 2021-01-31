# config.json

The `config.json` file contains the app settings:

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
