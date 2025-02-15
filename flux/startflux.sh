#!/bin/bash

#find if any process is running xflux
state=$(ps -a | grep xflux)
#echo "$state"

#get zipcode from ipinfo.io using curl
zipcode=$(curl -s ipinfo.io/postal)
#echo "$zipcode"

#-n tests if has value -z tests for empty
#need space on each side of "[" and "]"
#if we don't have a process running, start new flux
if [ -z "$state" ];
then
    ./xflux -z "$zipcode"
else
    echo "Flux is already running"
fi


