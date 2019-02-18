#-*- coding: utf-8 -*-
from _socket import *
import pyaudio
import datetime



CHUNK         = 1024
CHANNELS      = 1
RATE          = 44100
DELAY_SECONDS = 5
DELAY_SIZE    = DELAY_SECONDS * RATE / (10 * CHUNK)
HOST          = ''
PORT          = 8089

def init_audio(channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, FORMAT=pyaudio.paInt16):
    print("init_audio: Create PyAudio object")
    pa = pyaudio.PyAudio()
    print("init_audio: Open stream")
    s = pa.open(
        output=True,
        channels = channels,
        rate = rate,
        format = FORMAT,
        frames_per_buffer=frames_per_buffer
    )
    print("init_audio: audio stream initialized")
    return pa, s

def close_audio(pa, s):
    print("close_audio: Closing stream")
    s.close()
    print("close_audio: Terminating PyAudio Object")
    pa.terminate()


if __name__ == "__main__":
    client = socket(AF_INET, SOCK_STREAM)
    data = 1
    try:
        client.connect(('127.0.0.1', PORT))
        print('연결 확인 됐습니다.')
        client.send('I am a client'.encode('utf-8'))
        print('메시지를 전송했습니다.')
        pa, s = init_audio()

        while data:
            data = client.recv(CHUNK)
            print('데이터 수신 : ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            s.write(data)
    except:
        close_audio(pa, s)
        print('연결이 실패 하였습니다.')


