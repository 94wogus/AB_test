#-*- coding: utf-8 -*-
#!/usr/bin/python
import os
import pyaudio
import signal
from socket import socket, error, AF_INET, SOCK_STREAM
import datetime

CHUNK         = 1024
CHANNELS      = 1
RATE          = 44100
DELAY_SECONDS = 5
DELAY_SIZE    = DELAY_SECONDS * RATE / (10 * CHUNK)
HOST          = ''
PORT          = 8080
FORMAT        = pyaudio.paInt16


def init_audio(channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, FORMAT= pyaudio.paInt16):
    print("init_audio: Create PyAudio object")
    pa = pyaudio.PyAudio()
    print("init_audio: Open stream")
    s = pa.open(
        input=True,
        channels = channels,
        rate = rate,
        format = FORMAT,
        frames_per_buffer=frames_per_buffer
    )
    print("init_audio: audio stream initialized")
    return pa, s

def init_audio2(channels=CHANNELS, rate=RATE, frames_per_buffer=CHUNK, FORMAT= pyaudio.paInt16):
    print("init_audio: Create PyAudio object")
    pa = pyaudio.PyAudio()
    print("init_audio: Open stream")
    s = pa.open(
        input=True,
        channels = channels,
        rate = rate,
        format = FORMAT,
        frames_per_buffer=frames_per_buffer,
        stream_callback=get_callback()
    )
    print("init_audio: audio stream initialized")
    return pa, s

def close_audio(pa, s):
    print("close_audio: Closing stream")
    s.close()
    print("close_audio: Terminating PyAudio Object")
    pa.terminate()

def recode(s, duration):
    audio = str()
    for i in range(int(RATE / CHUNK * duration)):
        data = s.read(CHUNK)
        audio = audio + data
    return audio

def recode2(s, duration):
    pass

def get_callback(self):
    def callback(in_data, frame_count, time_info, status):
        self.wavefile.writeframes(in_data)
        return in_data, pyaudio.paContinue

    return callback

def sigint_handler(signum, frame):
    close_audio(pa, s)

signal.signal(signal.SIGINT, sigint_handler)


if __name__ == "__main__":
    while True:
        Server = socket(AF_INET, SOCK_STREAM)
        try:
            Server.bind((HOST, PORT))
        except error:
            os.system('lsof -i :' + str(PORT))
            Server.bind((HOST, PORT))
        Server.listen(1)

        connection, addr = Server.accept()
        print(str(addr), '에서 접속이 확인되었습니다.')

        data = connection.recv(CHUNK)
        if data.decode('utf-8') == 'I am a client':
            pa, s = init_audio()
            while True:
                try:
                    audio = recode(s, 0.2)
                    # print audio
                    # print len(audio)
                    # print type(audio)
                    connection.send(audio)
                    print('메시지를 보냈습니다. : ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                except error:
                    close_audio(pa, s)
                    break
        else:
            print('Go away! Stranger!')
