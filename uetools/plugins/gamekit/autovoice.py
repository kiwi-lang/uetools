import datetime
import os
from dataclasses import dataclass

from argklass.command import Command, ParentCommand


def _impl():
    import numpy as np

    OS_TTS = None
    try:
        import pyttsx3
        from scipy.io.wavfile import read as readwav
        from scipy.io.wavfile import write as writewav
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

    class TextToSpeech:
        def __init__(self, voice) -> None:
            import torch

            language = "en"
            model_id = "v3_en"

            device = torch.device("cpu")
            output = torch.hub.load(
                repo_or_dir="snakers4/silero-models",
                model="silero_tts",
                language=language,
                speaker=model_id,
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

    def get_voices():
        engine = pyttsx3.init()
        return engine.getProperty("voices")

    def show_voice(i, v):
        print(f"  --- {i}")
        print("        Name", v.name)
        print("         Age", v.age, "\tGender", v.gender)
        print("   Languages", v.languages)

    def select_voice(voices):
        engine = pyttsx3.init()

        for i, v in enumerate(voices):
            show_voice(i, v)
            print()

            engine.setProperty("voice", v.id)
            engine.say("I will speak this text")
            engine.runAndWait()

        return 0

    class TextToSpeechOS:
        def __init__(self, voice) -> None:
            if OS_TTS is not None:
                raise OS_TTS

            voices = get_voices()
            if voice is None:
                print("Select a Voice:")
                voice = select_voice(voices)
                print()
            else:
                print("Selected Voice:")
                show_voice(voice, voices[voice])
                print()

            self.sample_rate = None
            self.voice = voices[voice].id
            self.engine = pyttsx3.init()
            self.buffer_file = "buffer.wav"

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.cleanup()

        def to_speech(self, text):
            self.engine.setProperty("voice", self.voice)

            self.engine.save_to_file(text, self.buffer_file)
            self.engine.runAndWait()

            sr, data = readwav(self.buffer_file)
            self.sample_rate = sr
            return data

        def __del__(self):
            self.cleanup()

        def cleanup(self):
            try:
                os.remove(self.buffer_file)
            except:
                pass

    def get_subtitles(filename):
        return formatting.clean(
            ascii.clean(brackets.clean(lower_case.clean(subparser.parse(filename))))
        )

    def get_length(subtitles) -> datetime.timedelta:
        start = datetime.time()
        end = datetime.time()

        for subtitles in subtitles:
            end = max(end, subtitles.end)

        datetime.timedelta()
        fake_date = datetime.date.min

        # convert to timedelta
        duration = datetime.datetime.combine(
            fake_date, end
        ) - datetime.datetime.combine(fake_date, start)
        return duration

    def play_audio(data, sample_rate):
        if SOUND_DEVICE is not None:
            raise SOUND_DEVICE

        sd.default.samplerate = sample_rate
        sd.play(data, blocking=True)

    def read(filename, voice, outputfile):
        if SUBTITLE_PARSER is not None:
            raise SUBTITLE_PARSER

        engine = TextToSpeech()
        length = get_length(get_subtitles(filename))

        print(f"Creating an audio file lasting {length.seconds} s")

        sample_rate = None
        audio = None

        def generate_audio_buffer(sample_rate):
            sample_count = length.seconds * sample_rate

            print(f"Sample rate is {sample_rate}")
            print(f"Audio has {sample_count} samples")
            print("Generating:")
            print()

            return np.empty((sample_count,), dtype=np.int16)

        for subtitle in get_subtitles(filename):
            t = subtitle.text
            i = subtitle.index
            s = subtitle.start
            e = subtitle.end

            sample_rate = None
            data = engine.to_speech(t)

            if sample_rate is None:
                sample_rate = engine.sample_rate
                audio = generate_audio_buffer(sample_rate)

            ss = s.second * sample_rate
            e.second * sample_rate

            print("  -", i, t)
            audio[ss : ss + len(data)] = data[0:]

        print()
        writewav(outputfile, sample_rate, audio)
        print("Done")

    return read


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

        default_file = "E:/work/SubtitleToAudio/examples/captions.srt"

        filename = args.file or default_file
        outputfile = os.path.basename(filename) + ".wav"

        if args.output:
            outputfile = os.path.join(args.output, outputfile)

        impl = _impl()

        impl(filename, args.voice, outputfile)

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
        return [SubtitleToAudio]


COMMANDS = VoiceUtility
