#FROM nvidia/cuda:11.3.1-base-ubuntu20.04
FROM python:3.9

COPY /src /src
COPY .env .
COPY languages.json .
COPY requirements.txt .

RUN apt-get update -y
#RUN apt-get install -y python3.9
RUN apt-get -y install git
RUN apt-get -y install pip
RUN apt-get install ffmpeg libsm6 libxext6 -y
RUN pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cpu

RUN pip install -r requirements.txt

CMD ["python3", "src/run_speech.py"]