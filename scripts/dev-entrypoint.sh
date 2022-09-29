#!/bin/sh

/scripts/wait-for-it.sh "$POSTGRES_HOST:$POSTGRES_PORT"

exec "@$"