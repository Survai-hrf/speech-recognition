import whisper
import moviepy.editor as mp
import json
import os


def perform_speech_to_text(video_id, folder, save_output):

    output_data = {}
    
    video = f'{video_id}.mp4'
    audio_file = f'{video_id}.wav'

    # if folder of videos is not specified default to:
    if folder == '':
        video = f'temp_videodata_storage/{video}'
    else:
        video = folder

    # split audio from video file
    clip = mp.VideoFileClip(video)
    clip.audio.write_audiofile(audio_file)

    # load speech to text model
    model = whisper.load_model('medium')

    # detect language
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    language = {max(probs, key=probs.get)}
    print(language)

    # if language not english, translate to english
    if language != {'en'}:
        print('language not english, translating...')
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task='translate', **options)
        result = model.transcribe(audio_file, **translate_options)
        original_result = model.transcribe(audio_file)

        # add data to dictionary
        output_data['language'] = result['language']
        output_data['translation'] = result['text']
        output_data['segments'] = result['segments']
        output_data['original'] = original_result['text']

    else:
        print('language is english')
        result = model.transcribe(audio_file)

        # add data to dictionary
        output_data['language'] = result['language']
        output_data['translation'] = result['text']
        output_data['segments'] = result['segments']

    
    # convert segments to integers
    '''
    for segment in result['segments']:
        segment['start'] = int(segment['start'])
        segment['end'] = int(segment['end'])
    '''

    if save_output == True:
        # export data to json file
        with open(f'{video_id}_transcript.json', 'w+') as file:
            json.dump(output_data, file)
    
    # remove audio file
    os.remove(audio_file)
    print(video, ' completed')

    return output_data
