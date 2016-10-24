from slackclient import SlackClient
from slacker import Slacker

SLACK_TOKEN = 'xoxp-4905231067-93860464293-93805900307-96bc401331d824a87395e3369f8970d1'
SLACK_WEBHOOK_SECRET = 'p6aMVuJpV7TUSXBQYxqPjesE'
slack_client = SlackClient(SLACK_TOKEN)

slack = Slacker(SLACK_TOKEN)

#Output for this:
# {
#   u'args': {u'token': u'xoxp-4905231067-93860464293-93805900307-96bc401331d824a87395e3369f8970d1'},
#   u'ok': True
# }
# print slack_client.api_call('api.test')

#Output for this:
# {
#   u'user_id': u'U2RRADN8M',
#   u'url': u'https://dev4slack.slack.com/',
#   u'team_id': u'T04SM6T1Z', u'user': u'bos-hieu',
#   u'team': u'Slack Developer Hangout',
#   u'ok': True
# }
# print slack_client.api_call("auth.test")

#list all channels
def list_channels():
  channels_call = slack_client.api_call('channels.list')
  if channels_call['ok']:
    return channels_call['channels']
  return None


#return info of channels
def channel_info(channel_id):
  channel_info = slack_client.api_call('channels.info', channel = channel_id)
  if channel_info:
    return channel_info['channel']
  return None


def send_message(channel_id, message):
  slack_client.api_call(
    "chat.postMessage",
    channel = channel_id,
    text = message,
    username='hieu-bot',
    icon_emoji=':robot_face:'
  )

if __name__ == '__main__':
  #channels = list_channels()
  #if channels:
    #print('Channels: ')
    #for channel in channels:
      #print (channel['name'] + ' (' + channel['id']+')')
      #detailed_info = channel_info(c['id'])
      #if detailed_info and detailed_info['is_member'] == True:
        #print (detailed_info)
      #if channel['name'] == 'random':
       # send_message(channel['id'],
    #                 "Hello " + channel['name'] + "! It worked!")
    #print ('-------------------')
  #else:
   # print ("Unable to authenticate")
  #print slack_client.api_call("api.test")
  #print slack_client.api_call('im.open', user="U2RRADN8M")
  #print slack_client.api_call('im.open', user="U2S9CL6LV")
  # if slack_client.rtm_connect():
  #   print slack_client.server.channels
  #   slack_client.rtm_send_message(channel='#general', message="Hello channel! I'm testing")
  print slack.channels.get_channel_id('general')
  print channel_info('C04SM6TAK')