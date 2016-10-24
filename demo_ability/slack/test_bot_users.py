import os
import time
from slackclient import SlackClient


SLACK_BOT_TOKEN = 'xoxb-94318686709-NHZpp8Zhd7NzPEfIw87AqlU5'
BOT_NAME = 'hieu-bot'
BOT_ID = 'U2S9CL6LV'

AT_BOT = "<@" + BOT_ID + ">:"
EXAMPLE_COMMAND = 'do'

slack_client = SlackClient(SLACK_BOT_TOKEN)

def is_member():
  api_call = slack_client.api_call("users.list")
  if api_call.get('ok'):
    # retrieve all users so we can find our bot
    users = api_call.get('members')
    for user in users:
      if 'name' in user and user.get('name') == BOT_NAME:
        print("Bot ID for '" + user['name'] + "' is " + user.get('id'))
  else:
    print("could not find bot user with the name " + BOT_NAME)

def handle_command(command, channel):
  """
      Receives commands directed at the bot and determines if they
      are valid commands. If so, then acts on the commands. If not,
      returns back what it needs for clarification.
  """
  response = "Not sure what you mean. Use the *" + EXAMPLE_COMMAND + \
               "* command with numbers, delimited by spaces."
  if command.startswith(EXAMPLE_COMMAND):
    response = "Sure...write some more code then I can do that!"
  slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
  """
      The Slack Real Time Messaging API is an events firehose.
      this parsing function returns None unless a message is
      directed at the Bot, based on its ID.
  """
  output_list = slack_rtm_output
  print output_list
  if output_list and len(output_list) > 0:
    for output in output_list:
      if output and 'text' in output:
        # return text after the @ mention, whitespace removed
        return output['text'], \
               output['channel']
  return None, None


if __name__ == "__main__":
  # READ_WEBSOCKET_DELAY = 1  # 1 second delay between reading from firehose
  # if slack_client.rtm_connect():
  #   print("StarterBot connected and running!")
  #   while True:
  #      command, channel = parse_slack_output(slack_client.rtm_read())
  #      print command, channel
  #      if command and channel:
  #        handle_command(command, channel)
  #      print slack_client.rtm_read()
       # time.sleep(READ_WEBSOCKET_DELAY)
  # else:
  #   print("Connection failed. Invalid Slack token or bot ID?")
  print slack_client.api_call('groups.list')