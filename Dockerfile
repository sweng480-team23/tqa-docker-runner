# syntax=docker/dockerfile:1

FROM python:3.9.11-bullseye

WORKDIR /app

ENV RUNNER_TYPE="TFBertModelRunner"
ENV MODEL_URL="model/"
ENV BASE="bert-large-uncased-whole-word-masking-finetuned-squad"

COPY requirements.txt requirements.txt
RUN python -m pip install git+https://github.com/sweng480-team23/tqa-training-lib@main
RUN pip install -r requirements.txt

COPY . .

EXPOSE ${LISTEN_PORT}

CMD python app.py --type=${RUNNER_TYPE} --url=${MODEL_URL} --base=${BASE}