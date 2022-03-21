# TweetQA Docker Runner

The purpose of this program is to run as a Docker container in which a microservice runs to serve tweet-question answers from a chosen model and model runner.

## Local testing

To test locally, simply run in two separate processes the following commands. Make sure you have weights files in the `model/` directory first. Make sure the port arguments are the same (or omit the port argument for both to run on 5555 by default).

```bash
python model_runner_server.py
```

```bash
python model_runner_client.py
```

Available command line arguments and their defaults:

```
--port=5555
--type="TFBertModelRunner" (server only)
--url="model/" (server only)
--base="bert-large-uncased-whole-word-masking-finetuned-squad" (server only)
--tweet="George W. Bush and Bill Clinton visited a Ukrainian church in Chicago to show solidarity with the people of Ukraine." (client only)
--question="Where is the Ukrainian church?" (client only)
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

Rebuild the image anytime you make a change to the Dockerfile or model_runner_server.py

## Running the container

After building the image, run the container using the following command. Replace the environment variable values as needed. What's shown below are defaults if omitted. See the Dockerfile annd model_runner_server.py for all available environment variables / command line arguments.

```bash
docker run --expose=5555 -e LISTEN_PORT=5555 -e RUNNER_TYPE="TFBertModelRunner" -e MODEL_URL="model/" -e BASE="bert-large-uncased-whole-word-masking-finetuned-squad" -e MODEL_URL="model/" <tag>
```

## Request Formats

The server accepts two types of requests:

- A simple "HELLO?" string request should be met with a "HELLO!" response. This can be used to confirm the server is alive and well.
- An dict converted to a json string with key names "tweet" and "question" will be accepted as a request to run those corresponding values through the model runner.
  - The response will be a dict formatted as a json string with key names "answer", "start_position", and "end_position"

## Todo

- Switch to poller for server
- Add timeout to client test
- Stop container after x minutes? Or is this configurable in GCP?
- Push image to Dockerhub
- Finish writing todo list
