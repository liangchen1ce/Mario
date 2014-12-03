import audioRate

def playAudio(choice):
    # if speedCount == 0:
    #     rate = 1
    # elif speedCount == 1:
    #     rate = 2
    # elif speedCount == 2:
    #     rate = 4
    # elif speedCount == -1:
    #     rate = 0.5
    # else:  # speedCount == -2
    #     rate = 0.25
    if choice == "default":
        audioRate.playMusic()
    elif choice == "custom":
        pass

# modified from stackoverflow answer
# http://stackoverflow.com/questions/22755558/increase-decrease-play-speed-of-a-wav-file-python
# def saveNewAudios(fileName="StartGamePlay"):
#     path = data.Data().filePath(fileName+".wav")
#     CHANNELS = 1
#     swidth = 2
#     Change_RATE = [5, 10, 0.8, 0.5]
#     wf = [None, None, None, None]
#     newName = ["data/StartGamePlay0.wav", "data/StartGamePlay1.wav",
#                "data/StartGamePlay2.wav", "data/StartGamePlay3.wav"]
#
#     spf = wave.open(path, 'rb')
#     RATE=spf.getframerate()
#     signal = spf.readframes(-1)
#
#     for i in xrange(4):
#         wf[i] = wave.open(newName[i], 'wb')
#         wf[i].setnchannels(CHANNELS)
#         wf[i].setsampwidth(swidth)
#         wf[i].setframerate(RATE*Change_RATE[i])
#         wf[i].writeframes(signal)
#         wf[i].close()
#
# saveNewAudios()