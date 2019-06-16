# simple-http-server

A better simple http server based on SimpleHTTPServer

## Usage

1. move [http_server.py](http_server.py) and [start.sh](start.sh) to the directory, which contains a file index.html
2. start the http server: `sh start.sh 8080`
3. stop the http server: `kill $(cat pid.txt)`
