import argparse
import os
import json
import requests
import shutil
import mimetypes
from cv2 import VideoCapture
import traceback
mimetypes.init()

from openai_whisper.src.transcribe import perform_speech_to_text
from connect_download.connect_and_download import connect_and_download, delete_message


def parse_args():
    '''
    This script will take a video url from mux, split the audio, detect the language, and transcribe/translate the speech detected in the audio.
    If the language detected is not english, the program will default to translating text to english.
    '''
    parser = argparse.ArgumentParser(
        description='OpenAI Whisper - transcribe the speech in a video into english text')
    parser.add_argument('--folder', default='', help='path/to/folder/of/videos')
    parser.add_argument('--save-output', default=False, action='store_true', help='boolean')

    args = parser.parse_args()
    return args


def process_video(video_id, folder, save_output):
   
    while True: 
        if not os.path.exists('temp_videodata_storage'):
            os.makedirs(f'temp_videodata_storage')

        if folder == '':
            # connect to queue and download video using unique id and mux url
            video_id, resp, receipt_handle = connect_and_download(args.folder)

            if resp == 0:
                print("No messages")
                break
        
        # transcribe video
        print('initializing speech to text model for inference...')
        transcript = perform_speech_to_text(video_id, folder)

        if save_output == True:
            # export data to json file
            if not os.path.exists('output_files'):
                os.mkdir('output_files')      
            with open(f'output_files/{video_id}_transcript.json', 'w+') as file:
                json.dump(transcript, file)

        if folder == '':
            #send json to web
            API_ENDPOINT = "https://glimpse-ouqbsh7ia-survai.vercel.app/api/speech-to-text"
            r = requests.post(url=API_ENDPOINT, json=transcript)
            print(r.content)
            print("data sent to AWS")

            delete_message(receipt_handle)
            shutil.rmtree('temp_videodata_storage')
            print('message deleted')
        else:
            break


if __name__ == '__main__':

    args = parse_args()

    # if no folder is provided
    if args.folder == '':
        video_id = 1
        process_video(video_id, args.folder, args.save_output)

    else:
        #iterate folder and all subfolders looking for videos
        for subdir, dirs, files in os.walk(args.folder):
            print('iterating all files in sub directories looking for videos...')
            for file in files:

                filepath = subdir + os.sep + file

                mimestart = mimetypes.guess_type(filepath)[0]

                if mimestart != None:
                    mimestart = mimestart.split('/')[0]

                    #if file is a video
                    if mimestart in ['video']:
                        #verify its a working video 
                        try:
                            capture = VideoCapture(filepath)
                            print(filepath)
                            process_video(video_id=os.path.splitext(file)[0], folder=filepath, save_output=args.save_output)
                        except Exception as e:
                            print(f"broken video: {filepath}")
                            print(e)
                            print(traceback.format_exc())       