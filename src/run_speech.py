import argparse
import urllib.request
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
    parser.add_argument('video_id', help='unique id for saving video and video info')
    parser.add_argument('--folder', default='', help='path/to/folder/of/videos')

    args = parser.parse_args()
    return args


def process_video(video_id, folder):

    while True: 
        
        os.makedirs(f'temp_videodata_storage', exist_ok=True)

        if folder == '':
            video_id, resp, receipt_handle = connect_and_download(args.folder)

        if resp == 0:
            print("No messages")
            continue


        print('initializing speech to text model for inference...')
        perform_speech_to_text(video_id, folder)


        with open(f'{video_id}_transcription.json') as file:
            transcript = json.load(file)

        if folder == '':
            #send json to web
            API_ENDPOINT = "https://glimpse-weld.vercel.app/api/ai"
            r = requests.post(url=API_ENDPOINT, json=transcript)
            #print(r.content)

            delete_message(receipt_handle)
            #os.remove(f'{video_id}_transcription.json')
            shutil.rmtree('temp_videodata_storage')
            print('message deleted')
        else:
            break



if __name__ == '__main__':

    args = parse_args()

    # if no folder is provided
    if args.folder == '':
        process_video(args.video_id, args.folder)

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
                            process_video(os.path.splitext(file)[0], filepath)
                        except Exception as e:
                            print(f"broken video: {filepath}")
                            print(e)
                            print(traceback.format_exc())       