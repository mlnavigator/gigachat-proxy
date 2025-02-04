FROM python:3.11-slim
LABEL authors="mlnavigator"

ADD . /proxy-app

RUN python3 -m pip install -r /proxy-app/requirements.txt
EXPOSE 8078

ENTRYPOINT ["/usr/local/bin/python3", "/proxy-app/app.py"]
