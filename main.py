from pyautogui import screenshot,moveTo,click
from PIL import Image
from os import listdir

from random import randint
random = randint
def detectFiles():
    # 175% in google!!!!!!!!
    data = {}
    # window crop size- custom for sizes of match
    windowcrop = (405, 267, 1455, 827)
    # size of square in pixels
    tilesize = 35
    # tile width and height
    size = (16, 30)

    def getstatus(prnt=False):
        def getdata():
            for filename in listdir('C:\\Users\\castor\\Documents\\GitHub\\Minesweeper-bot\\tiles'):
                im = Image.open("tiles/" + filename)
                data[str(list(im.getdata()))] = [filename[:-4]]
                im.close()

        def getScreeshot():  # left up right low
            return (screenshot().crop(windowcrop))

        def slice(tilesize, tilenum, screenshot):
            ret = []
            for x in range(tilenum[0]):
                for y in range(tilenum[1]):
                    ret.append(screenshot.crop((tilesize * y, tilesize * x, tilesize * (y + 1), tilesize * (x + 1))))
            return ret


        screen = getScreeshot()
        stuff = slice(tilesize, size, screen)
        getdata()

        fixed = []
        currentfield = []
        x = 0
        for y in range(size[0]):
            currentfield.append([])
            for tile in range(size[1]):
                try:
                    currentfield[y].append(data[str(list(stuff[x].getdata()))])
                except KeyError:
                    return None
                x += 1

        def printfield():
            for x in currentfield:
                for y in x:
                    try:
                        print(int(y[0]), end=" ")
                    except ValueError:
                        print(y[0][0].upper(), end=" ")
                print("\n")

        for x in range(len(currentfield)):
            fixed.append([])
            for y in currentfield[x]:
                try:
                    fixed[x].append(int(y[0]))
                except ValueError:
                    fixed[x].append(y[0][0].upper())
        if prnt:
            printfield()

        return (fixed)

    def press(y,x):
        xpos = (405+tilesize/2)+(x*tilesize)
        ypos = (267+tilesize/2)+(y*tilesize)
        moveTo(xpos,ypos,0)
        click()

    def getClose(line, tile, stuff):
        close = []


        #zgoraj
        if (line > 0):
            close.append([line-1,tile])    #srednja
            if(tile > 0):    #levo
                close.append([line-1,tile-1])
            if(tile < len(stuff[0])-1):     #desno
                close.append([line-1,tile+1])
        #srednja
        if(True):
            if(tile > 0):       #levo
                close.append([line,tile-1])
            if(tile < len(stuff[0])-1):     #desno
                close.append([line,tile+1])
        #spodaj
        if(line != len(stuff)-1):
            close.append([line+1,tile])    #srednja
            if(tile > 0):    #levo
                close.append([line+1,tile-1])
            if(tile < len(stuff[0])-1):     #desno
                close.append([line+1,tile+1])


        return(close)

    def makeMatrix(stuff):
        #make empty
        mtrx = []
        numbers = []

        for x in range(len(stuff)):
            mtrx.append([])
            for y in range(len(stuff[x])):
                if(str(stuff[x][y]) in "87654321"):    #NUMBER  9
                    mtrx[x].append(9)
                    ln = len(numbers)
                    numbers.append([])
                    numbers[ln].append(stuff[x][y])
                    numbers[ln].append(x)
                    numbers[ln].append(y)
                elif(stuff[x][y] is 0):      #EMPTY    9
                    mtrx[x].append(9)
                elif(stuff[x][y] is 9):     #unknown   0
                    mtrx[x].append(0)

        for number in numbers:
            close = getClose(*number[1:],stuff)
            for tile in close:
                if(mtrx[tile[0]][tile[1]] != 9):
                    mtrx[tile[0]][tile[1]] = number[0]

        return mtrx

    def getsmallest(matrix):
        sm = 8
        ret = []
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if(matrix[x][y] != 0 and matrix[x][y] < sm):
                    sm = matrix[x][y]
        for x in range(len(matrix)):
            for y in range(len(matrix[x])):
                if(matrix[x][y] == sm):
                    ret.append([x,y])
        print(sm)
        return(ret)

    status = getstatus(prnt = False)
    if(status != None):
        for x in status:
            if("M" in x):
                click(933,210)
                status = getstatus()

        mtrx = makeMatrix(status)
        for x in mtrx:
            print()
            for y in x :
                print(y,end=" ")
        smallest = getsmallest(mtrx)
        if(smallest == []):
            press(8,15)
        else:
            x = random(0,len(smallest)-1)
            press(*smallest[x])
    else:
        print("wrong screenshot, restart")


for x in range(50):
    detectFiles()
