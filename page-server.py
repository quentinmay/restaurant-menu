import http.server
import socketserver
from urllib.parse import urlparse, parse_qs
from urllib import parse
import io
from io import BytesIO
from PIL import Image
import base64

import json

class MyHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Sending an '200 OK' response
        self.send_response(200)

        # Setting the header
        # self.send_header("Content-type", "application/json")
        # self.send_header("Content-type", "text/html")

        # Whenever using 'send_header', you also have to call 'end_headers'
        # self.end_headers()

        # Extract query param
        # global name 
        # query_components = parse_qs(urlparse(self.path))
        # print('query_components', query_components)
        # if 'name' in query_components:
        #     name = query_components["name"][0]
        # parse_res=parse.urlparse(self.path)
        # print('parse_res', parse_res.path[1:])

        # tacoshop = 

        if self.path == '/tacoshop':
            self.path = './public'+ self.path + '.html'
        elif self.path.endswith('.json'):
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.path = './public' + self.path
            f = open(self.path, 'rb')
            self.wfile.write(f.read())
            f.close()
            return
        elif self.path.endswith('.jpg'):
            self.send_header('Content-type', 'image/jpg')
            self.end_headers()
            self.path = './public/media' + self.path
            f = open(self.path, 'rb')
            self.wfile.write(f.read())
            f.close()
            return
        elif self.path == "/favicon.ico":
            self.send_header("Content-type", "image/x-icon")
            self.end_headers()
            self.path = './public/media'+ self.path
            f = open(self.path, 'rb')
            self.wfile.write(f.read())
            f.close()
            return
        elif self.path == "/sample":
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.path = "./public/sample.html"
            f = open(self.path, 'rb')
            self.wfile.write(f.read())
            f.close()
            return
        elif self.path.endswith('.css'):
            self.send_header("Content-type", "text/css")
            self.end_headers()
            self.path = "./public" + self.path
            f = open(self.path, 'rb')
            self.wfile.write(f.read())
            f.close()
            return
        else:
            self.path = './public'+ self.path

        print(self.path)
        
        # self.path = './public/'+'.html'
        
        
        # # Some custom HTML code, possibly generated by another function
        # html = f"<html><head></head><body><h1>Hello {name}!</h1></body></html>"

        # # Writing the HTML contents with UTF-8


        #return
        return http.server.SimpleHTTPRequestHandler.do_GET(self)


    def do_POST(self):
        credentials = "username:password"
        message_bytes = credentials.encode('ascii')
        base64_bytes = base64.b64encode(message_bytes)
        base64_credentials = base64_bytes.decode('ascii')
        if self.headers['Authorization'] != "Basic " + base64_credentials:
            return
        elif self.path == '/upload':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            dataJson = json.loads(post_data)

            response = BytesIO()
            response.write(b'This is POST request. ')
            response.write(b'Received: ')
            response.write(post_data)
            self.wfile.write(response.getvalue())


            with open('./public' + dataJson["fileName"], 'w+') as fileToSave:
                 json.dump(dataJson["menu"], fileToSave, ensure_ascii=True, indent=4)
        elif self.path == '/picture':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            dataJson = json.loads(post_data)

            image = base64.b64decode(dataJson["fileData"])
            response = BytesIO()
            response.write(b'This is POST request. ')
            response.write(b'Received: ')
            response.write(post_data)
            self.wfile.write(response.getvalue())

            img = Image.open(io.BytesIO(image))
            img.save("./public/media/" + dataJson["fileName"], 'jpeg')


# Create an object of the above class
handler_object = MyHttpRequestHandler

PORT = 80
my_server = socketserver.TCPServer(("", PORT), handler_object)

# Star the server
my_server.serve_forever()
