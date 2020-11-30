from flask import request
import socketserver
import http.server
import threading
from pymongo import MongoClient
from classes.CandCdatabase import Server_obj

client = MongoClient('localhost', 27017)
db = client['CandC']
collection = db['CandC_bots']
server = Server_obj(0,"",0,"")

class microServer:
    def __init__(self):
        self.interface = ""
        self.port = 0

    def runServer(self,interface,port):
        print("Server running up at %s:%s" %(interface,port))
        thread = threading.Thread(target=standup,args=(interface,port))
        print(str(thread.name))
        thread.start()
             
    def stopServer(self, server_id):

        return 0
    
def standup(interface, port):
    print("Server standing up at %s%s" %(interface,port))
    server_handle = http.server.SimpleHTTPRequestHandler
    server= socketserver.TCPServer((interface,port),server_handle)
    print("Web server active at %s%s" % (interface,str(port)))
    server.serve_forever()
