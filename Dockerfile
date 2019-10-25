FROM pytorch/pytorch

VOLUME /mnt/input
VOLUME /mnt/output

# Install python dependencies
RUN pip install Pillow numpy foolbox==1.8.0

# Download pretrained weights
ADD models.py /
RUN python /models.py

COPY . /app
WORKDIR /app

CMD ["sh", "run.sh"]
