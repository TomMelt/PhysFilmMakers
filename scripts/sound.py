import math
import warnings
from pyaudio import PyAudio


BITRATE = 32000
LENGTH = 0.005

NUMBEROFFRAMES = int(BITRATE * LENGTH)
RESTFRAMES = NUMBEROFFRAMES % BITRATE

p = PyAudio()
stream = p.open(
    format=p.get_format_from_width(1),
    channels=1,
    rate=BITRATE,
    output=True,
    )


def playsound(FREQUENCY=600):
    WAVEDATA = ''
    for x in range(NUMBEROFFRAMES):
        WAVEDATA += chr(
                int(
                    math.sin(x / ((BITRATE / FREQUENCY) / math.pi)) * 127 + 128
                    )
                )

    # fill remainder of frameset with silence
    for x in range(RESTFRAMES):
        WAVEDATA += chr(128)

    with warnings.catch_warnings():
        stream.write(WAVEDATA)
