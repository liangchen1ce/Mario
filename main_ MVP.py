# -*- coding: utf-8 -*-
from Tkinter import *
from eventBasedAnimationClass import EventBasedAnimationClass
import random
from objectClasses import Camera, Mario, Brick, Earth
import bricksSet

class Stream(EventBasedAnimationClass):
    def __init__(self, rows=12, cols=20):
        cellWidth, cellHight = 50, 99/3 # 88 is Mario's height
        canvasWidth = cols*cellWidth
        canvasHeight = rows*cellHight
        super(Stream, self).__init__(canvasWidth, canvasHeight)
        self.cellSize = (cellWidth, cellHight)
        self.rows = rows
        self.cols = cols
        self.rowsWhole = 36
        self.colsWhole = 30
        self.backgroundSize = (self.colsWhole*cellWidth, self.rowsWhole*cellHight)

    def initAnimation(self):
        self.timerDelay = 20
        self.camera = Camera(self.rows, self.cols, self.rowsWhole, self.colsWhole, self.cellSize)
        self.earth = Earth(self.backgroundSize, self.camera)
        earthHeight = self.earth.square[1]
        offset = (self.rowsWhole-self.rows)*self.cellSize[1]
        self.mario = Mario(earthHeight, offset, self.cellSize)
        self.score = 0
        self.board = [[None] * self.colsWhole for i in xrange(self.rowsWhole)]
        self.bricks = []
        bricksPos = bricksSet.chooseBrickSet("default", self.colsWhole, self.rowsWhole)
        for pos in bricksPos:  # need to change to modified by midi later
            self.bricks += [Brick(pos[0], pos[1], self.cellSize, self.camera)]

        def compareBricksByCol(a, b):
            return (b.row - a.row) if (a.col - b.col) == 0 else (a.col - b.col)
        self.bricks = sorted(self.bricks, compareBricksByCol)

        # changed in onTimeFired to determine which image of mario should be used
        self.count = 0
        self.speedCount = 0

        for brick in self.bricks:
            if brick.hasRock:
                self.updateWindowRock(brick.rock)

        self.scoreColors = ["red", "green", "orange", "black", "#8D7C69", "#24505C"]
        self.scoreColor = self.scoreColors[0]
        self.isPaused = False # set isPaused as False in the beginning
        self.isGameOver = False

    def onKeyPressed(self, event):
        if event.char == "r":  # restart game
            self.initAnimation()
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
        x, y = event.x, event.y
        print "Mouse click on:", x, y

    def onTimerFired(self):
        if not self.isGameOver:
            if not self.isPaused:

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
                elif self.speedCount == 1:
                    self.timerDelay = 8
                elif self.speedCount == 2:
                    self.timerDelay = 3
                elif self.speedCount == -1:
                    self.timerDelay = 40
                elif self.speedCount == -2:
                    self.timerDelay = 80

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
        self.drawCamera()
        if self.isGameOver:
            cx = self.width/2
            cy = self.height/2
            self.canvas.create_text(cx, cy, text="Game Over!",
                                    font=("Unifont", 35, "bold"))

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

if __name__ == '__main__':
    Stream().run()