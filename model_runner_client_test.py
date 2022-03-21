
import argparse
import json
import signal
import zmq

parser = argparse.ArgumentParser()
parser.add_argument('--port', default=5555)
parser.add_argument('--msg', default=None)
parser.add_argument('--tweet', default="George W. Bush and Bill Clinton visited a Ukrainian church in Chicago to show solidarity with the people of Ukraine.")
parser.add_argument('--question', default="Where is the Ukrainian church?")
cmd_args = parser.parse_args()

# this allows Ctrl+C to interrupt the socket wait and kill the process
signal.signal(signal.SIGINT, signal.SIG_DFL)

context = zmq.Context()

#  Socket to talk to server
print("Connecting to model runner server on port " + str(cmd_args.port) + "...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:" + str(cmd_args.port))

if cmd_args.msg is not None:
    req_str = cmd_args.msg
else:
    req_obj = {
        "tweet": cmd_args.tweet,
        "question": cmd_args.question,
    }

    req_str = json.dumps(req_obj)

print(f"Sending request {req_str} ...")
socket.send_string(req_str)

#  Get the reply.
message = socket.recv()
print(f"Received reply {message}")
