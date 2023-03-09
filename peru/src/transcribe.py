import whisper
import moviepy.editor as mp
import json
import os


def format_data(english_result, original_result, video_id):
    '''
    THIS WILL CHANGE TO FORMAT INTO CSV FORMAT
    '''
    output = {}

    # build dictionary
    output['Content ID'] = video_id
    output['Link'] = None
    output['english transcription'] = english_result['text']

    if original_result == None:
        output['original language transcription'] = original_result
    else:
        output['original language transcription'] = original_result['text']

    return output


def perform_speech_to_text(file_path, model):
    '''
    Runs speech to text model on a given video and returns data in proper format.
    '''
    video_file = file_path
    audio_file = os.path.basename(file_path)
    audio_file = f"{os.path.splitext(audio_file)[0]}.wav"

    # load video
    clip = mp.VideoFileClip(video_file)

    # if video has no audio, return empty transcription
    if clip.audio is None:
        print(f'NO AUDIO DETECTED: {video_file}')
        return

    # split audio from video
    clip.audio.write_audiofile(audio_file)

    # detect language
    audio = whisper.load_audio(audio_file)
    audio = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio).to(model.device)
    _, probs = model.detect_language(mel)
    language = max(probs, key=probs.get)
    print(language)

    # if language confidence is low, skip transcription
    if probs.get(language) < 0.54:
        os.remove(audio_file)
        return

    # if language not english, translate to english
    if language != 'en':
        print('language not english, translating...')
        english_result = model.transcribe(audio_file, task='translate', beam_size=5, best_of=5)
        original_result = model.transcribe(audio_file, beam_size=5, best_of=5)
    else:
        print('language is english')
        english_result = model.transcribe(audio_file, beam_size=5, best_of=5)
        original_result = None

    # format data for web
    output_data = format_data(english_result, original_result, file_path)
    
    # remove audio file
    os.remove(audio_file)
    print(file_path, ' completed')
    print(output_data)

    return output_data