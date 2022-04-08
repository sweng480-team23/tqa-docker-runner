# TweetQA Docker Runner

The purpose of this program is to run as a Docker container in which a microservice runs to serve tweet-question answers from a chosen model and model runner.

## Local testing

To test locally, simply run `app.py`. Make sure you have weights files in the `model/` directory first.

Available command line arguments and their defaults:

```
--type="TFBertModelRunner" (this currently does nothing, see todo list below)
--url="model/"
--base="bert-large-uncased-whole-word-masking-finetuned-squad"
```

## Building the image

Run the following command:

```bash
docker build . --tag <tag>
```

where \<tag\> is your repo name. For example:

```bash
docker build . --tag lwestfall:tqa-docker-runner
```

Rebuild the image anytime you make a change to the Dockerfile or app.py

## Request Formats

- A dict converted to a json string with key names "tweet" and "question" will be accepted as a request to run those corresponding values through the model runner.
  - The response will be a dict formatted as a json string with key names "answer", "start_position", and "end_position"

## Todo

- Switch to poller for server
- Add timeout to client test
- Actually instantiate the model runner from cmd_args.type
- Stop container after x minutes? Or is this configurable in GCP?
- Push image to Dockerhub
- Finish writing todo list
