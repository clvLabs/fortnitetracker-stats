FROM python:3

# Update apt cache
RUN apt update

# Copy app files needed for setup
COPY app/setup /fortnitetracker-stats/app/setup
COPY app/scripts /fortnitetracker-stats/app/scripts

# Run app setup
RUN /fortnitetracker-stats/app/setup/scripts/setup.sh

# Clean setup files
RUN rm -rf /fortnitetracker-stats/app/setup

# Copy app code
COPY app /fortnitetracker-stats/app

# Set default working dir & entry point
WORKDIR /fortnitetracker-stats/app
ENTRYPOINT ["scripts/start.sh"]
