# simple-http-server

A better simple http server based on SimpleHTTPServer

## Usage

1. move [http_server_start.py](http_server_start.py) and [http_server_start.sh](http_server_start.sh) to the directory, which contains a file index.html
2. start the http server: `sh http_server_start.sh 8080`
3. stop the http server: `kill $(cat pid.txt)`
