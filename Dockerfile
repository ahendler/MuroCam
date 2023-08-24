FROM ubuntu:20.04

# install dependencies
RUN apt-get update && apt-get install -y python3 python3-pip

# copy files
WORKDIR /app
COPY src/ /app
COPY requirements.txt /app

RUN pip3 install -r requirements.txt
RUN pip3 install torch==1.9.0+cpu torchvision==0.10.0+cpu torchaudio==0.9.0 -f https://download.pytorch.org/whl/torch_stable.html
CMD python3 src/print.py