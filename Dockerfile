FROM python:3.6-alpine

VOLUME /mnt/input
VOLUME /mnt/output

RUN pip install foolbox

COPY . /app
WORKDIR /app

CMD ["sh", "run.sh"]
