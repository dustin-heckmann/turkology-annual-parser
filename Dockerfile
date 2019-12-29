FROM python:3.7

COPY turkology-annual-parser /turkology-annual-parser/
COPY requirements.txt /
COPY data /data/
COPY run.sh /

RUN pip install -r requirements.txt
ENTRYPOINT ["./run.sh"]
