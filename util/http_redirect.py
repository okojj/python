#!/usr/bin/env python
# simeple httpd
#
import sys
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
import SimpleHTTPServer
import SocketServer

default_port = 8000
redirect_url = "http://www.okojj.com/"

if sys.argv[1:]:
    port = int(sys.argv[1])
else:
    port = default_port


class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(302)
		self.send_header('Location',redirect_url)
		self.end_headers()
		# Send the html message
		#self.wfile.write("Hello World !")
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', port), myHandler)
	print 'Started httpserver on port ' , port
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()