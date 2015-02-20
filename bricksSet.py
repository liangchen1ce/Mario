import os

def chooseBrickSet(choice, rowsWhole):
    defaultList = [(rowsWhole-6, 0), (rowsWhole-5, 1), (rowsWhole-5, 2), (rowsWhole-1, 2), (rowsWhole-2, 3), (rowsWhole-7, 4),
        (rowsWhole-8, 4), (rowsWhole-6, 5), (rowsWhole-1, 6), (rowsWhole-2, 7), (rowsWhole-3, 8), (rowsWhole-1, 9),
        (rowsWhole-3, 9), (rowsWhole-4, 10), (rowsWhole-2, 11), (rowsWhole-2, 12),
        (rowsWhole-2, 10), (rowsWhole-8, 11), (rowsWhole-12, 11), (rowsWhole-9, 12), (rowsWhole-9, 13), (rowsWhole-8, 14),
        (rowsWhole-8, 15), (rowsWhole-10, 16), (rowsWhole-12, 17), (rowsWhole-15, 18),
        (rowsWhole-8, 19), (rowsWhole-1, 20), (rowsWhole-2, 21), (rowsWhole-3, 22), (rowsWhole-1, 23)]
    if choice == "demo":
        return defaultList
    elif choice == "default":
        PlayGameSongList = [(rowsWhole-6, 0), (rowsWhole-5, 1), (rowsWhole-5, 2), (rowsWhole-1, 2), (rowsWhole-2, 3), (rowsWhole-7, 4),
        (rowsWhole-8, 4), (rowsWhole-6, 5), (rowsWhole-1, 6), (rowsWhole-2, 7), (rowsWhole-3, 8), (rowsWhole-1, 9),
        (rowsWhole-3, 9), (rowsWhole-4, 10), (rowsWhole-2, 10)]
        bricks = readBricks("bricksDefault")
        cols = len(bricks)/4
        rows = 4
        for row in xrange(rows):
            for col in xrange(cols):
                brickPos = (rowsWhole-int(bricks[4*row+col]), col+11)
                if not brickPos in PlayGameSongList:
                    PlayGameSongList += [brickPos]
        maxCols = cols+10
        return PlayGameSongList, maxCols

# from lecture note
def readFile(filename, mode="rt"):

        with open(filename, mode) as fin:
            return fin.read()

def readBricks(fileName):
    path = "data" + os.sep + fileName + ".txt"
    bricks = readFile(path).split()
    return bricks