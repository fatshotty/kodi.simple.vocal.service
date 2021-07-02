from resources.lib import kodiutils

def execute(data):
    action = data['action']
    name = data['name']
    params = data['params']
    text = data['question']

    responseText = data['responseText']

    if action == 'pvr_actions':
        return pvr_actions(name, params, text)
    
    elif action == 'base_navigation':
        return base_navigation(name, params, text)
    
    elif action == 'base_commands':
        return base_commands(name, params, text)
    
    elif action == 'change_volume':
        return change_volume(name, params, text)
    
    elif action == 'input_sorry':
        return input_sorry(name, params, text)
    

    return input_unknown(name, params, text)




def pvr_actions(name, params, text = None):
    requested_channel = params['channel']

    number = None

    try:
        number = int(requested_channel)
    except:
        # no error management is required
        pass

    channel_list = kodiutils.kodi_json_request( {"jsonrpc": "2.0", "method": "PVR.GetChannels", "params": {"channelgroupid": 'alltv', "properties": [
        "channeltype",
        "channel",
        "uniqueid",
        "channelnumber"
    ]}, "id": 1} )

    channel_list = channel_list['channels']

    channel_to_play = None

    if number:
        for channel in channel_list:
            if number == channel['channelnumber']:
                channel_to_play = channel
                break
    else:
        for channel in channel_list:
            if requested_channel.lower() == channel['channel'].lower():
                channel_to_play = channel
                break

    if channel_to_play:
        res = kodiutils.kodi_json_request( {"jsonrpc": "2.0", "method": "Player.Open", "params": {"item": {"channelid": channel_to_play['channelid']} } } )
        return True

    return False

def base_navigation(name, params, text = None):
    pass



def base_commands(name, params, text = None):

    command = params['command']

    if name == 'player_commands':

        if command in ['pause', 'pausa', 'play', 'stop']:
            resp = kodiutils.kodi_json_request( {"jsonrpc": "2.0", "method": "Player.GetActivePlayers", "id": 1} )

            if len(resp) <= 0:
                return False
            
            for player in resp:

                c = None

                if 'paus' in command:
                    c = {"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": player['playerid'], "play": False }, "id": 1}
                
                elif command == 'play':
                    c = {"jsonrpc": "2.0", "method": "Player.PlayPause", "params": { "playerid": player['playerid'], "play": True }, "id": 1}
                
                elif command == 'stop':
                    c = {"jsonrpc": "2.0", "method": "Player.Stop", "params": { "playerid": player['playerid'] }, "id": 1}

                if c:
                    kodiutils.kodi_json_request( c )
        
            return True
    
    return False


def change_volume(name, params, text = None):
    # kodiutils.debugger()
    data_volume = kodiutils.kodi_json_request( {"jsonrpc": "2.0", "method": "Application.GetProperties", "params": {"properties": ["volume"]}, "id": 1} )
    volume = data_volume['volume']

    action = params['action']
    value = params['volume']

    if value:
        value = int(value)
        if value > 100: value=100
        if value < 0 : value = 0
        resp = kodiutils.kodi_json_request( {"jsonrpc": "2.0", "method": "Application.SetVolume", "params": {"volume": value}, "id": 1} )
        return True

    elif action:
        if action == 'abbassa':

            value = volume / 2
            
        elif action == 'alza':

            value = volume * 2
        
        params['volume'] = value
        
        return change_volume(name, params, text)

    elif 'mut' in text:
        # set/unset mute
        kodiutils.kodi_json_request( {"jsonrpc": "2.0", "method": "Application.SetMute", "params": {"mute": "toggle"}, "id": 1} )
        return True
    
    return False



def input_sorry(name, params, text = None):
    pass



def input_unknown(name, params, text = None):
    # returns True in order to show text notification
    return True