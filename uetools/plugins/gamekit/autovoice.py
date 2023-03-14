from dataclasses import dataclass
import datetime
import os

from uetools.core.command import ParentCommand, Command

OS_TTS = None
try:
    import pyttsx3
    from scipy.io.wavfile import read as readwav, write as writewav
except ImportError as err:
    OS_TTS = err


SUBTITLE_PARSER = None
try:
    from pysubparser import parser as subparser
    from pysubparser.cleaners import ascii, brackets, formatting, lower_case
except ImportError as err:
    SUBTITLE_PARSER = err


SOUND_DEVICE = None
try:
    import sounddevice as sd
except ImportError as err:
    SOUND_DEVICE = err


import torch
import numpy as np


class TextToSpeech:
    def __init__(self) -> None:
       
        language = 'en'
        model_id = 'v3_en'

        device = torch.device('cpu')
        output = torch.hub.load(
            repo_or_dir='snakers4/silero-models',
            model='silero_tts',
            language=language,
            speaker=model_id
        )
         
        model = output[0]
        model.to(device)

        self.model = model  # gpu or cpu
        self.sample_rate = 48000
        self.device = device
        self.speaker = self.model.speakers[0]

    def to_speech(self, text):
        audio = self.model.apply_tts(
            text=text,
            speaker=self.speaker,
            sample_rate=self.sample_rate,
        )
        return audio.numpy()


def get_subtitles(filename):
    return formatting.clean(ascii.clean(brackets.clean(
        lower_case.clean(
            subparser.parse(filename)
        )
    )))


def get_length(subtitles) -> datetime.timedelta:
    start = datetime.time()
    end = datetime.time()

    for subtitles in subtitles:
        end = max(end, subtitles.end)

    datetime.timedelta()
    fake_date = datetime.date.min

    # convert to timedelta
    duration = datetime.datetime.combine(fake_date, end) - datetime.datetime.combine(fake_date, start)
    return duration


def play_audio(data, sample_rate):
    sd.default.samplerate = sample_rate
    sd.play(data, blocking=True)


def read(filename, voice, outputfile):
    engine = pyttsx3.init()

    if voice is not None:
        engine.setProperty('voice', voice)

    length = get_length(get_subtitles(filename))

    print(f'Creating an audio file lasting {length.seconds} s')

    sample_rate = None
    audio = None

    def generate_audio_buffer(sample_rate):
        sample_count = length.seconds * sample_rate
        
        print(f'Sample rate is {sample_rate}')
        print(f'Audio has {sample_count} samples')
        print('Generating:')
        print()
        
        return np.empty((sample_count,), dtype=np.int16)

    for subtitle in get_subtitles(filename):

        t = subtitle.text
        i = subtitle.index
        s = subtitle.start
        e = subtitle.end

        engine.save_to_file(t , buffer_file)
        engine.runAndWait()

        sr, data = readwav(buffer_file)

        if sample_rate is not None:
            assert sample_rate == sr, "Sample rate should not change during generation!"
        else:
            sample_rate = sr
            audio = generate_audio_buffer(sample_rate)

        ss = s.second * sample_rate
        ee = e.second * sample_rate

        print('  -', i, t)
        audio[ss:ss + len(data)] = data[0:]

    print()
    writewav(outputfile, sample_rate, audio)
    print('Done')

    try:
        os.remove(buffer_file)
    except:
        pass
        

def get_voices():
    engine = pyttsx3.init()
    return engine.getProperty('voices') 


def show_voice(i, v):
    print(f'  --- {i}')
    print('        Name', v.name)
    print('         Age', v.age, '\tGender', v.gender)
    print('   Languages', v.languages)


def select_voice(voices):
    engine = pyttsx3.init()

    for i, v in enumerate(voices):
        show_voice(i, v)
        print()

        engine.setProperty('voice', v.id)
        engine.say("I will speak this text")
        engine.runAndWait()

    return 0


buffer_file = "buffer.wav"


class SubtitleToAudio(Command):
    """Generate audio from a subtitle file"""

    name: str = "subtitle"
    
    # fmt: off
    @dataclass
    class Arguments:
        file  : str             # subtitle file to turn into audio
        voice   : int   = 0     # Voice index to use to generate audio
        output  : str   = "."   # Output folder
    # fmt: on

    @staticmethod
    def execute(args):
        # engine = TextToSpeech()
        # output = engine.to_speech("Hello; Welcome to the fog of war tutorial")
        # writewav("test.wav", engine.sample_rate, output)
        # return

        if OS_TTS is not None:
            raise OS_TTS
    
        default_file = 'E:/work/SubtitleToAudio/examples/captions.srt'
        
        voices = get_voices()

        if args.voice is None:
            print('Select a Voice:')
            args.voice = select_voice(voices)
            print()
        else:
            print('Selected Voice:')
            show_voice(args.voice, voices[args.voice])
            print()


        filename = args.file or default_file
        outputfile = os.path.basename(filename) + '.wav'

        if args.output:
            outputfile = os.path.join(args.output, outputfile)
        
        read(filename, voices[args.voice].id, outputfile)
        return 0


#
# Parent
#

class VoiceUtility(ParentCommand):
    """Utility to generate audio from subtitles"""

    name: str = "voice"

    @staticmethod
    def module():
        import uetools.plugins.gamekit.autovoice
        return uetools.plugins.gamekit.autovoice
    
    @staticmethod
    def command_field():
        return "subsubcommand"
    
    @staticmethod
    def fetch_commands():
        return [
            SubtitleToAudio
        ]

COMMANDS = VoiceUtility
