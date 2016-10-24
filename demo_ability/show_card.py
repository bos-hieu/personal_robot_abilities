#!/usr/bin/env python
from sdk import send_json
import json


title = "hello world"
description = "This is a personal robot."
local_image_path = ""

data = {"action": "SHOW_CARD", "value": (title, description, local_image_path)}

#send data to brain:
package = {"type": "animation", "data": json.dumps(data), "source": "", "protocol": ""}
send_json.send_zmq(json.dumps(package))