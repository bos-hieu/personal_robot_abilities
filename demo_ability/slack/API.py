import json
import os
import time
from slackclient import SlackClient
from slacker import Slacker
from demo_ability.sdk.send_json import send_zmq

SLACK_BOT_TOKEN = 'xoxb-94318686709-NHZpp8Zhd7NzPEfIw87AqlU5'
BOT_NAME = 'hieu-bot'
BOT_ID = 'U2S9CL6LV'

client_id = "4905231067.94454686948"
client_secret = "b9be8ca7ea3cd26410c1208d74f74579"
code = "4905231067.95237492967.a09ae0c8d4"

#SLACK_TOKEN = 'xoxp-4905231067-93860464293-93805900307-96bc401331d824a87395e3369f8970d1'
SLACK_TOKEN = 'xoxp-4905231067-93860464293-95244030978-0ebd6a3ca5c24cf7e3a45deb5c9cf740'
SLACK_WEBHOOK_SECRET = 'p6aMVuJpV7TUSXBQYxqPjesE'

slack_client = SlackClient(SLACK_TOKEN)
slacker = Slacker(SLACK_TOKEN)
#slack_client = SlackClient(SLACK_BOT_TOKEN)


def get_user_info(user_id):
  api_call = slack_client.api_call('users.info', user=user_id)
  if api_call['ok']:
    return api_call['user']
  return None


def get_username(user_id):
  user_info = get_user_info(user_id)
  if user_info:
    return user_info['name']
  return None


def get_user_id(username):
  return slacker.users.get_user_id(username)


def is_member(username):
  api_call = slack_client.api_call('users.list')
  try:
    if api_call['ok']:
      users = api_call['members']
      for user in users:
        if 'name' in user and user['name'] == username:
          return  ("User ID for '" + user['name'] + "' is " + user.get('id'))

    return 'Not found username: %s' % username
  except Exception, e:
    print 'Find user error: %s' % e


def get_channels_of_user(username):
  pass


def get_channel_name(channel_id):
  api_call = slack_client.api_call('channels.info', channel=channel_id)
  if api_call['ok']:
    return api_call['channel']['name']
  else:
    api_call = slack_client.api_call('groups.info', channel=channel_id)
    if api_call['ok']:
      return api_call['group']['name']
  return None


def parse_slack_output(slack_rtm_output):
  output_list = slack_rtm_output
  print output_list
  if output_list and len(output_list) > 0:
    for output in output_list:
      if output and 'text' in output and 'type' in output and output['type'] == 'message':
        return output['text'],output['channel'], output['user']
  return None, None, None


def output(action):
  data = {"action":action, "value": ""}
  package = {"source": "", "data": json.dumps(data), "type": "t2s", "protocol": ""}
  send_zmq(json.dumps(package))


if __name__ == '__main__':
  # print get_user_info(BOT_ID)
  # print get_user_id("hieu-bot")
  # print get_username(BOT_ID)
  # channel_id = slacker.channels.get_channel_id('general')
  # print get_channel_name(channel_id)
  # print is_member('hieu-bt')
  #print get_channel_name('D2S9PV1K4')
  # print slack_client.api_call('groups.info', channel='G2T4D9R28')

  this_user_id =''
  api_call = slack_client.api_call('auth.test')
  print api_call
  if api_call['ok']:
    this_user_id = api_call['user_id']


  READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
  if slack_client.rtm_connect():
    print("StarterBot connected and running!")
    while True:
      message, channel_id, user_id = parse_slack_output(slack_client.rtm_read())

      #Get channel_name, username from channel_id, user_id
      channel_name = get_channel_name(channel_id)
      username = get_username(user_id)

      if message and user_id != this_user_id:
        if channel_name:
          title = 'New message from user %s on channel %s' % (username, channel_name)
        else:
          title = 'New message from user %s' % username

        data = {"action": "new message", "value": (title, message)}
        package = {"type": "t2s", "data": json.dumps(data), "source": "", "protocol": ""}
        send_zmq(json.dumps(package))
        print package
        #if channel_id:
         #slack_client.rtm_send_message(channel=channel_id, message='Reply: ' + message)
      time.sleep(READ_WEBSOCKET_DELAY)
  else:
    print("Connection failed. Invalid Slack token or bot ID?")

  #slack_client.api_call('reminders.add', text='For testing reminders', time=10)
  #api_call = slack_client.api_call('auth.test')
  # print api_call
  #api_call =slack_client.api_call('oauth.access', client_id = client_id, client_secret=client_secret, code=code)
  #api_call =slack_client.api_call('channels.list')
  #print api_call
  # if api_call['ok']:
  #   reminders = api_call['reminders']
  #   for reminder in reminders:
  #     slack_client.api_call('reminders.delete', reminder=reminder['id'])
  # print api_call