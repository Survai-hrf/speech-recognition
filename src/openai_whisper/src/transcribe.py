import whisper
import moviepy.editor as mp
import json


def perform_speech_to_text(video_id, folder):

    output_data = {}
    
    video_id = f'{video_id}.mp4'

    # if folder of videos is not specified default to:
    if folder == '':
        video = f'temp_videodata_storage/{video_id}'
    else:
        video = folder

    # create file name for audio
    audio_file = video_id.split('.')[0]
    audio_file = f'{audio_file}.wav'

    # split audio from video file
    clip = mp.VideoFileClip(video)
    clip.audio.write_audiofile(audio_file)

    # load speech to text model
    model = whisper.load_model('base', device='cpu')

    # detect language
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    language = {max(probs, key=probs.get)}

    # if language not english, translate to english
    if language != {'en'}:
        options = dict(beam_size=5, best_of=5)
        translate_options = dict(task='translate', **options)
        translate_result = model.transcribe(audio_file, **translate_options)

        # add data to dictionary
        output_data['language'] = translate_result['language']
        output_data['translation'] = translate_result['text']

    else:
        result = model.transcribe(audio_file)

        # add data to dictionary
        output_data['language'] = result['language']
        output_data['translation'] = result['text']

    # export data to json file
    with open('transcription.json', 'w+') as file:
        json.dump(output_data, file)
