#!/bin/bash
set -e
cmd="$@"

# This entrypoint is used to play nicely with the current cookiecutter configuration.
# Since docker-compose relies heavily on environment variables itself for configuration, we'd have to define multiple
# environment variables just to support cookiecutter out of the box. That makes no sense, so this little entrypoint
# does all this for us.


# wait for mysql to be ready
nc -z mysql 3306
n=$?
while [ $n -ne 0 ]; do
    sleep 1
    nc -z mysql 3306
    n=$?
done

exec $cmd
