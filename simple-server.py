import http.server
import socketserver
from urllib.parse import urlparse
from urllib.parse import parse_qs
from urllib import parse
from io import BytesIO
import json
import requests


class SimpleHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        #print(self.path)
        parse_res=parse.urlparse(self.path)
        #print('parse_res', parse_res.path[1:])

        print
        # tacoshop = 
        if self.path == '/tacoshop':
            self.path = './public'+ self.path + '.html'
        else:
            self.path = './public'+ self.path

        # # Get: read json file from request
        # data = requests.get('http://localhost:8000/example.json').json()
        # print(data)
        # print()

        return http.server.SimpleHTTPRequestHandler.do_GET(self)

       

    def do_POST(self):

        content_length = int(self.headers['Content-Length'])
        body = self.rfile.read(content_length)
        self.send_response(200)
        self.end_headers()

        data = json.loads(body)
        
        #print('post_json_data: ', data)

        # This is the response from post, check it from postman
        response = BytesIO()
        response.write(b'This is POST request. ')
        response.write(b'Received: ')
        response.write(body)
        self.wfile.write(response.getvalue())

        with open('./public/example.json', 'w') as f:
            json.dump(data, f)
        

        

httpd = http.server.HTTPServer(('localhost', 8001), SimpleHTTPRequestHandler)
httpd.serve_forever()
