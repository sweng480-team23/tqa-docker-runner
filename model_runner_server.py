import argparse
import json
import signal
import zmq
from tqa_training_lib.model_runners.tf_bert_model_runner import TFBertModelRunner

parser = argparse.ArgumentParser()
parser.add_argument('--port', default=5555)
parser.add_argument('--type', default="TFBertModelRunner")
parser.add_argument('--url', default="model/")
parser.add_argument('--base', default="bert-large-uncased-whole-word-masking-finetuned-squad")
cmd_args = parser.parse_args()

print("**** Model Runner Server Starting Up ****")
print("Listen Port: " + str(cmd_args.port))
print("Runner Type: " + str(cmd_args.type))
print("Model Path: " + str(cmd_args.url))
print("Pretrained Base: " + str(cmd_args.base))

# this allows Ctrl+C to interrupt the socket wait and kill the process
signal.signal(signal.SIGINT, signal.SIG_DFL)

# todo: use factory to choose appropriate runner
runner = TFBertModelRunner(cmd_args.url, cmd_args.base)

context = zmq.Context()
socket = context.socket(zmq.REP)

socket.bind("tcp://*:" + str(cmd_args.port))

while True:
    print("Ready!")

    #  Wait for next request from client
    message = socket.recv()
    print(f"Received request: {message}")

    if message.decode("ascii") == "HELLO?":
        print("HELLO!")
        socket.send_string("HELLO!")
        continue

    try:
        tq = json.loads(message)
        ans, start, end = runner.answer_tweet_question(tq["tweet"], tq["question"])
        response_obj = {"answer": ans, "start_position": start, "end_position": end}
        socket.send_string(json.dumps(response_obj))
    except Exception:
        socket.send_string("BAD REQUEST")
