# -*- coding: utf-8 -*-
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
from objectClasses import Camera, Mario, Brick, Earth
import bricksSet
import audioRate
import threading
import ctypes
import tkFileDialog
import tkMessageBox

# This class is inspired by my previous homework in 15-112. drawCell() method is directly from previous homework.
class Stream(EventBasedAnimationClass):
    def __init__(self, rows=12, cols=20):
        cellWidth, cellHight = 50, 99/3 # 88 is Mario's height
        canvasWidth = cols*cellWidth
        canvasHeight = rows*cellHight
        super(Stream, self).__init__(canvasWidth, canvasHeight)
        self.cellSize = (cellWidth, cellHight)
        self.rows = rows
        self.cols = cols
        self.canvasWidth = canvasWidth
        self.canvasHeight = canvasHeight

        # splash screen parameters
        self.inSplashScreen = True
        self.optionSize = [self.canvasWidth/6, self.canvasHeight/8]
        self.demoPos = [self.canvasWidth/4, self.canvasHeight/4]
        self.defaultPos = [self.canvasWidth/4, self.canvasHeight/2]
        self.uploadPos = [self.canvasWidth/4, 3*self.canvasHeight/4]
        self.instruction1Pos = [2.8*self.canvasWidth/4, self.canvasHeight/4]
        self.instruction2Pos = [2.8*self.canvasWidth/4, self.canvasHeight/1.7]
        self.demoSquare = self.squareCalc(self.demoPos, self.optionSize)
        self.defaultSquare = self.squareCalc(self.defaultPos, self.optionSize)
        self.uploadSquare = self.squareCalc(self.uploadPos, self.optionSize)
        self.inDemo = False
        self.inDefulat = False
        self.inCustom = False
        self.isPaused = False
        self.threadings = []

    def initAnimation(self):
        self.timerDelay = 20
        self.scoreColors = ["red", "green", "orange", "black", "#8D7C69", "#24505C"]
        self.scoreColor = self.scoreColors[0]
        self.isPaused = False # set isPaused as False in the beginning
        self.isGameOver = False
        self.score = 0
        # changed in onTimeFired to determine which image of mario should be used
        self.count = 0
        self.speedCount = 0

    def choose(self, choice):
        if choice == "demo":
            self.choiceDemo()
        elif choice == "default":
            self.choiceDefault()
        elif choice == "custom":
            self.choiceCustom()

    def choiceCustom(self):
        self.rowsWhole = 36
        self.colsWhole = 480
        self.backgroundSize = (self.colsWhole*self.cellSize[0], self.rowsWhole*self.cellSize[1])
        self.camera = Camera(self.rows, self.cols, self.rowsWhole, self.colsWhole, self.cellSize)
        self.earth = Earth(self.backgroundSize, self.camera)
        earthHeight = self.earth.square[1]
        offset = (self.rowsWhole-self.rows)*self.cellSize[1]
        self.mario = Mario(earthHeight, offset, self.cellSize)
        self.bricks = []
        bricksPos = bricksSet.chooseBrickSet("demo", self.rowsWhole)
        for pos in bricksPos:  # need to change to modified by midi later
            self.bricks += [Brick(pos[0], pos[1], self.cellSize, self.camera)]

        def compareBricksByCol(a, b):
            return (b.row - a.row) if (a.col - b.col) == 0 else (a.col - b.col)
        self.bricks = sorted(self.bricks, compareBricksByCol)

        for brick in self.bricks:
            if brick.hasRock:
                self.updateWindowRock(brick.rock)

    def choiceDefault(self):
        self.rowsWhole = 36
        self.bricks = []
        bricksPos, self.colsWhole = bricksSet.chooseBrickSet("default", self.rowsWhole)
        # self.colsWhole = 480
        self.backgroundSize = (self.colsWhole*self.cellSize[0], self.rowsWhole*self.cellSize[1])
        self.camera = Camera(self.rows, self.cols, self.rowsWhole, self.colsWhole, self.cellSize)
        self.earth = Earth(self.backgroundSize, self.camera)
        earthHeight = self.earth.square[1]
        offset = (self.rowsWhole-self.rows)*self.cellSize[1]
        self.mario = Mario(earthHeight, offset, self.cellSize)

        for pos in bricksPos:  # need to change to modified by midi later
            self.bricks += [Brick(pos[0], pos[1], self.cellSize, self.camera)]

        def compareBricksByCol(a, b):
            return (b.row - a.row) if (a.col - b.col) == 0 else (a.col - b.col)
        self.bricks = sorted(self.bricks, compareBricksByCol)

        for brick in self.bricks:
            if brick.hasRock:
                self.updateWindowRock(brick.rock)

    def choiceDemo(self):
        self.rowsWhole = 36
        self.colsWhole = 30
        self.backgroundSize = (self.colsWhole*self.cellSize[0], self.rowsWhole*self.cellSize[1])
        self.camera = Camera(self.rows, self.cols, self.rowsWhole, self.colsWhole, self.cellSize)
        self.earth = Earth(self.backgroundSize, self.camera)
        earthHeight = self.earth.square[1]
        offset = (self.rowsWhole-self.rows)*self.cellSize[1]
        self.mario = Mario(earthHeight, offset, self.cellSize)
        self.bricks = []
        bricksPos = bricksSet.chooseBrickSet("demo", self.rowsWhole)
        for pos in bricksPos:  # need to change to modified by midi later
            self.bricks += [Brick(pos[0], pos[1], self.cellSize, self.camera)]

        def compareBricksByCol(a, b):
            return (b.row - a.row) if (a.col - b.col) == 0 else (a.col - b.col)
        self.bricks = sorted(self.bricks, compareBricksByCol)

        for brick in self.bricks:
            if brick.hasRock:
                self.updateWindowRock(brick.rock)

    @staticmethod
    def squareCalc(pos, size):
        top = pos[1] - size[1]/2
        bottom = top + size[1]
        left = pos[0] - size[0]/2
        right = left + size[0]
        return left, top, right, bottom

    def onKeyPressed(self, event):
        if event.char == "q" and not self.inSplashScreen:
            if self.inDefulat:
                self.terminate_thread(self.threadings[0])
                self.terminate_thread(self.threadings[1])
                self.__init__()
            elif self.inCustom:
                self.terminate_thread(self.threadings[0])
                self.terminate_thread(self.threadings[1])
                self.__init__()
            else:
                self.__init__()
        if event.char == "r":  # restart game
            if self.inDemo:
                self.initAnimation()
                self.choose("demo")
            elif self.inDefulat:
                self.initAnimation()
                self.choose("default")
            elif self.inCustom:
                self.initAnimation()
                self.choose("custom")
        if not self.isGameOver:
            if self.isPaused and event.char == "p":  # resume the game
                self.isPaused = False
            elif not self.isPaused:
                if event.char == "p":  # pause the game
                    self.isPaused = True
                elif (not self.mario.isFalling) and (not self.mario.isJumping) \
                        and (event.char == " "):  # Mario jump
                    self.mario.jump()
                elif (event.keysym == "Right") and self.speedCount < 2:
                    self.speedCount += 1
                elif (event.keysym == "Left") and self.speedCount > -2:
                    self.speedCount -= 1

    def onMousePressed(self, event):
        if self.inSplashScreen:
            cx, cy = event.x, event.y
            if self.isInside(self.demoSquare, (cx, cy)):
                self.choose("demo")
                self.inSplashScreen = False
                self.inDemo = True
            elif self.isInside(self.defaultSquare, (cx, cy)):
                self.inSplashScreen = False
                self.inDefulat = True

                # def play1():
                #     return self.choose(choice＝"default")

                def play2():
                    # while self.camera.left <= 0:
                    #     pass
                    return audioRate.playMusic(choice="default")

                self.threadings = [threading.Thread(target=self.choose(choice="default"), name="game"),
                              threading.Thread(target=play2, name="music")]
                self.threadings[0].start()
                self.threadings[1].start()

            elif self.isInside(self.uploadSquare, (cx, cy)):
                filePath = tkFileDialog.askopenfilename()
                if filePath == "":
                    print "lalalala"
                elif not ".wav" in filePath:  # This is modified from lecture notes
                    message = "Only accept '.wav' files."
                    title = "Warning"
                    tkMessageBox.showinfo(title, message)
                else:
                    self.inSplashScreen = False
                    self.inCustom = True
                    def play2():
                    # while self.camera.left <= 0:
                    #     pass
                        return audioRate.playMusic(choice=filePath)

                    self.threadings = [threading.Thread(target=self.choose(choice="custom"), name="game"),
                              threading.Thread(target=play2, name="music")]
                    self.threadings[0].start()
                    self.threadings[1].start()

    def handler(self):
        if self.inDefulat or self.inCustom:
            self.terminate_thread(self.threadings[1])
            #self.threadings[1].stop()
        super(Stream, self).handler()

    @staticmethod
    def isInside(square, point):
        # a is an object, point is a tuple
        if square[0] < point[0] < square[2] and square[1] < point[1] < square[3]:
            return True

    def onTimerFired(self):
        if not self.isGameOver:
            if not self.isPaused and not self.inSplashScreen:

                #####place for print debug information
                # print "mario jumping", self.mario.isJumping
                # print "mario falling", self.mario.isFalling
                # print "mario hitRock", self.mario.hitRock
                # print "mario hitTop", self.mario.hitTop

                if self.mario.hitRock:
                    self.gameOver()
                # mario moving forward
                self.count += 1
                self.mario.moveForward()
                #print "a"
                #print "now and previous pos", self.mario.pos, self.mario.previousPos
                self.mario.update()
                self.mario.detect(self.bricks, self.earth)
                self.updateWindowMario()
                # print "now and previous pos", self.mario.pos, self.mario.previousPos
                # print "now square:", self.mario.square
                if self.mario.isJumping:
                    self.mario.jump()
                    #print "b"
                    self.mario.update()
                    self.mario.detect(self.bricks, self.earth)
                    self.updateWindowMario()
                    # print "now and previous pos", self.mario.pos, self.mario.previousPos
                    if self.mario.pos[1] + self.mario.jumpHeight*self.mario.jumpTime <= self.mario.currentGroundHeight:
                        self.mario.fall()
                        # print "c"
                        self.mario.update()
                        self.mario.detect(self.bricks, self.earth)
                        self.updateWindowMario()
                elif self.mario.isFalling:
                    self.mario.fall()
                    # print "d"
                    self.mario.update()
                    self.mario.detect(self.bricks, self.earth)
                    self.updateWindowMario()
                elif self.mario.isHanging:
                    self.mario.fall()
                    # print "e"
                    self.mario.update()
                    self.mario.detect(self.bricks, self.earth)
                    self.updateWindowMario()

                # rock moving forward
                for brick in self.bricks:
                    if brick.hasRock:
                        #print "effective square:", brick.rock.square
                        brick.rock.move()
                        brick.rock.update()
                        #print "move square:", brick.rock.square
                        brick.rock.detect(self.bricks, self.earth)
                        #print "removed square:", brick.rock.square
                        self.updateWindowRock(brick.rock)

                self.updateWindowEarth()
                self.updateWindowBricks()

                # camera moving forward
                self.camera.update(self.mario)
                if self.camera.Rolling and self.mario.windowPos[0] <= 0:
                    self.gameOver()

                # change speed
                if self.speedCount == 0:
                    self.timerDelay = 20
                    for brick in self.bricks:
                        if brick.hasRock:
                            brick.rock.forwardSpeed = 1.5
                elif self.speedCount == 1:
                    self.timerDelay = 10
                    for brick in self.bricks:
                        if brick.hasRock:
                            brick.rock.forwardSpeed = 1.5*15/20
                elif self.speedCount == 2:
                    self.timerDelay = 5
                    for brick in self.bricks:
                        if brick.hasRock:
                            brick.rock.forwardSpeed = 1.5*13/20
                elif self.speedCount == -1:
                    self.timerDelay = 30
                    for brick in self.bricks:
                        if brick.hasRock:
                            brick.rock.forwardSpeed = 1.5*30/20
                elif self.speedCount == -2:
                    self.timerDelay = 40
                    for brick in self.bricks:
                        if brick.hasRock:
                            brick.rock.forwardSpeed = 1.5*35/20

    def updateWindowMario(self):
        self.mario.windowPos[0] = self.mario.pos[0] - self.camera.left
        self.mario.windowPos[1] = self.mario.pos[1] - self.camera.top

    def updateWindowRock(self, rock):
        left = rock.square[0] - self.camera.left
        top = rock.square[1] - self.camera.top
        right = rock.square[2] - self.camera.left
        bottom = rock.square[3] - self.camera.top
        rock.windowSquare = [left, top, right, bottom]

    def updateWindowEarth(self):
        left = self.earth.square[0] - self.camera.left
        top = self.earth.square[1] - self.camera.top
        right = self.earth.square[2] - self.camera.left
        bottom = self.earth.square[3] - self.camera.top
        self.earth.windowSquare = [left, top, right, bottom]

    def updateWindowBricks(self):
        for brick in self.bricks:
            if not brick.hit:
                left = brick.square[0] - self.camera.left
                top = brick.square[1] - self.camera.top
                right = brick.square[2] - self.camera.left
                bottom = brick.square[3] - self.camera.top
                brick.windowSquare = [left, top, right, bottom]

    def redrawAll(self):
        self.canvas.delete(ALL)
        if not self.inSplashScreen:
            self.drawCamera()
            if self.isGameOver:
                cx = self.width/2
                cy = self.height/2
                self.canvas.create_text(cx, cy, text="Game Over!",
                                        font=("Unifont", 35, "bold"))
        else:
            self.drawSplashScreen()

        if self.inCustom:
            message = "I have not completed the bricks automatic generation part, so no more bricks! Just Run!            Designed by Chen Liang         Default Music 'Start Game Play' by Emil Milan Karol         Stick Figure from Xingyun Zhang                                                 There is really nothing behind..."
            messagePos = [107 * self.cellSize[0], self.canvasHeight/2]
            messageWindowPos = [0, 0]
            messageWindowPos[0] = messagePos[0] - self.camera.left
            messageWindowPos[1] = self.canvasHeight/2
            font = "Unifont 45"
            self.canvas.create_text(messageWindowPos, text=message, font=font)

    def drawSplashScreen(self):
        # instruction
        instruction1 = "SURVIVAL GUIDE"
        instruction2 = '''
1. Use SPACE to jump
2. Use LEFT and RIGHT to control speed
3. Keep Calm
4. ...and, Carpe diem!!!
(You can choose your own background music:)
(Oh, by the way, try to press 'r', 'q' and 'p')'''
        font1 = "Electrolize 56 bold"
        font2 = "Electrolize 25 "

        # options
        demo = "DEMO"
        fontD = "Unifont 45 bold"
        default = "DEFAULT"
        upload = "UPLOAD"

        self.canvas.create_rectangle(0, 0, self.canvasWidth, self.canvasHeight, fill="#CCEBE9")
        self.canvas.create_text(self.demoPos, text=demo, fill="#666F9A", font=fontD)
        self.canvas.create_text(self.defaultPos, text=default, fill="#E5B853", font=fontD)
        self.canvas.create_text(self.uploadPos, text=upload, fill="#915EA1", font=fontD)
        self.canvas.create_text(self.instruction1Pos, text=instruction1, font=font1)
        self.canvas.create_text(self.instruction2Pos, text=instruction2, font=font2)

    def drawCamera(self):
        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill="#348899")
        self.drawEarth()
        self.drawMario()
        self.drawBricks()
        self.drawEndMessage()
        self.drawScore()
        self.drawSpeed()

    def drawEndMessage(self):
        font = "Electrolize 150"
        self.canvas.create_text(self.camera.endMessageWindowPos[0], text=self.camera.endMessage[0], font=font)
        self.canvas.create_text(self.camera.endMessageWindowPos[1], text=self.camera.endMessage[1], font=font)

    def drawScore(self):
        index = (self.count % 30)/5
        self.scoreColor = self.scoreColors[index]
        font = "Unifont 25"
        self.canvas.create_text(self.canvas.winfo_width()-30, 30, text=str(self.mario.score), fill=self.scoreColor, font=font)

    def drawSpeed(self):
        texts = [" ", "ᐅ", "ᐅᐅ", "ᐊᐊ", "ᐊ"]
        index = self.speedCount
        font = "Unifont 25"
        self.canvas.create_text(30, 30, text=texts[index], font=font)

    def drawEarth(self):
        brown = "#A44B00"
        self.canvas.create_rectangle(self.earth.windowSquare, fill=brown)

    def drawMario(self):
        if self.mario.square == self.mario.previousSquare:
            self.canvas.create_image(self.mario.windowPos, image=self.mario.image_9)
        else:
            if self.count % 36 <= 3:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_0)
            elif self.count % 36 <= 7:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_1)
            elif self.count % 36 <= 11:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_2)
            elif self.count % 36 <= 15:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_3)
            elif self.count % 36 <= 19:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_4)
            elif self.count % 36 <= 23:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_5)
            elif self.count % 36 <= 27:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_6)
            elif self.count % 36 <= 31:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_7)
            elif self.count % 36 <= 35:
                self.canvas.create_image(self.mario.windowPos, image=self.mario.image_8)

    def drawBricks(self):
        for brick in self.bricks:
            if not brick.hit:
                darkWhite = "#962D3E"
                self.canvas.create_rectangle(brick.windowSquare, fill=darkWhite, width=0)
            if brick.hasRock:
                darkRed = "#F2EBC7"
                self.canvas.create_oval(brick.rock.windowSquare, fill=darkRed, width=0)

    def drawCell(self, row, col, fill=None):
        cellSize = self.cellSize
        left = col * cellSize[0]
        right = left + cellSize[0]
        top = row * cellSize[1]
        bottom = top + cellSize[1]
        self.canvas.create_rectangle(left, top, right, bottom,
                                     fill=fill, width=0)

    def gameOver(self):
        self.isGameOver = True

    # this is from Johan Dahlin answer in page:
    # http://stackoverflow.com/questions/323972/is-there-any-way-to-kill-a-thread-in-python
    # Thank god I can finally kill a thread
    def terminate_thread(self, thread):
        """Terminates a python thread from another thread.

        :param thread: a threading.Thread instance
        """
        if not thread.isAlive():
            return

        exc = ctypes.py_object(SystemExit)
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
            ctypes.c_long(thread.ident), exc)
        if res == 0:
            raise ValueError("nonexistent thread id")
        elif res > 1:
            # """if it returns a number greater than one, you're in trouble,
            # and you should call it again with exc=NULL to revert the effect"""
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread.ident, None)
            raise SystemError("PyThreadState_SetAsyncExc failed")

if __name__ == '__main__':
    Stream().run()