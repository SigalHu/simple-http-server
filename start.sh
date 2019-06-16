#!/usr/bin/env bash

HOME=$(dirname $(readlink -f $0))
PORT=$1

PYTHON_VERSION=`python -V 2>&1|awk '{print $2}'|awk -F '.' '{print $1}'`

if [[ ${PYTHON_VERSION} == 3 ]]; then
    2to3 -w ${HOME}/http_server.py
fi
nohup python ${HOME}/http_server.py ${PORT} 1>${HOME}/nohup.out 2>&1 &
