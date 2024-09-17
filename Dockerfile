FROM python:3.10

LABEL "channel"="TEST"
LABEL "Creator"="TEST-TEST"

WORKDIR ./usr/stable
COPY . .

RUN pip3 install -r requirements.txt
RUN playwright install firefox
RUN playwright install-deps
