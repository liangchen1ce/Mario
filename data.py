from os.path import *
from Tkinter import PhotoImage

class Data(object):
    def __init__(self):
        self.dirPath = normpath(join(abspath(dirname(__file__)), "data"))

    def filePath(self, fileName):
        return join(self.dirPath, fileName)

    def load(self, fileName):
        return open(self.filePath(fileName), "r")

    def loadImage(self, fileName):
        return PhotoImage(file=self.filePath(fileName))

    def loadSmallerImage(self, fileName, X, Y):
        return PhotoImage(file=self.filePath(fileName)).subsample(X, Y)

    def loadBiggerImage(self, fileName, X, Y):
        return PhotoImage(file=self.filePath(fileName)).zoom(X, Y)

    @staticmethod
    def testFilePath():
        data = Data()
        assert(data.filePath("mario.gif")
        == "/Users/chenlian/Dropbox/2014fall/15112/termProject/GamePart/data/mario.gif")
        print "Passed!"

    @staticmethod
    def testAll():
        Data.testFilePath()

if __name__ == '__main__':
    Data.testAll()