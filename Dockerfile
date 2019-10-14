FROM python:3.6

VOLUME /mnt/input
VOLUME /mnt/output

RUN pip install foolbox
RUN pip install Pillow
RUN pip install tensorflow

COPY . /app
WORKDIR /app

CMD ["sh", "run.sh"]
