FROM python:2.7
MAINTAINER Ryan Grieve <me@ryangrieve.com>

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

ADD ./app /app

WORKDIR /app

CMD ["python", "run.py"]

EXPOSE 5000
