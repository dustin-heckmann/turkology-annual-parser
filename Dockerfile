FROM python:3.7

COPY turkology-annual-parser /turkology-annual-parser/
COPY requirements.txt /
COPY data /data/
COPY install.sh /
COPY run.sh /

RUN ./install.sh
ENTRYPOINT ["./run.sh"]
