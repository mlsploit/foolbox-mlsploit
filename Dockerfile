FROM python:3.6

VOLUME /mnt/input
VOLUME /mnt/output

RUN pip install foolbox
RUN pip install Pillow

COPY . /app
WORKDIR /app

CMD ["sh", "run.sh"]
