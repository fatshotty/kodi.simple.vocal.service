import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "resources/lib")))

from resources.lib.messenger.socketclient import SockClient as SocketClient
from resources.lib.actions import execute

def onMessage(data):
    print(data['action'])
    print(data['name'])
    print(data['params'])
    
    print( execute(data) )


# socket_client = SocketClient( 'http://174.138.3.191:5002', onMessage, client_id = '/XXX-XXXX-XXX')
socket_client = SocketClient( 'http://127.0.0.1:5002', onMessage, client_id = '/XXX-XXXX-XXX')
print( socket_client.connect() )