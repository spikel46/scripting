#!/bin/bash

variable=`ps -a | grep 'xflux' | awk '{ printf("kill %s\n",$1) }'`
$variable
