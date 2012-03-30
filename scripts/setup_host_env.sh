#!/bin/bash

# USAGE: $ source setup_host_env.sh

if [ ${USER} = "d2rk" ] ; then
    echo "Setup ${USER} host environment"
    export PATH=${PATH}:/opt/parallax/bin/
    echo "PATH = ${PATH}"
    source /usr/local/lib/catalina/bin/use_catalina
fi
