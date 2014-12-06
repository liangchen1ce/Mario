from interaction import Interaction
import data, random

class Mario(Interaction):
    def __init__(self, earthHeight, offsetForWindowHeight, cellSize):
        dR = 5 # the ratio that image has decreased
        self.dR = dR
        self.image_0 = data.Data().loadSmallerImage("MarioFrame0.gif", dR, dR)
        self.image_1 = data.Data().loadSmallerImage("MarioFrame1.gif", dR, dR)
        self.image_2 = data.Data().loadSmallerImage("MarioFrame2.gif", dR, dR)
        self.image_3 = data.Data().loadSmallerImage("MarioFrame3.gif", dR, dR)
        self.image_4 = data.Data().loadSmallerImage("MarioFrame4.gif", dR, dR)
        self.image_5 = data.Data().loadSmallerImage("MarioFrame5.gif", dR, dR)
        self.image_6 = data.Data().loadSmallerImage("MarioFrame6.gif", dR, dR)
        self.image_7 = data.Data().loadSmallerImage("MarioFrame7.gif", dR, dR)
        self.image_8 = data.Data().loadSmallerImage("MarioFrame8.gif", dR, dR)
        self.image_9 = data.Data().loadSmallerImage("MarioStand.gif", dR-2, dR-2)
        images = [self.image_0, self.image_1, self.image_2, self.image_3, self.image_4,
                  self.image_5, self.image_6, self.image_7, self.image_8, self.image_9]
        imagesWidth = []
        imagesHeight = []
        for i in xrange(9):
            width = images[i].width()
            imagesWidth += [width]
            height = images[i].height()
            imagesHeight += [height]
        self.cellSize = cellSize
        self.size = (max(imagesWidth)-20,
                     max(imagesHeight))
        offset = 5
        self.pos = [self.size[0]/2+offset, earthHeight-self.size[1]/2]
        self.windowPos = [self.pos[0], self.pos[1]-offsetForWindowHeight]
        super(Mario, self).__init__(self.pos, self.size)
        self.jumpHeight = 5
        self.jumpTime = 20
        self.forwardSpeed = 1
        self.score = 0
        self.currentGroundHeight = self.pos[1]
        self.isJumping = False
        self.isFalling = False
        self.isHanging = False
        self.hitRock = False
        self.hitTop = True  # This will reset every time use collide function
        self.hitNoBricks = True
        self.standOnEarth = True  # This won't reset

    def moveForward(self):
        self.pos[0] += self.forwardSpeed
        #print self.hitNoBricks

    def jump(self):
        self.isJumping = True
        self.pos[1] -= self.jumpHeight

    def fall(self):
        self.isFalling = True
        self.isJumping = False
        self.isHanging = False
        self.pos[1] += self.jumpHeight

    def collideOtherOnLeft(self, other):
        # if type(other) == Brick:
        #     self.hitBrickOnLeft = True
        pass

    def collideOtherOnRight(self, other):
        # if type(self) == Rock and type(other) == Brick:
        #     self.direction = -self.direction
        pass

    def collideOtherOnBottom(self, other):
        if type(other) == Brick and other.hit == False:
            self.score += 1
            other.hit = True

    def collideOtherOnTop(self, other):
        if (type(other) == Brick and other.hit == False) or type(other) == Earth:
            self.pos[1] = other.square[1] - self.size[1]/2
            self.hitTop = True
            self.currentGroundHeight = other.square[1]-self.size[1]/2
            self.isFalling = False
            self.standOnEarth = True
            # print "hit earth or brick"

    def collideOnOther(self, other):
        if type(other) == Earth and not self.hitTop:
            self.square = self.previousSquare
            self.pos = self.previousPos
            self.standOnEarth = True
            # print "earth stops me"
            # print "earth square:", other.square
            # print "Mario square:", self.square, "Mario pos", self.pos
        elif type(other) == Rock:
            self.hitRock = True
        elif type(other) == Brick and not other.hit and not self.hitTop:
            # print "Mario square:", self.square, "Mario pos", self.pos
            self.square = self.previousSquare
            self.pos = self.previousPos
            # print self.hitTop
            # print "Brick square:", other.square
            # print "Mario square:", self.square, "Mario pos", self.pos

    def collideNothing(self, others):
        if type(others) == list and type(others[0]) == Brick:
            self.hitNoBricks = True
        elif type(others) == Earth:
             self.standOnEarth = False

    def detect(self, bricks, earth):
        self.hitNoBricks = False
        self.collide(other=earth)
        for brick in bricks:
            if brick.hasRock:
                self.collide(other=brick.rock)
            if not brick.hit:
                self.collide(other=brick)
        self.collide(others=bricks)
        if not self.isFalling and not self.isJumping and not self.standOnEarth:
            if self.hitNoBricks:
                self.isHanging = True
                # print "guess what!"
                # print self.isFalling, self.isJumping, self.standOnEarth
                # print self.isFalling, self.isJumping, self.hitTop, self.hitNoBricks
                # self.fall()
        # if self.pos[1] < self.currentGroundHeight:
        #     self.isHanging = True
        #     print "hang!"
        # if self.hitNoBricks and self.currentGroundHeight != earth.square[1]-self.size[1]/2:
        #     self.fall()
        #     print "guess what?"
        #     print self.square
        # if not self.isFalling:
        #     newBricks = []
        #     for brick in bricks:
        #         # if there is no bricks, which are under Mario and has same col with Mario,
        #         # within a specific offset range of Mario, Mario is set to be hanging.
        #         if not brick.hit and brick.square[0] <= self.square[0] \
        #                 and brick.square[2] >= self.square[2]:
        #             newBricks += [brick]
        #     for brick in newBricks:
        #
        #                 and self.square[3]+8 >= brick.square[1] >= self.square[3]:
        #             return
        #         if self.currentGroundHeight == earth.square[1]-self.size[1]/2:
        #             return
        #     self.isHanging = True
        #     print "hang"

    def update(self):
        # just update square and position data
        self.previousSquare = self.square
        self.previousPos = self.squareToPos(self.previousSquare)
        top = self.pos[1] - self.size[1]/2
        bottom = top + self.size[1]
        left = self.pos[0] - self.size[0]/2
        right = left + self.size[0]
        self.square = (left, top, right, bottom)
        if (5+0.3*self.score) < self.cellSize[1]:
            self.jumpHeight = 5 + 0.5 * self.score

class Rock(Interaction):
    def __init__(self, cx, cy, d):
        brown = "#A44B00"
        self.color = brown
        pos = [cx, cy]
        size = (15, 15)
        super(Rock, self).__init__(pos, size)
        self.direction = d
        self.fallHeight = 2
        self.forwardSpeed = 1.5
        self.hitEarth = False
        self.hitNoBricks = False

    def fall(self):
        self.pos[1] += self.fallHeight

    def move(self):
        self.pos[0] += self.forwardSpeed*self.direction

    def collideOtherOnLeft(self, other):
        if type(other) == Brick:
            self.direction = -self.direction
            # print "Hit Brick Left!"

    def collideOtherOnRight(self, other):
        if type(other) == Brick:
            self.direction = -self.direction
            # print "Hit Brick Right"

    def collideOnOther(self, other):
        if type(other) == Earth:
            # print "illegal square:", self.square
            # self.square = self.previousSquare
            # self.pos = self.previousPos
            self.hitEarth = True
            # print "hit Earth!"
            # print "reseted square:", self.square

    def collideNothing(self, others):
        if type(others) == list and type(others[0]) == Brick:
            self.hitNoBricks = True

    def detect(self, bricks, earth):
        self.hitEarth = False
        self.hitNoBricks = False
        self.collide(other=earth)
        for brick in bricks:
            self.collide(other=brick)
        self.collide(others=bricks)
        if not self.hitEarth and self.hitNoBricks:
            self.fall()

    def update(self):
        # just update square and position data
        self.previousSquare = self.square
        self.previousPos = self.squareToPos(self.previousSquare)
        top = self.pos[1] - self.size[1]/2
        bottom = top + self.size[1]
        left = self.pos[0] - self.size[0]/2
        right = left + self.size[0]
        self.square = (left, top, right, bottom)

class Brick(Interaction):
    def __init__(self, row, col, cellSize, camera):
        self.row = row  # This is the row in background, not in window
        self.col = col
        cellWidth, cellHeight = cellSize[0], cellSize[1]
        pos = [(col+0.5)*cellWidth, (row+0.5)*cellHeight]
        super(Brick, self).__init__(pos, cellSize)

        left = self.square[0]
        top = self.square[1] - camera.top
        right = self.square[2]
        bottom = self.square[3] - camera.top
        self.windowSquare = [left, top, right, bottom]

        self.hit = False
        self.hasRock = False
        num = random.randint(1, 10)
        if num%10 < 1:
            self.setRock()

    def setRock(self):
        self.hasRock = True
        distanceUpon = 25
        direction = random.choice([1, -1])
        self.rock = Rock((self.square[0]+self.square[2])/2, (self.square[1]+self.square[3])/2-distanceUpon, direction)

class Earth(Interaction):
    def __init__(self, backgroundSize, camera):
        backgroundWidth = backgroundSize[0]
        backgroundHeight = backgroundSize[1]
        pos = [backgroundWidth/2, backgroundHeight+23]
        size = (backgroundWidth, 50)
        super(Earth, self).__init__(pos, size)
        left = self.square[0]
        top = self.square[1] - camera.top
        right = self.square[2]
        bottom = self.square[3] - camera.top
        self.windowSquare = [left, top, right, bottom]

class Camera(object):
    def __init__(self, rows, cols, rowsWhole, colsWhole, cellSize):
        # attributes from game
        self.rows = rows
        self.cols = cols
        self.rowsWhole = rowsWhole
        self.colsWhole = colsWhole
        self.cellSize = cellSize
        self.size = [self.cols*self.cellSize[0], self.rows*self.cellSize[1]]
        # attributes for camera
        self.forwardLength = 1 * cellSize[0]/(1000/20)  # at 20ms speed, camera move 1 cell every 1s
        self.Rolling = False
        self.endMessage = ["", ""]
        self.endMessagePos = [(0, 0), (0, 0)]
        self.endMessageWindowPos = [(0, 0), (0, 0)]
        self.left = 0
        self.top = (rowsWhole-self.rows) * cellSize[1]

    def moveForward(self):
        self.left += self.forwardLength

    def followingMarioV(self, mario):
        offsetHeight = (self.rowsWhole-self.rows)*self.cellSize[1] + 2.5
        if self.size[1]*0.4 <= mario.windowPos[1] <= self.size[1]*0.6:
            if 0 < mario.pos[1] - self.size[1]/2 < offsetHeight:
                self.top = mario.pos[1] - self.size[1]/2

    def update(self, mario):
        if self.left + self.size[0]/2 >= self.colsWhole*self.cellSize[0]:
            self.Rolling = False
            self.endMessage = ["THE", "END"]
            self.endMessagePos = [[self.colsWhole*self.cellSize[0]+self.size[0]/4, self.rowsWhole*self.cellSize[1]-3*self.size[1]/4],
                                  [self.colsWhole*self.cellSize[0]+self.size[0]/4, self.rowsWhole*self.cellSize[1]-self.size[1]/4]]
            self.endMessageWindowPos = [[self.endMessagePos[0][0]-self.left, self.endMessagePos[0][1]-self.top],
                [self.endMessagePos[1][0]-self.left, self.endMessagePos[1][1]-self.top]]
        elif mario.windowPos[0] >= self.size[0]/2:
            self.Rolling = True

        if self.Rolling:
            self.moveForward()

        self.followingMarioV(mario)