# from Tkinter import *
# from eventBasedAnimationClass import EventBasedAnimationClass
# import data
# import random
#
# ########Global Cons
# # should change cellHight in Stream class manually
# # the real jump height == (1+mario.jumpTime)*mario.jumpHeight
#
# ########Bricks
# # have a bug about jumping on bricks. Cannot define where the ground is
# # have different kinds of bricks to display
# # have a bug when hit down side of brick(length is too large because of time delay setting)
#
# ########Rock
#
# # def collideOnLeftOfA(a, b):
# #     # three conditions:
# #     # a = brick and b = mario
# #     # a = brick and b = rock
# #     # a = rock and  b = mario
# #     posOffset = 2
# #     if ((a.square[0]-2 <= b.square[2] <= a.square[0])
# #     and (a.square[1]-b.size[1]+posOffset < b.square[1] < a.square[3]-posOffset)):
# #         b.collide(a, "left")
# #
# # def collideOnRightOfA(a, b):
# #     posOffset = 2
# #     if ((a.square[2]-2 <= b.square[2] <= a.square[2])
# #     and (a.square[1]-b.size[1]+posOffset < b.square[1] < a.square[3]-posOffset)):
# #         b.collide(a, "right")
# #
# # def isNotCollideAnyBrick(a, b):
# #     # a: bricks b: rock
# #     pointUL = (b.square[0], b.square[1])
# #     pointUR = (b.square[2], b.square[1])
# #     pointDL = (b.square[0], b.square[3])
# #     pointDR = (b.square[2], b.square[3])
# #     points = [pointUL, pointUR, pointDL, pointDR]
# #     for brick in a:
# #         for point in points:
# #             if isInside(brick, point):
# #                 return
# #     b.collide(a[0], "notCollide")
# #
# #
# # def isInside(a, point):
# #     # a is an object, point is a tuple
# #     if a.square[0] <= point[0] <= a.square[2] and a.square[1] <= point[1] <= a.square[3]:
# #         return True
# #
# # class Rock(object):
# #     def __init__(self, x, y, d):
# #         #self.hight = 25
# #         # self.image = data.Data().loadImage("rock.gif")
# #         # self.size = (self.image.width(), self.image.height())
# #         # offset = 5
# #         # self.pos = [self.size[0]/2+offset, self.size[1]/2]
# #         brown = "#A44B00"
# #         self.color = brown
# #         self.pos = [x, y]
# #         self.size = (25, 25)
# #         top = self.pos[1] - self.size[1]/2
# #         bottom = top + self.size[1]
# #         left = self.pos[0] - self.size[0]/2
# #         right = left + self.size[0]
# #         self.square = (left, top, right, bottom)
# #         self.direction = d
# #         self.fallHeight = 2
# #
# #     def collide(self, a, hitSide):
# #         if isinstance(a, PaperBrick):
# #             if hitSide == "left" or hitSide == "right":
# #                 self.direction = -self.direction
# #             elif hitSide == "notCollide" and self.square[3] < 430: # 435 is canvas height #####must change
# #                 self.fall()
# #
# #     def rotate(self):
# #         pass
# #
#     def draw(self, canvas):
#         canvas.create_oval(self.square, fill=self.color)
# #
# #     def updateSquare(self):
# #         top = self.pos[1] - self.size[1]/2
# #         bottom = top + self.size[1]
# #         left = self.pos[0] - self.size[0]/2
# #         right = left + self.size[0]
# #         self.square = (left, top, right, bottom)
# #
# #     def fall(self):
# #         self.pos[1] += self.fallHeight
# #
# #     def move(self, forwardSpeed=1.5):
# #         self.pos[0] += forwardSpeed*self.direction
#
# # class Mario(object):
# #     def __init__(self):
# #         dR = 9 # the ratio that image has decreased
# #         self.image = data.Data().loadSmallerImage("mario.gif", dR, dR)
# #         self.image_r = data.Data().loadSmallerImage("mario_r.gif", dR, dR)
# #         self.size = (max(self.image.width(), self.image_r.width()),
# #                      max(self.image.height(), self.image_r.height()))
# #         offset = 5
# #         self.pos = [self.size[0]/2+offset, self.size[1]/2]
# #         self.jumpHeight = 5
# #         self.isJumping = False
# #         self.isFalling = False
# #         self.jumpTime = 20
# #         self.hitLeft = False
# #         self.hitRight = False
# #         self.hitTop = False
# #         self.hitDown = False
# #         self.hitRock = False
# #
# #     def collide(self, a, direction):
# #         if direction == "left":
# #             if isinstance(a, PaperBrick):
# #                 self.hitLeft = True
# #             elif isinstance(a, Rock):
# #                 self.hitRock = True
# #         elif direction == "right":
# #             if isinstance(a, PaperBrick):
# #                 self.hitRight = True
# #             elif isinstance(a, Rock):
# #                 self.hitRock = True
# #
# #     def move(self, forwardSpeed=1):
# #         self.pos[0] += 1 * 50/(1000/20)
# #
# #     def jump(self):
# #         self.isJumping = True
# #         self.pos[1] -= self.jumpHeight
# #
# #     def fall(self):
# #         self.isFalling = True
# #         self.isJumping = False
# #         self.pos[1] += self.jumpHeight
#
# # class PaperBrick(object):
# #     def __init__(self, row, col, square):
# #         self.row = row
# #         self.col = col
# #         self.hit = False
# #         self.hasRock = False
# #         self.square = square
# #         num = random.randint(1, 10)
# #         if num < 2:
# #             self.setRock()
# #
# #     def setRock(self):
# #         self.hasRock = True
# #         distanceUpon = 25
# #         direction = random.choice([1, -1])
# #         assert(isinstance(direction, int))
# #         self.rock = Rock((self.square[0]+self.square[2])/2, (self.square[1]+self.square[3])/2-distanceUpon, direction)
# #
# #     def update(self):
# #         self.rock.updateSquare()
# #
# #     def __hash__(self):
# #         hashables = (self.row, self.col)
# #         return hash(hashables)
#
# # class Camera(object):
# #     def __init__(self, rows, cols, rowsWhole):
# #         self.rows = rows
# #         self.cols = cols
# #         self.forwardLength = 1  # 1 cell
# #         self.followingMarioH = False
# #         self.followingMarioV = False
# #         self.left = 0
# #         self.top = rowsWhole-self.rows
#
# class Stream(EventBasedAnimationClass):
#     # def __init__(self, rows=12, cols=20):
#     #     margin = 0
#     #     cellWidth, cellHight = 50, 88/3 # 88 is Mario's height
#     #     canvasWidth = 2*margin + cols*cellWidth
#     #     canvasHeight = 2*margin + rows*cellHight
#     #     super(Stream, self).__init__(canvasWidth, canvasHeight)
#     #     self.margin = margin
#     #     self.cellSize = (cellWidth, cellHight)
#     #     self.rowsWhole = 36
#     #     self.colsWhole = 480
#     #     self.camera = Camera(rows, cols, self.rowsWhole)
#
#     # def onKeyPressed(self, event):
#     #     if event.char == "r":  # restart game
#     #         self.initAnimation()
#     #     if not self.isGameOver:
#     #         if self.isPaused and event.char == "p":  # resume the game
#     #             self.isPaused = False
#     #         elif not self.isPaused:
#     #             if event.char == "p":  # pause the game
#     #                 self.isPaused = True
#     #             elif (not self.mario.isFalling) and (not self.mario.isJumping) \
#     #                     and (event.char == " "):  # Mario jump
#     #                 self.mario.jump()
#
#     # def onTimerFired(self):
#     #     if not self.isGameOver:
#     #         if not self.isPaused:
#     #             self.detectCollide()
#     #             if self.mario.hitRock:
#     #                 self.gameOver()
#     #             # mario moving forward
#     #             if (not self.mario.hitLeft) and (not self.mario.hitRight):
#     #                 self.count += 1
#     #                 self.mario.move()
#     #             if self.mario.isJumping and (not self.mario.hitDown):
#     #                 self.mario.jump()
#     #                 if self.mario.pos[1] + self.mario.jumpHeight*self.mario.jumpTime <= self.tempGroundPosHeight:
#     #                     self.mario.fall()
#     #             elif self.mario.isFalling and (not self.mario.hitTop):
#     #                 self.mario.fall()
#     #                 if self.mario.pos[1] >= self.groundPosHeight:
#     #                     self.mario.isFalling = False
#     #             # rock moving forward
#     #             for brick in self.bricks:
#     #                 if brick.hasRock:
#     #                     brick.rock.move()
#     #
#     #             self.setMarioSquare()
#     #             self.updateBrick()
#     #             self.marioBrickInteract()
#     #             self.camera.left += 0.1
#
#     # def detectCollide(self):
#     #
#     #     # a = brick and b = rock
#     #     for brick1 in self.bricks:
#     #         if not brick1.hit:
#     #             for brick2 in self.bricks:
#     #                 if brick2.hasRock:
#     #                     collideOnLeftOfA(brick1, brick2.rock)
#     #                     collideOnRightOfA(brick1, brick2.rock)
#     #
#     #     # detect if each rock has collided any bricks or not
#     #     for brick in self.bricks:
#     #         if brick.hasRock:
#     #             isNotCollideAnyBrick(self.bricks, brick.rock)
#     #
#     #     # a = rock and  b = mario
#     #     for brick in self.bricks:
#     #         if brick.hasRock:
#     #             collideOnRightOfA(brick.rock, self.mario)
#     #             collideOnLeftOfA(brick.rock, self.mario)
#
#     # def gameOver(self):
#     #     self.isGameOver = True
#     #
#     # def updateBrick(self):
#     #     for brick in self.bricks:
#     #         if brick.hasRock:
#     #             brick.update()
#     #
#     # def setBrickSquare(self, row, col):
#     #     margin = self.margin
#     #     cellSize = self.cellSize
#     #     left = margin + col * cellSize[0]
#     #     right = left + cellSize[0]
#     #     top = margin + row * cellSize[1]
#     #     bottom = top + cellSize[1]
#     #     square = (left, top, right, bottom)
#     #     return square
#     #
#     # def setMarioSquare(self):
#     #     left = self.mario.pos[0] - self.mario.size[0]/2
#     #     right = left + self.mario.size[0]
#     #     top = self.mario.pos[1] - self.mario.size[1]/2
#     #     bottom = top + self.mario.size[1]
#     #     self.mario.square = (left, top, right, bottom)
#
#     # def hit(self):
#     #     self.score += 1
#     #
#     # def hitLeft(self):
#     #     self.mario.hitLeft = True
#     #
#     # def hitRight(self):
#     #     self.mario.hitRight = True
#     #
#     # def hitTop(self):
#     #     self.mario.hitTop = True
#     #     self.mario.isFalling = False
#     #
#     # def hitDown(self):
#     #     self.mario.hitDown = True
#     #     if self.mario.isJumping and self.mario.pos[1] <= self.tempGroundPosHeight:
#     #         self.mario.fall()
#     #
#     # def marioBrickInteract(self):
#     #     posOffset = 2
#     #     self.mario.hitLeft = False
#     #     self.mario.hitRight = False
#     #     self.mario.hitTop  = False
#     #     self.mario.hitDown = False
#     #     for brick in self.bricks:
#     #         if ((not brick.hit)
#     #             and (brick.square[0] <= self.mario.square[0])
#     #             and (brick.square[2] >= self.mario.square[2])
#     #             and ((brick.square[1] < self.mario.square[1]+posOffset < brick.square[3]))):
#     #             self.hit()
#     #             brick.hit = True
#     #         elif ((brick.square[0]-2 <= self.mario.square[2] <= brick.square[0])
#     #               and (brick.square[1]-self.mario.size[1]+posOffset
#     #                        < self.mario.square[1] < brick.square[3]-posOffset)):
#     #             self.hitLeft()
#     #         elif ((brick.square[2]-2 <= self.mario.square[2] <= brick.square[2])
#     #               and (brick.square[1]-self.mario.size[1]+posOffset
#     #                        < self.mario.square[1] < brick.square[3]-posOffset)):
#     #             self.hitRight()
#     #         elif (brick.square[0]-self.mario.size[0] < self.mario.square[0] < brick.square[2]
#     #             and brick.square[1]-2 <= self.mario.square[3] <= brick.square[1]):
#     #             self.hitTop()
#     #             self.tempGroundPosHeight = self.groundPosHeight-(self.height-brick.square[1])
#     #             if brick.square[2]-posOffset < self.mario.square[0] < brick.square[2]+posOffset:
#     #                 self.mario.isFalling = True
#     #                 self.tempGroundPosHeight = self.groundPosHeight
#     #         elif (((brick.square[0]-self.mario.size[0] < self.mario.square[0] < brick.square[0])
#     #         or (brick.square[2]-self.mario.size[0] < self.mario.square[0] < brick.square[2]))
#     #             and (brick.square[3]-12 < self.mario.square[1] < brick.square[3]+12)):
#     #             self.hitDown()
#
#     # def redrawAll(self):
#     #     self.canvas.delete(ALL)
#     #     self.drawCamera()
#     #     if self.isGameOver:
#     #         cx = self.width/2
#     #         cy = self.height/2
#     #         self.canvas.create_text(cx, cy, text="Game Over!",
#     #                                 font=("Helvetica", 32, "bold"))
#
#     def drawBrick(self):
#         for brick in self.bricks:
#             if brick.hit:
#                 self.drawCell(brick.row-self.camera.top, brick.col-self.camera.left)
#             else:
#                 self.drawCell(brick.row-self.camera.top, brick.col-self.camera.left, "green")
#                 if brick.hasRock:
#                     brick.rock.draw(self.canvas)
#
#     def drawMario(self):
#         if self.count % 10 <= 4 or self.mario.hitLeft or self.mario.hitRight:
#             self.canvas.create_image(self.mario.pos[0], self.mario.pos[1], image=self.mario.image)
#         else:
#             self.canvas.create_image(self.mario.pos[0], self.mario.pos[1], image=self.mario.image_r)
#         self.canvas.create_text(self.mario.pos[0], self.mario.pos[1]-50, text=str(self.score)  )
#
#     # def drawCamera(self):
#     #     left, bottom = 0, self.rowsWhole
#     #     right, top = left+self.camera.cols, bottom-self.camera.rows
#     #     self.drawBoard(left, top)
#     #     print top
#
#     def drawBoard(self, left, top):
#         # draw background
#         self.canvas.create_rectangle(0, 0, self.width, self.height,
#                                 fill="orange", width=0)
#         rows, cols = self.camera.rows, self.camera.cols
#         for row in xrange(rows):
#             for col in xrange(cols):
#                 self.drawCell(row, col)
#
#         # draw Mario
#         self.drawMario()
#
#         # draw brick
#         self.drawBrick()
#
#     def drawCell(self, row, col, fill=None):
#         margin = self.margin
#         cellSize = self.cellSize
#         left = margin + col * cellSize[0]
#         right = left + cellSize[0]
#         top = margin + row * cellSize[1]
#         bottom = top + cellSize[1]
#         self.canvas.create_rectangle(left, top, right, bottom,
#                                      fill=fill, width=0)
#
#     def initAnimation(self):
#         # self.mario = Mario()
#         # self.score = 0
#         # self.groundPosHeight = self.height - self.mario.pos[1]
#         # self.tempGroundPosHeight = self.groundPosHeight
#         # self.mario.pos[1] = self.groundPosHeight
#         # self.rowCellPerMario = 3  # is the cells mario occupies
#         # self.board = [[None] * self.colsWhole for i in xrange(self.rowsWhole)]
#         # self.bricks = []
#         # bricksPos = []
#         # for i in xrange(80):  # need to change to modified by midi later
#         #     row = random.randint(0, self.rowsWhole-1-self.rowCellPerMario)
#         #     col = random.randint(0, self.colsWhole-1)
#         #     if not (row, col) in bricksPos:
#         #         square = self.setBrickSquare(row, col)
#         #         self.bricks += [PaperBrick(row, col, square)]
#         #         bricksPos += [(row, col)]
#         #
#         # row, col = self.rowsWhole-1, 2
#         # square = self.setBrickSquare(row, col)
#         # self.bricks += [PaperBrick(row, col, square)]
#         #
#         # row, col = self.rowsWhole-2, 3
#         # square = self.setBrickSquare(row, col)
#         # self.bricks += [PaperBrick(row, col, square)]
#         #
#         # row, col = self.rowsWhole-4, 0
#         # square = self.setBrickSquare(row, col)
#         # self.bricks += [PaperBrick(row, col, square)]
#         #
#         # row, col = self.rowsWhole-7, 4
#         # square = self.setBrickSquare(row, col)
#         # self.bricks += [PaperBrick(row, col, square)]
#         #
#         # def compareBricksByCol(a, b):
#         #     return (b.row - a.row) if (a.col - b.col) == 0 else (a.col - b.col)
#         # self.bricks = sorted(self.bricks, compareBricksByCol)
#         # self.setMarioSquare()
#         # # changed in onTimeFired to determine which image of mario should be used
#         # self.count = 0
#         # self.isPaused = False # set isPaused as False in the beginning
#         # self.timerDelay = 20
#         # self.isGameOver = False
#
# if __name__ == '__main__':
#     Stream().run()