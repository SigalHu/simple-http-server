#!/usr/bin/env bash

HOME=$(dirname $(readlink -f $0))
PORT=$1

nohup python ${HOME}/http_server.py ${PORT} 1>${HOME}/nohup.out 2>&1 &
