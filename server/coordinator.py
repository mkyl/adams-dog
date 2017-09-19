#!/usr/bin/python3

import number_manager

import socket
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

hostName = ""
hostPort = 1513

number_manager = number_manager.NumberManager()

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.protocol_version='HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            message = number_manager.get_a_unknown_number_index()
            self.wfile.write(bytes("http://www.countablethoughts.com/concat-then-factor/dl.py?%s" % message , "utf-8"))
        elif self.path == "/status" or self.path == "/status/":
            self.protocol_version='HTTP/1.1'
            self.send_response(200, 'OK')
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("%d out of 1513 numbers are still unknown" % number_manager.how_many_known(), "utf-8"))
        else:
            self.protocol_version='HTTP/1.1'
            self.send_response(404)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes("File not found\n", "utf-8"))

    def do_POST(self):
        print( "incomming http: ", self.path )
        content_length = int(self.headers['Content-Length'])
        post_data = str(self.rfile.read(content_length), "utf-8")
        self.send_response(200)

        parts = post_data.split(",")
        number_manager.now_known_number(parts[0], parts[1])

myServer = HTTPServer((hostName, hostPort), MyServer)
print(time.asctime(), "Server Start")

try:
    myServer.serve_forever()
except KeyboardInterrupt:
    pass

myServer.server_close()
print(time.asctime(), "\nServer Stop")
