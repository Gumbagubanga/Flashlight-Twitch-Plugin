def results(fields, original_query):
	import twitch

	if not '~channel' in fields:
		return

	channelName = fields['~channel']
	if not twitch.is_live(channelName):
		return

	channelUrl = twitch.get_playlist(channelName)
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
