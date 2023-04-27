#!/bin/bash
docker run --env-file .env -d --restart always -v ./data:/home/appuser/data discord_bot
