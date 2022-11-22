import argparse
import urllib.request
import os
import shutil
import mimetypes
from cv2 import VideoCapture
import traceback
mimetypes.init()

from openai_whisper.src.transcribe import perform_speech_to_text


def parse_args():
    '''
    This script will take a video url from mux, split the audio, detect the language, and transcribe/translate the speech detected in the audio.
    If the language detected is not english, the program will default to translating text to english.
    '''
    parser = argparse.ArgumentParser(
        description='OpenAI Whisper - transcribe the speech in a video into english text')
    parser.add_argument('mux_url', help='mux url, writes out detections.json to processed/(VIDEO_ID)/')
    parser.add_argument('video_id', help='unique id for saving video and video info')
    parser.add_argument('--folder', default='', help='path/to/folder/of/videos')

    args = parser.parse_args()
    return args


def process_video(mux_url, video_id, folder):

    os.makedirs(f'temp_videodata_storage', exist_ok=True)

        # if not using folders, download video from mux
    if folder == '':
        urllib.request.urlretrieve(f"{mux_url}?download={video_id}.mp4", f'temp_videodata_storage/{video_id}.mp4') 
        print('downloading complete')

    perform_speech_to_text(video_id, folder)

    shutil.rmtree('temp_videodata_storage')




if __name__ == '__main__':

    args = parse_args()

    # if no folder is provided
    if args.folder == '':
        process_video(args.mux_url, args.video_id, args.folder)

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
                            process_video('', os.path.splitext(file)[0], filepath)
                        except Exception as e:
                            print(f"broken video: {filepath}")
                            print(e)
                            print(traceback.format_exc())       