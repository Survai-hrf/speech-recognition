FROM nvidia/cuda:11.3.1-base-ubuntu20.04

# install python 3.9
RUN sudo apt-get update -y
RUN sudo apt-get install -y python=3.9

# create directory to copy repo
WORKDIR /speech_to_text

# copy requirements and env
COPY requirements.txt .
COPY .env .

# install dependencies
RUN pip install -r requirements.txt

# copy src files
COPY ./src ./src

# run command to perform speech to text
CMD ["python", "./src/run_speech.py"]