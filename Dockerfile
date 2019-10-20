FROM pytorch/pytorch

VOLUME /mnt/input
VOLUME /mnt/output

# Install python dependencies
RUN pip install Pillow numpy foolbox

# Download pretrained weights
ADD models.py /
RUN python /models.py 

COPY . /app
WORKDIR /app

CMD ["sh", "run.sh"]
