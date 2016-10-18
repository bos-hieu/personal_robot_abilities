#!/usr/bin/env python

import json
from sdk.actions import ANIMATION_ACTIONS
from sdk import send_json

data_send = {"action": ANIMATION_ACTIONS.SMILE, "value": ""}

#send data to brain:
package = {"type": "animation", "data": json.dumps(data_send), "source": "", "protocol": ""}
send_json.send_zmq(json.dumps(package))