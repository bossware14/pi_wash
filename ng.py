#!/usr/bin/env python
#pip install ngrok
#python3 -m pip install ngrok
#touch ng.py
#NGROK_AUTHTOKEN=2q6m1Gd0w8fEuibiwyToH0JEyfx_2ft99jvARhHn2u8Q2EPe1 python3 ng.py

from http.server import HTTPServer, BaseHTTPRequestHandler
import logging, ngrok


class HelloHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        body = bytes("Hello", "utf-8")
        self.protocol_version = "HTTP/1.1"
        self.send_response(200)
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)

logging.basicConfig(level=logging.INFO)

# Create the server and attach ngrok
server = HTTPServer(("localhost", 0), HelloHandler)
ngrok.listen(server)

try:
    logging.info("Starting server. Press Ctrl+C to stop.")
    server.serve_forever()
except KeyboardInterrupt:
    logging.info("Shutting down server...")
    server.server_close()  
    ngrok.kill()  
    logging.info("Server stopped cleanly.")
