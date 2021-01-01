from pyautogui import screenshot as pyautogui_ss
from pyautogui import moveTo
from pyautogui import click as mouseClick
from PIL import Image, ImageChops
import win32gui
from time import sleep
from pathlib import Path

class Screen:
    #gameSize[(x,y) tuple]
    #tileSize[integer]
    #tiles[{index: Image} dict]
    #coords[(
    #verbosemap[{index: stringtoprint} dict]
    def __init__(self, gameSize, tileSize):
        self.gameSize = gameSize
        self.tileSize = tileSize
        self.tiles = {}
        self.verboseMap = {}
        self.matrix = []
        self.coords = ()

        self.__windowRect()
        self.__load()
        # f = 0
        # for x in self.__slice(self.gameSize, self.tileSize):
        #     f+=1
        #     x.save(str(f)+".png")

    # finds the minesweeper window and gets the coordinates
    def __windowRect(self, name="Minesweeper", cut=(19, 127, -14, -13)):
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                if (win32gui.GetWindowText(hwnd) == name):
                    global coords
                    coords = win32gui.GetWindowRect(hwnd)
                    coords = tuple(coords[x] + cut[x] for x in range(4))
                    self.coords = coords
        win32gui.EnumWindows(winEnumHandler, None)

    #returns a screenshot of the screen
    def __screenshot(self, sleeptime=0):

        sleep(sleeptime)
        return(pyautogui_ss().crop(box=self.coords))

    #generator that yields slices of the screen
    def __slice(self, gameSize, tileSize):
        im = self.__screenshot()
        for x in range(gameSize[1]):
            for y in range(gameSize[0]):
                yield im.crop((tileSize * y, tileSize * x, tileSize * (y + 1), tileSize * (x + 1)))

    #loads tile images into memory
    def __load(self, tilenum=13, path = "\\tiles\\"):
        path = str(Path(__file__).parent) + path
        for x in range(tilenum):
            with Image.open(path + str(x) + ".png") as im:
                self.tiles[str(x)] = im.convert("RGB")
        self.verboseMap = dict(zip(range(tilenum), range(tilenum)))
        self.verboseMap[12] = "f"
        self.verboseMap[9] = "x"
        self.verboseMap[10] = "m"
        self.verboseMap[11] = "k"

    #detect cell type from image
    def __detect(self, cell, cutoff=50):
        cell = cell.convert("RGB")

        for tilei in self.tiles:
            found = True
            difference = ImageChops.difference(cell, self.tiles[tilei])
            for x in set(difference.getdata()):
                if((x[0] + x[1] + x[2]) > 3*cutoff):
                    found = False
            if(found):
                return tilei
    #generates 2d matrix corresponding to the minesweeper field
    def genMatrix(self, verbose = False):
        self.matrix = []
        gen = self.__slice(self.gameSize, self.tileSize)
        for y in range(self.gameSize[1]):
            self.matrix.append([])
            for x in range(self.gameSize[0]):
                self.matrix[y].append( self.__detect(next(gen)))
        if(verbose):
            for y in self.matrix:
                for x in y:
                    print(self.verboseMap[int(x)], end=" ")
                print("")
            print("\n\n\n")
    def press(self, y, x):
        y-=1
        x-=1
        xpos = self.coords[0] + self.tileSize//2 + x*self.tileSize
        ypos = self.coords[1]+ self.tileSize//2 + y*self.tileSize
        print(xpos, ypos)
        moveTo(xpos, ypos, 0)
        mouseClick()
if __name__ == "__main__":
    screen = Screen((9,9), 20)
    screen.press(5,8)

