import whisper
import moviepy.editor as mp


def perform_speech_to_text(video_path):

    # create file name for audio
    audio_file = video_path.split('.')[0]
    audio_file = f'{audio_file}.wav'

    # split audio from video file
    clip = mp.VideoFileClip(video_path)
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
        result = model.transcribe(audio_file, **translate_options)
        return result
    else:
        result = model.transcribe(audio_file)
        return result