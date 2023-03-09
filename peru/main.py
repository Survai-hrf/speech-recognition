#from src.transcribe import perform_speech_to_text

import os


dir = 'Downloads'

# make list of files
files = os.listdir(dir)

for file in files:
    print(f'{dir}/{file}')

    # perform transcription
    #perform_speech_to_text(base_name)