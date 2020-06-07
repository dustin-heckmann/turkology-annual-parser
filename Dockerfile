FROM python:3.8

COPY turkology-annual-parser /turkology-annual-parser/
COPY Pipfile.lock /
COPY Pipfile /
COPY go /

RUN ./go build-docker
ENTRYPOINT ["./go", "run-docker"]
