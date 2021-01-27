#!/bin/bash

function log {
  echo -e "\e[32m$@\e[0m"
}

# -----------------------------------------

APP_NAME="fortnitetracker-stats"
BASE_PATH="$PWD"
APP_PATH="$BASE_PATH/app"
RESOURCES_PATH="$BASE_PATH/resources"
SCRIPTS_PATH="$BASE_PATH/scripts"
LOGS_PATH="$BASE_PATH/logs"
SETUP_LOGS_PATH="$LOGS_PATH/setup"
SETUP_RESOURCES_PATH="$RESOURCES_PATH/setup"
SETUP_SIGNATURE_FILE="$SETUP_LOGS_PATH/setup-completed.txt"
SETUP_LOG_FILE="$SETUP_LOGS_PATH/setup.log"

# -----------------------------------------

if ! [ -f "$SCRIPTS_PATH/setup.sh" ]
then
    log "Please run this from the project folder"
    exit 1
fi

# -----------------------------------------

log -
log - $APP_NAME setup - $(date)
log -

if [ -e $SETUP_SIGNATURE_FILE ]; then
	log - Setup already done, doing nothing...
	exit 0
fi

log - ----------------------------------------------------------------------------
log -
log - Updating OS...
log -
sudo apt -y update

log - ----------------------------------------------------------------------------
log -
log - Installing dependencies...
log -
sudo apt -y install watch entr tree screen
# pip3 install flask

# log - ----------------------------------------------------------------------------
# log -
# log - Creating directories...
# log -

log - ----------------------------------------------------------------------------
log -
log - Initializing config...
log -
cp --verbose --no-clobber $SETUP_RESOURCES_PATH/config.json $APP_PATH

log - ----------------------------------------------------------------------------
log -
log - Creating custom scripts...
log -
cp --verbose $SETUP_RESOURCES_PATH/start.sh $SCRIPTS_PATH/start.sh
sed --in-place "s|__BASE_PATH__|${BASE_PATH}|g" $SCRIPTS_PATH/start.sh

cp --verbose $SETUP_RESOURCES_PATH/devrun.sh $SCRIPTS_PATH/devrun.sh
sed --in-place "s|__BASE_PATH__|${BASE_PATH}|g" $SCRIPTS_PATH/devrun.sh

log - ----------------------------------------------------------------------------
log -
log - Setting up systemd service...
log -
SERVICE_NAME=$APP_NAME.service
sudo cp --verbose $SETUP_RESOURCES_PATH/$SERVICE_NAME /lib/systemd/system/$SERVICE_NAME
sudo sed --in-place "s|__BASE_PATH__|${BASE_PATH}|g" /lib/systemd/system/$SERVICE_NAME
sudo chmod --verbose 644 /lib/systemd/system/$SERVICE_NAME
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME
sudo systemctl status $SERVICE_NAME

log - ----------------------------------------------------------------------------
log -
log - Setting up log rotation...
log -
sudo mkdir --parents /var/log/$APP_NAME
sudo cp --verbose $SETUP_RESOURCES_PATH/logrotate /etc/logrotate.d/$APP_NAME
sudo chmod 0644 /etc/logrotate.d/$APP_NAME
# Uncomment this to do a "dry run" to check configuration
# logrotate /etc/logrotate.conf --debug

log - ----------------------------------------------------------------------------
log -
log - $APP_NAME setup finished !!!
log - Setup log saved as $SETUP_LOGS_PATH/setup.log
log -
echo $(date) > $SETUP_SIGNATURE_FILE
