#-*- coding: utf-8 -*-
#!/usr/bin/python
import os
import pyaudio
import signal
from socket import socket, error, AF_INET, SOCK_STREAM
import time
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
    print "init_audio: Create PyAudio object"
    pa = pyaudio.PyAudio()
    print "init_audio: Open stream"
    s = pa.open(
        input=True,
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

def recode(s, duration):
    for _ in range(int(RATE / CHUNK * duration)):
        audio = s.read(CHUNK)
    return audio

def sigint_handler(signum, frame):
    close_audio(pa, s)

signal.signal(signal.SIGINT, sigint_handler)


if __name__ == "__main__":
    while True:
        pa, s = init_audio()

        Server = socket(AF_INET, SOCK_STREAM)
        try:
            Server.bind((HOST, PORT))
        except error:
            os.system('lsof -i :' + str(PORT))
            Server.bind((HOST, PORT))
        Server.listen(1)

        connection, addr = Server.accept()
        print str(addr), '에서 접속이 확인되었습니다.'

        data = connection.recv(1024)
        print len(data)
        print '받은 데이터 : ', data.decode('utf-8')

        while True:
            try:
                audio = recode(s, 1)
                # print audio
                # print len(audio)
                # print type(audio)
                connection.send(audio)
                print '메시지를 보냈습니다. : ', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            except error:
                close_audio(pa, s)
                break
