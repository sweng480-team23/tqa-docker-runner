import argparse
from tqa_training_lib.model_runners.tf_bert_model_runner import TFBertModelRunner
from flask import Flask
from flask import request

parser = argparse.ArgumentParser()
parser.add_argument('--type', default="TFBertModelRunner")
parser.add_argument('--url', default="model/")
parser.add_argument('--base', default="bert-large-uncased-whole-word-masking-finetuned-squad")
cmd_args = parser.parse_args()

print("**** Model Runner Server Starting Up ****")
print("Runner Type: " + str(cmd_args.type))
print("Model Path: " + str(cmd_args.url))
print("Pretrained Base: " + str(cmd_args.base))

app = Flask(__name__)

# todo: use factory to choose appropriate runner
runner = TFBertModelRunner(cmd_args.url, cmd_args.base)


@app.route('/', methods=['GET'])
def root():
    return "The model runner service is running", 200


@app.route('/', methods=['POST'])
def run_pipeline():
    tq: dict = request.get_json()
    ans, start, end = runner.answer_tweet_question(tq["tweet"], tq["question"])
    response_obj = {"answer": ans, "start_position": start, "end_position": end}
    return response_obj, 200


if __name__ == "__main__":
    app.run()
