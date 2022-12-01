FROM nvidia/cuda:11.3.1-base-ubuntu20.04

RUN apt-get update -y
RUN apt-get install -y python3.9
RUN apt-get -y install git
RUN apt-get -y install pip
RUN apt-get install ffmpeg libsm6 libxext6 -y

COPY src/ /workdir/
RUN ls --recursive /workdir/
COPY test_files/ /workdir/
RUN ls --recursive /workdir/
COPY .env .
COPY languages.json .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD ["python3", "src/run_speech.py", "--folder", "test_files", "--save-output"]