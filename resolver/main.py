import falcon
from waitress import serve
import requests
import json
import random
import socket

class dht:

    @staticmethod
    def findpeer(peer_id):
        "http://127.0.0.1:5002/api/v0/dht/provide?arg=<key>"
        endpoint = "http://127.0.0.1:5002/api/v0/dht/findpeer?arg="+peer_id
        #print ("Pre-request")
        resp = requests.post(endpoint)
        print (resp.status_code)
        if resp.status_code != 200:
            #print ("None:","p2p.listener")
            return None

        return resp.text


    @staticmethod
    def forward(protocol,listen_address,target_address,allow_custom_protocol):
        endpoint = "http://127.0.0.1:5002/api/v0/p2p/forward?arg="+protocol+"&arg="+listen_address+"&arg="+target_address+"&allow-custom-protocol="+("true" if allow_custom_protocol else "false")
        resp = requests.post(endpoint)

        if resp.status_code != 200:
            #print ("None:","p2p.listener")
            return None

        return resp.text

def is_port_open(port):
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    location = ("127.0.0.1", port)
    result_of_check = a_socket.connect_ex(location)

    return result_of_check == 0

def _random_port():
    c_port = random.randint(8100,65535)
    while True:
        if not is_port_open(c_port):
            return c_port

PORT_CACHE = {}

class Simple(object):
    def on_get(self,req,resp):
        resp.status = falcon.HTTP_200
        resp.set_header("Access-Control-Allow-Origin",'*')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.body = "Hello World!"
        return

class NodeID(object):
    def on_get(self,req,resp,node_id):

        resp.status = falcon.HTTP_200
        resp.set_header("Access-Control-Allow-Origin",'*')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')

        raw = dht.findpeer(node_id)
        print (raw)
        j = json.loads("["+raw.split(node_id+"\",\"Addrs\":[")[1].split("]")[0]+"]")
        resp.body=json.dumps(j)
        return

class Ssh(object):
    def on_get(self,req,resp,node_id):
        resp.status = falcon.HTTP_200
        resp.set_header("Access-Control-Allow-Origin",'*')
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')

        if node_id in PORT_CACHE:
            PORT_CACHE[node_id]["port"]

        port = _random_port()
        raw = dht.forward("ipfs-ssh", "/ip4/0.0.0.0/tcp/"+str(port)+"/", "/p2p/"+node_id, allow_custom_protocol=True)
        print (raw)
        resp.body="ssh ubuntu@"+socket.gethostbyname(socket.gethostname()) + " -p "+str(port)
        return



App = falcon.App()

# Routes
simple = Simple()
node_id = NodeID()
ssh = Ssh()



#App.add_route('/simple',simple)
#App.add_route("/{node_id}",node_id)
#App.add_route("/p2p/{node_id}",node_id)
App.add_route("/ssh/{node_id}",ssh)

serve(App, host="0.0.0.0", port=80,threads=64)
