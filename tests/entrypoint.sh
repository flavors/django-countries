#!/bin/bash

set -e

while ! nc -z localhost 5432; do
    >&2 echo "Postgres is zzZzZzZZzZzzz"
    sleep 5
done

>&2 echo "Postgres is up!!"
