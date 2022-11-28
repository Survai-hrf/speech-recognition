FROM python:3.9

WORKDIR /speech_to_text

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ./src ./src

CMD ["python", "./src/run_speech.py", "0", "--folder", "test_files"]