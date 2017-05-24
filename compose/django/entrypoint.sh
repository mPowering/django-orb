#!/bin/bash
set -e
cmd="$@"

# ./wait-for-it.sh mysql:3306

exec $cmd
