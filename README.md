# fortnitetracker-stats

Stats and tools for fortnitetracker.com

## Setup

* Make sure you have [docker](https://docs.docker.com/engine//) and [docker-compose](https://docs.docker.com/compose/) installed on your system
* Clone the project repo
```
$ git clone https://github.com/clvLabs/fortnitetracker-stats.git
```

* Enter the local repo folder
```
$ cd fortnitetracker-stats
```

* Copy the `sample/config` folder as `config`
```
$ cp -r sample/config ./config
```

* Edit `config/config.json` ([more info](sample/config/config.md))
```
$ nano config/config.json
```

* Build the Docker image
```
$ scripts/build.sh
```

## Usage

* Start the service: `scripts/start.sh`
* Stop the service: `scripts/stop.sh`
* Restart the service: `scripts/restart.sh`
* Update the service: `scripts/update.sh`
* View service logs: `scripts/logs.sh`
* Build the container: `scripts/build.sh`

## Development

* Build image: `dev/build.sh`
* Build image (force full rebuild): `dev/build.sh --no-cache`
* Run container with code mapped to local copy: `dev/run.sh`
* Run container with code mapped to local copy (with restart on changes): `dev/devwatch.sh`
* Restart container: `dev/restart.sh`
* Stop container: `dev/stop.sh`
* Kill container: `dev/kill.sh`
* Run a container starting with a bash shell: `dev/shell.sh`
* Get a bash shell in a running container: `docker exec -it fortnitetracker-stats bash`
