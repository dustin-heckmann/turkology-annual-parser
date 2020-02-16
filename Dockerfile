FROM python:3.7

COPY turkology-annual-parser /turkology-annual-parser/
COPY requirements.txt /
COPY data /data/
COPY go /

RUN ./go build-docker
ENTRYPOINT ["./go run-docker"]
