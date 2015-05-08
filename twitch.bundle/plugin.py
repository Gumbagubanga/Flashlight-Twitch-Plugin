def get_response_for(host, path, secure):
	import httplib

	conn = httplib.HTTPSConnection(host) if secure else httplib.HTTPConnection(host)
	conn.request('GET', path)
	resp = conn.getresponse()
	data = resp.read()
	conn.close()

	return data if resp.status is 200 else None

def is_live(channelName):
	import json

	host = 'api.twitch.tv'
	path = '/kraken/streams/{channelName}'.format(channelName=channelName)
	resp = get_response_for(host, path, True)

	if resp is None:
		return False

	return json.loads(resp)['stream'] is not None

def get_signature_and_token(channelName):
	import json
	
	host = 'api.twitch.tv'
	path = '/api/channels/{channelName}/access_token'.format(channelName=channelName)
	resp = get_response_for(host, path, False)

	if resp is None:
		return None, None

	tokenJson = json.loads(resp)
	return tokenJson['sig'], tokenJson['token']

def get_playlist(channelName):
	sig, token = get_signature_and_token(channelName)

	if sig is None and token is None:
		return

	host = 'usher.twitch.tv'
	path = '/api/channel/hls/{channelName}.m3u8?sig={sig}&token={token}'.format(channelName=channelName, sig=sig, token=token)

	url = 'http://' + host + path

	return url

def results(fields, original_query):
	if not '~channel' in fields:
		return

	channelName = fields['~channel']
	if not is_live(channelName):
		return

	channelUrl = get_playlist(channelName)
	if not channelUrl:
		return

	return {
		"title": "Open Twitch channel of {0}".format(channelName),
		"run_args": [channelUrl]
	}

def run(channelUrl):
	from subprocess import call
	
	supportedPlayers = { "VLC": "/Applications/VLC.app", "QT": "/Applications/QuickTime Player.app" }
	application = supportedPlayers["QT"]

	call(["open", "-a", application, channelUrl])
