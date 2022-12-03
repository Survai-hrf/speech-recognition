import whisper
import moviepy.editor as mp
import json
import os


def format_data(result, video_id):
    '''
    Takes the raw output from the speech to text model and reshapes data into proper format.
    '''
    output = {}
    segments = []

    with open('languages.json') as file:
        languages = json.load(file)

    # store needed data for each segment in dictionary and append to list
    for segment in result['segments']:
        segments.append({
            'start': int(segment['start']),
            'text': segment['text']
        })

    # build final dictionary 
    output['uniqueId'] = video_id
    output['originalLanguage'] = languages.get(result['language'])
    output['transcription'] = result['text']
    output['segments'] = segments

    return output


def perform_speech_to_text(video_id, folder, save_output):
    '''
    Runs speech to text model on a given video and returns data in proper format.
    '''
    video_file = f'{video_id}.mp4'
    audio_file = f'{video_id}.wav'

    # if folder of videos is not specified default to:
    if folder == '':
        video_file = f'temp_videodata_storage/{video_file}'
    else:
        video_file = folder

    # load video
    clip = mp.VideoFileClip(video_file)

    # if video has no audio, return empty transcription
    if clip.audio is None:
        print(f'NO AUDIO DETECTED: {video_file}')
        return {
            "uniqueId": video_id,
            "originalLanguage": "no speech detected",
            "transcription": "",
            "segments": []
        }

    # split audio from video
    clip.audio.write_audiofile(audio_file)

    # load speech to text model
    model = whisper.load_model('large', device='cpu')

    # detect language
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    language = max(probs, key=probs.get)
    print(language)

    # if language not english, translate to english
    if language != 'en':
        print('language not english, translating...')
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task='translate', **options)
        result = model.transcribe(audio_file, **translate_options)
    else:
        print('language is english')
        result = model.transcribe(audio_file)

    # format data for web
    output_data = format_data(result, video_id)

    if save_output == True:
        # export data to json file
        if not os.path.exists('output_files'):
            os.mkdir('output_files')      
        with open(f'output_files/{video_id}_transcript.json', 'w+') as file:
            json.dump(output_data, file)
    
    # remove audio file
    os.remove(audio_file)
    print(video_id, ' completed')

    return output_data




