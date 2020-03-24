FROM pytorch/pytorch

VOLUME /mnt/input
VOLUME /mnt/output

# Install python dependencies
COPY requirements.txt /
RUN pip install --ignore-installed \
        -r /requirements.txt

# Download pretrained weights
COPY models.py /
RUN python /models.py

COPY . /app
WORKDIR /app

CMD ["sh", "run.sh"]
