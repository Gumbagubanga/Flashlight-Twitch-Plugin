import json

def get_response_for(path, secure):
	import httplib

	host = 'api.twitch.tv'
	conn = httplib.HTTPSConnection(host) if secure else httplib.HTTPConnection(host)
	conn.request('GET', path)
	resp = conn.getresponse()
	data = resp.read()
	conn.close()

	return data if resp.status is 200 else None

def get_stream_info(channelName):
	path = '/kraken/streams/{channelName}'.format(channelName=channelName)
	resp = get_response_for(path, True)

	if resp is None:
		return None

	return json.loads(resp)['stream']

def get_signature_and_token(channelName):
	path = '/api/channels/{channelName}/access_token'.format(channelName=channelName)
	resp = get_response_for(path, False)

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