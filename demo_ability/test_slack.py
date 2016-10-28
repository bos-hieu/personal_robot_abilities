import argparse
import json
import time
from slackclient import SlackClient
from sdk.send_json import send_zmq

SLACK_BOT_TOKEN = 'xoxb-94318686709-NHZpp8Zhd7NzPEfIw87AqlU5'
BOT_NAME = 'hieu-bot'
BOT_ID = 'U2S9CL6LV'


# For team https://dev4slack.slack.com
#client_id = "4905231067.94454686948"
#client_secret = "b9be8ca7ea3cd26410c1208d74f74579"
#code = "4905231067.95237492967.a09ae0c8d4"

#for team  testingslackapigroup.slack.com
client_id =  '96331862466.96266010563'
client_secret = '15e6151e1c321aa36927cc17f14d4bba'
redirect_uri= 'https://slack.com/oauth/authorize?complete'
code = '96839134117.96870773271.119aa669ce'

#SLACK_TOKEN = 'xoxp-4905231067-93860464293-93805900307-96bc401331d824a87395e3369f8970d1'
#SLACK_TOKEN = 'xoxp-4905231067-93860464293-95244030978-0ebd6a3ca5c24cf7e3a45deb5c9cf740'
#SLACK_TOKEN = 'xoxp-96331862466-96316368960-96863481522-1f3059a8daaae6c604bda19a5363dd6f'
SLACK_TOKEN = 'xoxp-96839134117-96781460755-96808999827-03dd8f5adeeee32367eeaa036bf834e4'
SLACK_WEBHOOK_SECRET = 'p6aMVuJpV7TUSXBQYxqPjesE'

#TODO: Add error handling
class MySlackClient(SlackClient):
  def __init__(self, token):
    super(MySlackClient, self).__init__(token)

  def get_user_info(self, user_id):
    api_call = self.api_call('users.info', user=user_id)
    if api_call['ok']:
      return api_call['user']
    return None

  def get_username(self, user_id):
    user_info = self.get_user_info(user_id)
    if user_info:
      return user_info['name']
    return None

  def get_user_id(self, username):
    #return slacker.users.get_user_id(username)
    pass

  def is_member(self, username):
    api_call = self.api_call('users.list')
    try:
      if api_call['ok']:
        users = api_call['members']
        for user in users:
          if 'name' in user and user['name'] == username:
            return  ("User ID for '" + user['name'] + "' is " + user.get('id'))

      return 'Not found username: %s' % username
    except Exception, e:
      print 'Find user error: %s' % e

  #Get all groups of this user (private channel)
  def get_user_groups(self):
    api_call = self.api_call('groups.list')
    if api_call['ok']:
      return api_call['groups']

  #Get all channel of this user (public channel)
  def get_user_channels(self):
    try:
      #List to store all channels of this user
      user_channels = []

      #Get all public channels of this user
      api_call = self.api_call('channels.list')
      if api_call['ok']:
        channels = api_call['channels']
        for channel in channels:
          if channel['is_member']:
            user_channels.append(channel)
        print len(user_channels)

    except Exception, e:
      print 'Get channels error: %s' % e

  def get_channel_name(self, channel_id):
    api_call = self.api_call('channels.info', channel=channel_id)
    if api_call['ok']:
      return api_call['channel']['name']
    else:
      api_call = self.api_call('groups.info', channel=channel_id)
      if api_call['ok']:
        return api_call['group']['name']
    return None

  @staticmethod
  def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the user, based on its ID.
    """
    output_list = slack_rtm_output
    print output_list
    if output_list and len(output_list) > 0:
      for output in output_list:
        if output and 'text' in output and 'type' in output and output['type'] == 'message' and 'user' in output:
          return output['text'],output['channel'], output['user']
    return None, None, None


  def get_this_user_id(self):
    this_user_id = None
    api_call = self.api_call('auth.test')
    if api_call['ok']:
      this_user_id = api_call['user_id']
    return this_user_id

  def get_notification(self):
    message, channel_id, user_id = MySlackClient.parse_slack_output(self.rtm_read())

    # Get channel_name, username from channel_id, user_id
    channel_name = self.get_channel_name(channel_id)
    username = self.get_username(user_id)
    this_user_id = self.get_this_user_id()

    if message and user_id != this_user_id:
      if channel_name:
        title = 'New message from user %s on channel %s' % (username, channel_name)
      else:
        title = 'New message from user %s' % username

      output(title, message)

  def push_notifications(self):
    READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
    if self.rtm_connect():
      print("StarterBot connected and running!")
      while True:
        self.get_notification()
        time.sleep(READ_WEBSOCKET_DELAY)
    else:
      print("Connection failed. Invalid Slack token or bot ID?")

  def remider_add(self, text, time):
    self.api_call('reminders.add', text=text, time=time)

  def remider_delete(self, reminder_id):
    self.api_call('reminders.delete', reminder = reminder_id)

  def post_message(self, channel_id, message, username, icon_emoji=None):
    self.api_call(
      "chat.postMessage",
      channel=channel_id,
      text=message,
      username=username,
      icon_emoji= icon_emoji or ''
    )

  def post_rtm_message(self,channel_id, message):
    self.rtm_send_message(channel_id, message)


def output(title, message):
  data = {"action":"Push Notifications Slack", "value": (title, message)}
  package = {"source": "", "data": json.dumps(data), "type": "t2s", "protocol": ""}
  send_zmq(json.dumps(package))


#TODO: write function to get code auth and access token
if __name__ == '__main__':
  parser = argparse.ArgumentParser()

  parser.add_argument('-d', '-data', help='data', required=True)
  parser.add_argument('-a', '-action', help='action', required=True)
  parser.add_argument('-p', '-protocol', help='protocol')

  args = parser.parse_args()
  message = args.d

  slack_api = MySlackClient(SLACK_TOKEN)
  #slack_api.push_notifications()
  slack_api.remider_add(text=message, time='in 5 minutes')
  print args