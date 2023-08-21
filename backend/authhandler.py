
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import threading

class AuthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        global code
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        # Extract the authentication code from the query parameters
        query_params = parse_qs(urlparse(self.path).query)
        code = query_params.get("code", [""])[0]

        # Close the server once the code is received
        #print("\nReceived code", code)
        # Close the server once the code is received
        threading.Thread(target=self.server.shutdown).start()
    def getCode():
        return code