FROM pytorch/pytorch:1.5.1-cuda10.1-cudnn7-runtime

VOLUME /mnt/input
VOLUME /mnt/output

# Install system dependencies
RUN apt-get update -y \
        && apt-get install -y git curl

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
