# -*- coding: utf-8 -*-

from resources.lib import kodiutils
from resources.lib import kodilogging
from resources.lib.messenger.socketclient import SockClient as SocketClient
import logging
import time
import xbmc
import xbmcaddon
from resources.lib.actions import execute



ADDON = xbmcaddon.Addon()
logger = logging.getLogger(ADDON.getAddonInfo('id'))


def onMessage(data):
    logger.info('received remote action: {}', data)
    result = execute(data)
    if result:
        header = kodiutils.get_string(32000)
        kodiutils.notification(header, data['responseText'], sound=(data['action'] == 'input_unknown'))
    else:
        logger.warn('Cannot execute action')

def onConnect(sio):
    header = kodiutils.get_string(32000)
    message = kodiutils.get_string(32003)
    kodiutils.notification(header, message, sound=False)

def onDisconnect(sio):
    header = kodiutils.get_string(32000)
    message = kodiutils.get_string(32004)
    kodiutils.notification(header, message, sound=False)


def onLog(str):
    logger.info( str )


def generate_uuid():
    import random, string
    # TODO: generate a new UUID for connecting to a server channel
    ts = str( time.time() )
    last_ts = ts[-3:]
    code = "{}{}{}-{}{}{}{}-{}".format(
        random.choice(string.ascii_letters).upper(),
        random.choice(string.ascii_letters).upper(),
        random.choice(string.ascii_letters).upper(),
        random.choice(string.ascii_letters).upper(),
        random.choice(string.ascii_letters).upper(),
        random.choice(string.ascii_letters).upper(),
        random.choice(string.ascii_letters).upper(),
        last_ts
    )
    return code



def run():
    monitor = xbmc.Monitor()

    socket_client = None

    logger.info("Starting! %s" % time.time() )

    client_id = kodiutils.get_setting('client_id')
    serverhost = kodiutils.get_setting("server_host")

    if not client_id:
        logger.info("No client_id found, generate a new one!" )
        # generate a new client_id
        client_id = generate_uuid()
        kodiutils.set_setting('client_id', client_id)
        logger.info("New client_id is ".format(client_id) )

    logger.info("clientid {} and host {}".format(client_id, serverhost) )
    

    logger.info("Try to connect..." )
    socket_client = SocketClient( serverhost, onMessage, client_id = '/{}'.format(client_id), onLog = onLog, onConnect=onConnect, onDisconnect=onDisconnect)
    socket_client.connect()

    logger.info("connection established" )

    # TODO: show notification for connection

    while not monitor.abortRequested():
        # Sleep/wait for abort for 5 seconds
        if monitor.waitForAbort(5):
            # Abort was requested while waiting. We should exit
            break
    
    logger.info("...going to disconnect and exit" )
    socket_client.remove_event_listeners()
    socket_client.disconnect()
