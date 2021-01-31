FROM python:3

# Update apt cache
RUN apt update

# Copy app code
COPY app /fortnitetracker-stats/app

# Run app setup
RUN \
    /fortnitetracker-stats/app/setup/scripts/setup.sh && \
    rm -rf /fortnitetracker-stats/app/setup && \
    true

# Set default working dir & entry point
WORKDIR /fortnitetracker-stats
ENTRYPOINT ["/fortnitetracker-stats/app/scripts/start.sh"]
