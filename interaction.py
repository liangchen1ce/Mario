class Interaction(object):
    def __init__(self, pos, size):
        self.dR = 0 # to separate Mario class and others
        # pos = [x, y] in background
        # size = [width, height] of the object
        self.pos = pos
        self.size = size
        top = self.pos[1] - self.size[1]/2
        bottom = top + self.size[1]
        left = self.pos[0] - self.size[0]/2
        right = left + self.size[0]
        self.square = (left, top, right, bottom)
        self.previousSquare = self.square
        self.previousPos = self.pos

    def collide(self, other=None, others=None):
        offset = 3
        if (other == None and others == None) or (other != None and others != None):
            raise ValueError("collide method must have one optional argument.")

        pointUL = (self.square[0], self.square[1])
        pointUR = (self.square[2], self.square[1])
        pointDL = (self.square[0], self.square[3])
        pointDR = (self.square[2], self.square[3])
        points = [pointUL, pointUR, pointDL, pointDR]
        self.hitTop = False
        self.hitBrickOnLeft = False

        if isinstance(other, Interaction):
            ########space for debug
            # print "other square", other, other.square
            # print "self square", self, self.square
            # print "self size", self, self.size
            # print "first:", other.square[0]-offset <= self.square[2] <= other.square[0]
            # print "second:", other.square[1]-self.size[1] < self.square[1] < other.square[3]
            # # print "third:", self.previousSquare[3] < other.square[1] < self.square[3]

            ########collideOnLeftOfA
            #
            # Because Mario will only move at 1pixel/tick(relative with background),
            # bricks are stationary and rocks move 1.5p/tick(relative with background),
            # we just write a simple version with offset of 3 pixeles
            #
            # one condition:
            # a = rock and  b = brick
            if ((other.square[0]-offset <= self.square[2] <= other.square[0])
            and (other.square[1]-self.size[1] < self.square[1] < other.square[3])):
                self.collideOtherOnLeft(other)

            elif ((other.square[2]-offset <= self.square[0] <= other.square[2])
            and (other.square[1]-self.size[1] < self.square[1] < other.square[3])):
                self.collideOtherOnRight(other)

            ########collide on downside
            #
            # we will count previous pos of mario into consideration,
            # cause mario sometimes will jump out our judgement
            #
            # one condition:
            # self = mario, other = self
            elif (other.square[0]-self.size[0] <= self.square[0]
            and other.square[2]+self.size[0] >= self.square[2]
            and self.square[1] < other.square[3] < self.previousSquare[1]):
                self.collideOtherOnBottom(other)

            elif (other.square[0]-self.size[0] <= self.square[0]
            and other.square[2]+self.size[0] >= self.square[2]
            and self.previousSquare[3]-6 <= other.square[1] <= self.square[3]):
                self.collideOtherOnTop(other)

            ########not collideOnOther in every possibility
            #
            # many conditions:
            # 1. rock hit mario
            # 2. rock hit earth
            # 3. mario hit earth
            # 4. rock hit brick(no effect)
            # 5. rock hit brick(no effect)
            # 6. brick hit mario(no effect)
            # etc.
            for point in points:
                if self.overLap(self, other):
                    self.collideOnOther(other)
                    return
            self.collideNothing(other)

        #######not collide on others in every possibility
        #
        # again, we don't consider the situation that objects right throw the other in one time,
        # cause we only set jump height as 5pixels/tick.
        #
        # There are two conditions:
        # 1. self = mario, others = bricks
        # 2. self = rock, others = bricks
        elif isinstance(others, list):
            newBrickList = []
            for brick in others:
                if not brick.hit:
                    newBrickList += [brick]
            for brick in newBrickList:
                # if brick.col == 3:
                #     print brick.square
                if self.dR == 5:
                    offset = 3
                if self.overLap(self, brick, offset=offset):
                    return
            self.collideNothing(others)

    @staticmethod
    def isInside(a, point):
        # a is an object, point is a tuple
        if a.square[0] < point[0] < a.square[2] and a.square[1] < point[1] < a.square[3]:
            return True

    @staticmethod
    def overLap(a, b, offset=0):
        # have same line included
        if not a.square[0]-offset > b.square[2] and not a.square[2]+offset < b.square[0] \
                and not a.square[1]-offset > b.square[3] and not a.square[3]+offset < b.square[1]:
            return True

    @staticmethod
    def squareToPos(square):
        left = square[0]
        top = square[1]
        right = square[2]
        bottom = square[3]
        cx = (left + right)/2.0
        cy = (top + bottom)/2.0
        return [cx, cy]

    def collideOtherOnLeft(self, other):
        pass

    def collideOtherOnRight(self, other):
        pass

    def collideOtherOnBottom(self, other):
        pass

    def collideOtherOnTop(self, other):
        pass

    def collideOnOther(self, other):
        pass

    def collideNothing(self, other):
        if isinstance(other, list):
            # not collide on bricks
            pass
        elif isinstance(other, Interaction):
            # not collide on single object
            pass