#  coding: utf-8 
import socketserver
import os

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/


class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print ("Got a request of: %s\n" % self.data)

        data = self.data.split(b' ')

        # Check if method is GET
        if bytes("GET", 'utf-8') == data[0]:
            path = data[1].decode('utf-8')
            print("Path is", path)

            if path == '/':
                self.request.send(bytes("HTTP/1.1 200 OK\r\n", 'utf-8'))

            # open file
            else:
                try:
                    print("www" in path)
                    cur_dir = os.path.abspath(os.getcwd())
                    if 'www' in path:
                        print("cur dir type is", type(cur_dir))
                        path = str(cur_dir) + path
                    else:
                        path = str(cur_dir) + "/www" + path

                    print("new path is", path)
                    file = open(path)
                    file_type = path.split('.')[1]
                    print("file type is", file_type)
                    output_data = file.read()

                    if file_type == 'html':
                        self.request.send(bytes("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: " + str(len(output_data)) + "\r\n" + output_data, 'utf-8'))
                    elif file_type == 'css':
                        self.request.send(bytes("HTTP/1.1 200 OK\r\nContent-Type: text/css\r\nContent-Length: " + str(len(output_data)) + "\r\n" + output_data, 'utf-8'))
                
                except IOError:
                    print("ERRRRRRRRRRRRRRRRROR")
                    self.request.send(bytes("HTTP/1.1 404 Not Found\r\n", 'utf-8'))

        else:
            self.request.send(bytes("HTTP/1.1 405 Method Not Allowed\r\n", 'utf-8'))


        self.request.sendall(bytearray("OK",'utf-8'))

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()

    
    """ BUFFER_SIZE = 1024
    
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)
        
        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            
            print("Connected by", addr)
            
            try:
                # get filename from data and read file
                data = conn.recv(BUFFER_SIZE)
                filename = data.split()[1]
                file = open(filename[1:])
                output_data = file.read()
                
                # send header and data
                full_data = "HTTP/1.1 200 OK\nContent-Type: text/html\nContent-Length: " + str(len(output_data)) + "\n\n" + output_data
                conn.send(full_data)
                conn.close()
            
            # if file does not exist
            except IOError:
                conn.send("HTTP/1.1 404 Not Found\n")
                conn.close() """

    
    
