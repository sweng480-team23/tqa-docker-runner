from tqa_training_lib.model_runners.tf_bert_model_runner import TFBertModelRunner
from flask import Flask
from flask import request
from decouple import config
import logging

# parser = argparse.ArgumentParser()
# parser.add_argument('--port', default=5555)
# parser.add_argument('--type', default="TFBertModelRunner")
# parser.add_argument('--url', default="model/")
# parser.add_argument('--base', default="bert-large-uncased-whole-word-masking-finetuned-squad")
# cmd_args = parser.parse_args()

app = Flask(__name__)

port = config("LISTEN_PORT")
runner_type = config("RUNNER_TYPE")
model_url = config("MODEL_URL")
base = config("BASE")

print("**** Model Runner Server Starting Up ****")
print("Runner Type: " + runner_type)
print("Model Path: " + model_url)
print("Pretrained Base: " + base)

# todo: use factory to choose appropriate runner
runner = TFBertModelRunner(model_url, base)


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
    app.run("0.0.0.0", port=port)
else:
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
