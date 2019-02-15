#-*- coding: utf-8 -*-
from _socket import *
import pyaudio
import datetime
import wave


CHUNK         = 1024
CHANNELS      = 1
RATE          = 44100
DELAY_SECONDS = 5
DELAY_SIZE    = DELAY_SECONDS * RATE / (10 * CHUNK)
HOST          = ''
PORT          = 8080

def init_audio(channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, FORMAT=pyaudio.paInt16):
    print "init_audio: Create PyAudio object"
    pa = pyaudio.PyAudio()
    print "init_audio: Open stream"
    s = pa.open(
        output=True,
        channels = channels,
        rate = rate,
        format = FORMAT,
        frames_per_buffer=frames_per_buffer
    )
    print "init_audio: audio stream initialized"
    return pa, s

def close_audio(pa, s):
    print "close_audio: Closing stream"
    s.close()
    print "close_audio: Terminating PyAudio Object"
    pa.terminate()

# for i in range(100):
#     file = r"/home/qorwogus/Desktop/audio_test/"+str(i)+".wav"
#     f = wave.open(file, "rb")
#     p = pyaudio.PyAudio()
#
#     stream = p.open(
#         format=p.get_format_from_width(f.getsampwidth()),
#         channels=f.getnchannels(),
#         rate=f.getframerate(),
#         output=True
#     )
#
#     data = f.readframes(CHUNK)
#
#     while data:
#         stream.write(data)
#         data=f.readframes(CHUNK)
#
#     stream.stop_stream()
#     stream.close()
#
#     p.terminate()


if __name__ == "__main__":
    client = socket(AF_INET, SOCK_STREAM)
    client.connect(('127.0.0.1', 8080))
    print '연결 확인 됐습니다.'
    client.send('I am a client'.encode('utf-8'))
    print'메시지를 전송했습니다.'

    pa, s = init_audio()

    while True:
        data = client.recv(CHUNK)
        print '데이터 수신 : ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        s.write(data)
