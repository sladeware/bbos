#!/bin/bash

if [ ${USER} = "d2rk" ] ; then
    #echo "Setup ${USER} host environment"
    PATH=/opt/parallax/bin/:$PATH
    source /usr/local/lib/catalina/bin/use_catalina
fi
