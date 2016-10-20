import json
import argparse

from demo_ability.sdk.send_json import send_zmq
from demo_ability.sdk.actions import ANIMATION_ACTIONS

#data_send = {"action": ANIMATION_ACTIONS.SMILE, "value": ""}

def output(action):
  data = {"action":action, "value": ""}
  package = {"source": "", "data": json.dumps(data), "type": "t2s", "protocol": ""}
  send_zmq(json.dumps(package))

if __name__ == '__main__':

  parser = argparse.ArgumentParser()
  parser.add_argument('-d', '-data', help='data', required=False)
  parser.add_argument('-a', '-action', help='action', required=True)
  parser.add_argument('-s', '-source', help='source', required=False)
  parser.add_argument('-p', '-protocol', help='protocol', required=False)

  args = parser.parse_args()
  #action = json.loads(args.a)
  action = args.a

  if hasattr(ANIMATION_ACTIONS, action):
    output(action)