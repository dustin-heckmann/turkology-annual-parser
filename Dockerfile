FROM python:3.7

COPY turkology-annual-parser /turkology-annual-parser/
COPY Pipfile Pipfile.lock /
COPY go go.helpers /

RUN ./go build-docker
ENTRYPOINT ["./go", "run-docker"]
