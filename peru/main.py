import os
import pandas as pd

from src.transcribe import perform_speech_to_text


dir = 'videos'

# make list of files
files = os.listdir(dir)

csv_list = []
for file in files:
    # perform transcription
    print(file)
    output_data = perform_speech_to_text(file, 'base')
    print(output_data)
    csv_list.append(output_data)