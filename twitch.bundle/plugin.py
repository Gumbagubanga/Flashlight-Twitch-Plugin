import twitch

def results(fields, original_query):
	if not '~channel' in fields:
		return

	channelName = fields['~channel']
	streamInfo = twitch.get_stream_info(channelName)

	if streamInfo is None:
		return

	displayName = streamInfo['channel']['display_name']

	return {
		"title": "Open Twitch channel of {0}".format(displayName),
		"run_args": [channelName]
	}

def run(channelName):
	from subprocess import call
	
	channelUrl = twitch.get_playlist(channelName)
	if not channelUrl:
		return
	
	application = "/Applications/QuickTime Player.app"

	call(["open", "-a", application, channelUrl])
