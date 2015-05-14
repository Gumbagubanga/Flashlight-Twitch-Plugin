import twitch
import json

def prepareHtml(streamInfo):
	displayName = streamInfo['channel']['display_name']
	game = streamInfo['channel']['game']
	status = streamInfo['channel']['status']
	viewers = streamInfo['viewers']
	previewImage = streamInfo['preview']['template'].format(width=400, height=225)

	html = (u"{displayName} - {game} - {viewers} viewsers<br/><br/>"
		u"{status}<br/><br/>"
		"<img style='width: 100%;' src='{previewImage}'/>").format(displayName=displayName, game=game, status=status, viewers=viewers, previewImage=previewImage)
	return html

def results(fields, original_query):
	if not '~channel' in fields:
		return

	channelName = fields['~channel']
	streamInfo = twitch.get_stream_info(channelName)

	if streamInfo is None:
		return

	displayName = streamInfo['channel']['display_name']
	html = prepareHtml(streamInfo)

	return {
		"title": "Open Twitch channel of {0}".format(displayName),
		"run_args": [channelName],
		"webview_transparent_background": True,
		"html": html
	}

def run(channelName):
	from subprocess import call
	
	settings = json.load(open('preferences.json'))
	inBrowser = settings['inBrowser']

	if inBrowser:
		twitchUrl = "http://twitch.tv/{channelName}/".format(channelName=channelName)
		call(["open", twitchUrl])	
		return

	channelUrl = twitch.get_playlist(channelName)
	if not channelUrl:
		return
	
	application = settings['application']
	call(["open", "-a", application, channelUrl])
