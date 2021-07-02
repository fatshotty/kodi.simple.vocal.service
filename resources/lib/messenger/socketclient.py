from resources.lib import socketio

TRANSPORT = 'websocket'

class SockClient():

    LOG_NAME = 'kodivocals'

    DEBUG = 2 # 0 = HIGH, 1 = MEDIUM, 2 = LOW lasciare a uno! (solo _log <= DEBUG vengono visualizzati)

    SocketIO = None

    _serverhost = None
    _client_id = None
    _onlog = None
    _onconnect = None
    _ondisconnect = None
    _onmessage = None

    def __init__(self, serverhost, onMessage, client_id=None, onConnect = None, onDisconnect=None, onLog = None):

        self._serverhost = serverhost
        self._client_id = client_id

        self._onlog = onLog

        self.reconnect_on_disconnect = True
        self.reconnect_on_error = True
        self.current_reconnection_times = 0

        self.SocketIO = socketio.Client(

            reconnection=True,
            reconnection_attempts=0,
            reconnection_delay=1,
            reconnection_delay_max=5,
            randomization_factor=0.5,
            logger=False
        )

        self._onconnect = onConnect
        self.SocketIO.on('connect', self._on_connect, namespace=self._client_id)
        
        self._ondisconnect = onDisconnect
        self.SocketIO.on('disconnect', self._on_disconnect, namespace=self._client_id)

        self._onmessage = onMessage
        self.SocketIO.on('message', self._got_message, namespace=self._client_id)
        self.SocketIO.on('data', self._got_message, namespace=self._client_id)


    def _log(self, str):
        if self._onlog:
            self._onlog(str)
        else:
            print(str)


    def connect(self):
        self._log('try to connect to {}'.format(self._serverhost) )

        url = self._serverhost
        # in alpha version just use the teamwatch feed

        print( self._client_id )

        return self.SocketIO.connect( url, transports=[TRANSPORT], namespaces = [self._client_id] )

    def disconnect(self):
        self._log('try to disconnect to {}'.format(self._serverhost) )
        self.SocketIO.disconnect()

    def wait_before_exit(self):
        self.SocketIO.wait()


    def _on_connect(self):
        self._log('socket connected: sid {}'.format(self.SocketIO.sid) )
        if self._onconnect:
            self._onconnect(self.SocketIO)

    def _on_disconnect(self):
        self._log('socket diconnected')
        if self._ondisconnect:
            self._ondisconnect(self.SocketIO)

    def _got_message(self, data):
        # parse message
        self._log( 'Got message: {}'.format(data) )

        self._onmessage( data )


    def remove_event_listeners(self):
        self._onlog = None
        self._onconnect = None
        self._ondisconnect = None
        self._onmessage = None
