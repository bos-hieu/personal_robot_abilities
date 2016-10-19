import zmq

context = zmq.Context()
result_receiver = context.socket(zmq.PULL)
result_receiver.bind('tcp://127.0.0.1:1112')
while True:
  result = result_receiver.recv_string()
  print result