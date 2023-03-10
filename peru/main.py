import os
import pandas as pd
from googletrans import Translator

from src.transcribe import perform_speech_to_text


def main():
    dir = 'videos'

    # make list of files
    files = os.listdir(dir)

    csv_list = []
    for file in files:
        # perform transcription
        print(file)
        output_data = perform_speech_to_text(file, 'medium')
        print(output_data)
        csv_list.append(output_data)

    df = pd.DataFrame(csv_list)
    df.to_csv('peru.csv')


if __name__ == "__main__":
    main()