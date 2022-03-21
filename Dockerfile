# syntax=docker/dockerfile:1

FROM python:3.9.11-bullseye

WORKDIR /app

ENV LISTEN_PORT=5555
ENV RUNNER_TYPE="TFBertModelRunner"
ENV MODEL_URL="model/"
ENV BASE="bert-large-uncased-whole-word-masking-finetuned-squad"

COPY requirements.txt requirements.txt
RUN python -m pip install git+https://github.com/sweng480-team23/tqa-training-lib@main
RUN pip install -r requirements.txt

COPY . .

CMD python model_runner_server.py --port=${LISTEN_PORT} --type=${RUNNER_TYPE} --url=${MODEL_URL} --base=${BASE}