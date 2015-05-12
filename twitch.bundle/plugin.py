import twitch

def results(fields, original_query):
	if not '~channel' in fields:
		return

	channelName = fields['~channel']
	if not twitch.is_live(channelName):
		return

	return {
		"title": "Open Twitch channel of {0}".format(channelName),
		"run_args": [channelName]
	}

def run(channelName):
	from subprocess import call
	
	channelUrl = twitch.get_playlist(channelName)
	if not channelUrl:
		return
	
	application = "/Applications/QuickTime Player.app"

	call(["open", "-a", application, channelUrl])
