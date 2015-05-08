def get_signature_and_token(channelName):
	import json
	import httplib
	
	conn = httplib.HTTPConnection('api.twitch.tv')
	conn.request('GET', '/api/channels/{channelName}/access_token'.format(channelName=channelName))
	resp = conn.getresponse()

	if not resp.status is 200:
		return None, None

	tokenJson = json.load(resp)
	conn.close()
	return tokenJson['sig'], tokenJson['token']

def check_if_live(channelName, sig, token):
	import httplib

	channelHost = 'usher.twitch.tv'
	channelPath = '/api/channel/hls/{channelName}.m3u8?sig={sig}&token={token}'.format(channelName=channelName, sig=sig, token=token)

	channelUrl = 'http://' + channelHost + channelPath

	return {
		"title": "Open Twitch channel of {0}".format(channelName),
		"run_args": [channelUrl]
	}

def results(fields, original_query):
	if not '~channel' in fields:
		return

	channelName = fields['~channel']
	
	sig, token = get_signature_and_token(channelName)

	if sig is None and token is None:
		return

	return check_if_live(channelName, sig, token)

def run(channelUrl):
	from subprocess import call
	
	supportedPlayers = { "VLC": "/Applications/VLC.app", "QT": "/Applications/QuickTime Player.app" }
	application = supportedPlayers["QT"]

	call(["open", "-a", application, channelUrl])
