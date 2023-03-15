#!/bin/bash
docker run --env-file .env -d -v /tmp/data:/home/appuser/data discord_bot