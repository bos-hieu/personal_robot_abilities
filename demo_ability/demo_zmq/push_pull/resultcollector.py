import time
import zmq
import pprint

def result_collector():
  context = zmq.Context()

  result_receiver = context.socket(zmq.PULL)
  result_receiver.bind("tcp://127.0.0.1:5558")

  collector_data = {}
  for x in xrange(1000):
    result = result_receiver.recv_json()
    if collector_data.has_key(result['consumer']):
      collector_data[result['consumer']] = collector_data[result['consumer']] + 1
    else:
      collector_data[result['consumer']] = 1
    if x == 999:
      pprint.pprint(collector_data)


result_collector()