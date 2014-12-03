import pyaudio
import wave
import data

# This is modified from examples in PyAudio official website
def playMusic(choice):
    if choice == "default":
        fileName = "StartGamePlay.wav"
    else:
        fileName = "StartGamePlay.wav"
    path = data.Data().filePath(fileName)

    count = 0
    while count < 5:
        count += 1
        wf = wave.open(path, 'rb')

        # instantiate PyAudio (1)
        p = pyaudio.PyAudio()

        # open stream using callback (3)
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)

        datas = wf.readframes(1024)

        while datas != '':
            stream.write(datas)
            datas = wf.readframes(1024)

       # stop stream (6)
        stream.stop_stream()
        stream.close()

        # close PyAudio (7)
        p.terminate()

#playMusic("StartGamePlay.wav")