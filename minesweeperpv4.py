from pyautogui import *
from tkinter import *
from PIL import *
import time
import ait


global colors, direct, bads
colors = {
    (231, 57, 0):-2,
    (168, 208, 61):-1,
    (176, 214, 70):-1,
    (174, 206, 71):-1,
    (167, 199, 62):-1,#gues
    (226, 194, 156):0,
    (212, 184, 151):0,
    (119, 151, 190):1,
    (113, 147, 187):1,
    (171, 172, 125):2,
    (182, 180, 129):2,
    (218, 157, 128):3,
    (208, 150, 123):3,
    (208, 177, 151):4,
    (220, 187, 157):4,
    (246, 144, 0):5,#gues
    (246, 143, 0):5#gues
}
direct = [(0,-1),(1,-1),(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1)]
bads = [((0,-1),(0,1)), ((-1,0), (1,0)), ((0,1),(0,-1)), ((1,0),(-1,0))]


################################################################################
## returns integer value given a square:
# takes in a 25x25 img -> returns most likey value
# 0 = empty -> checked
# -1 = unvisited -> green square
# -2 = flag
def img_to_number(img):
    color = img.getpixel((10,8))
    try:
        color = colors[color]
    except:
        return 0
    return color


################################################################################
## Creates the board with a screenshot
def tile_array(board_data):
    screen = screenshot()

    x_0, y_0, d = board_data[0], board_data[1], board_data[4]
    tiles = []

    for y in range(0, board_data[3]):
        row = []
        for x in range(0, board_data[2]):
            box = (x_0 + x*25, y_0 + y*25, x_0 + (x+1)*25, y_0 + (y+1)*25)
            value = img_to_number(screen.crop(box))
            row.append(value)

        tiles.append(row)
    return tiles



def update_tiles(board_data, tiles):
    screen = screenshot()

    x_0, y_0, d = board_data[0], board_data[1], board_data[4]

    for y in range(0, board_data[3]):
        for x in range(0, board_data[2]):
            if(tiles[y][x] == -1 or tiles[y][x] == 0):
                box = (x_0 + x*25, y_0 + y*25, x_0 + (x+1)*25, y_0 + (y+1)*25)
                value = img_to_number2(screen.crop(box))
                tiles[y][x] = value

    return tiles

def in_range(x,y):
    if(x >= 0 and x < 24 and y >= 0 and y < 20):
        return True
    return False




################################################################################
##return the minimun and maximum flags in a set
# reurns min_flags, max flags
def minmaxset(x,y, dir1, dir2, tiles):
    dx = dir1[0] - dir2[0]
    dy = dir1[1] - dir2[1]

    ## There are no tiles overlapping both
    if((abs(dx) == 2 and abs(dy) == 2) or (dir1,dir2) in bads):
        return 0, 2

    ## There is one tile overlapping -> L shape
    elif(abs(dx) + abs(dy) == 3):
        Zx = x + (dir1[0] + dir2[0])
        Zy = y + (dir1[1] + dir2[1])

        if(abs(dir1[0]) + abs(dir1[1]) == 1):
            if(tiles[Zy + dir1[1]][Zx + dir1[0]] < 0):
                return 0, 2
        else:
            if(tiles[Zy + dir2[1]][Zx + dir2[0]] < 0):
                return 0, 2

        return minmaxpoint(Zy,Zx, tiles)

    ## There is one tile overlapping -> diagonal
    elif(abs(dy) == 1 and abs(dx) == 1):
        Zx = x + (dir1[0] + dir2[0])
        Zy = y + (dir1[1] + dir2[1])
        return minmaxpoint(Zy,Zx, tiles)


    ## There are two tiles overlapping -> line
    elif(abs(dx) + abs(dy) == 2):
        Zx = x + int((dir1[0] + dir2[0])/2)
        Zy = y + int((dir1[1] + dir2[1])/2)

        if(tiles[Zy - dir1[1]][Zx - dir1[0]] < 0 or tiles[Zy - dir2[1]][Zx - dir2[0]] < 0):
            min_2, max_2 = 0, 2
        else:
            min_2, max_2 = minmaxpoint(Zy,Zx, tiles)


        if(tiles[Zy][Zx] < 0):
            min_1, max_1 = 0,2
        else:
            Zx = x + (dir1[0] + dir2[0])
            Zy = y + (dir1[1] + dir2[1])
            min_1, max_1 = minmaxpoint(Zy,Zx, tiles)

        return max(0, min_1,min_2), min(2, max_1,max_2)





    ## There are three tiles overlapping -> next to eachother
    elif(abs(dir1[0]) + abs(dir1[1]) > abs(dir2[0]) + abs(dir2[1])):
        Zx = x + (dir1[0] - dir2[0])
        Zy = y + (dir1[1] - dir2[1])

        if(in_range(Zx - dir2[0], Zy - dir2[1])):
            if(tiles[Zy - dir2[1]][Zx - dir2[0]] < 0 or tiles[Zy - dir1[1]][Zx - dir1[0]] < 0):
                min_1, max_1 = 0, 2
            else:
                min_1, max_1 = minmaxpoint(Zy,Zx, tiles)
        else:
            min_1, max_1 = minmaxpoint(Zy,Zx, tiles)

        Zx = x + (dir1[0] + dir2[0])
        Zy = y + (dir1[1] + dir2[1])
        min_2, max_2 = minmaxpoint(Zy,Zx, tiles)

        Zx = x + dir2[0]*2
        Zy = y + dir2[1]*2
        if(in_range(Zx - dir1[0], Zy - dir1[1])):
            if(tiles[Zy - dir1[1]][Zx - dir1[0]] < 0):
                min_3, max_3 = 0, 2
            else:
                min_3, max_3 = minmaxpoint(Zy,Zx, tiles)
        else:
            min_3, max_3 = minmaxpoint(Zy,Zx, tiles)

        return max(0, min_1, min_2, min_3), min(2, max_1, max_2, max_3)


    elif(abs(dir1[0]) + abs(dir1[1]) < abs(dir2[0]) + abs(dir2[1])):
        Zx = x + (dir2[0] - dir1[0])
        Zy = y + (dir2[1] - dir1[1])
        if(in_range(Zx - dir1[0], Zy - dir1[1])):
            if(tiles[Zy - dir1[1]][Zx - dir1[0]] < 0 or tiles[Zy - dir2[1]][Zx - dir2[0]] < 0):
                min_1, max_1 = 0, 2
            else:
                min_1, max_1 = minmaxpoint(Zy,Zx, tiles)
        else:
            min_1, max_1 = minmaxpoint(Zy,Zx, tiles)



        Zx = x + (dir1[0] + dir2[0])
        Zy = y + (dir1[1] + dir2[1])
        min_2, max_2 = minmaxpoint(Zy,Zx, tiles)

        Zx = x + dir1[0]*2
        Zy = y + dir1[1]*2
        if(in_range(Zx - dir2[0], Zy - dir2[1])):
            if(tiles[Zy - dir2[1]][Zx - dir2[0]] < 0):
                min_3, max_3 = 0, 2
            else:
                min_3, max_3 = minmaxpoint(Zy,Zx, tiles)
        else:
            min_3, max_3 = minmaxpoint(Zy,Zx, tiles)

        return max(0, min_1, min_2, min_3), min(2, max_1, max_2, max_3)

    return 0,2



def minmaxpoint(Zy,Zx, tiles):
    if(in_range(Zx, Zy) == False or tiles[Zy][Zx] <= 0):
        return 0, 2

    flags = tiles[Zy][Zx]
    minflags = flags + 2

    for di in direct:
        if(in_range(Zx + di[0], Zy + di[1])):
            if(tiles[Zy + di[1]][Zx + di[0]] == -2):
                flags -= 1
                minflags -= 1
            if(tiles[Zy + di[1]][Zx + di[0]] == -1):
                minflags -= 1
    return max(0, minflags), min(2, flags)

################################################################################
## Returns tiles to mark/destroy around x,y
# in form of list of tuples with (x, y, op)
def markable_in_vicinity(x,y, tiles):


    around = []
    for di in direct:
        if(in_range(x+di[0], y+di[1])):
            around.append(tiles[y+di[1]][x+di[0]])
        else:
            around.append(0)

    num_flags = tiles[y][x]                 # Number of flags needed around x,y
    emptys = around.count(-1)               # Number of emtys around x,y
    flags_al = around.count(-2)             # Number of flags already aorund x,y

    # Mark the easy ones

    if(emptys == 0):
        return []
    if((num_flags - flags_al) == emptys):
        return(empty_in_around(around, 'f', x, y))
    if((num_flags - flags_al) == 0):
        return(empty_in_around(around, 'r', x, y))


    # Stop here for tiles with 2- or 6+ tiles
    if(emptys > 5 or emptys <= 2):
        return []



    e_i = []    # list of the indices of empty tiles
    for i in range(8):
        if(around[i] == -1):
            e_i.append(i)


    for i in range(len(e_i)): # for each pair of empty tiles -> next to eachother
        min_flags, max_flags = minmaxset(x,y, direct[e_i[i]], direct[e_i[i-1]], tiles)

        if(min_flags == 0 and max_flags == 2):
            pass
        elif(num_flags - flags_al - min_flags == 0):
                          # remove all non-subset empties
            around[e_i[i]] = 0
            around[e_i[i-1]] = 0
            return(empty_in_around(around, "r", x, y))
        elif(num_flags - flags_al - max_flags == emptys - 2):       # flag all non-subset empties

            around[e_i[i]] = 0
            around[e_i[i-1]] = 0
            return(empty_in_around(around, "f", x, y))

    return[]



## Helper -> returns list of stuff to do
# list of tuples -> (x,y,'op').
# for each empty tile around x,y -> with either 'r' or 'f'
def empty_in_around(around, op, x, y):
    ans = []
    for i in range(8):
        if(around[i] == -1):
            ans.append((x + direct[i][0],y + direct[i][1],op))
    return ans



################################################################################
## Mark/Destroy all tiles possible from the board
def mark_all_determinants(board_data):

    x_0, y_0 = board_data[0] + 10, board_data[1] + 10
    ait.move(510,585)
    ait.click()
    ait.move(x_0 + 12 * 25, y_0 + 10 * 25)
    sleep(0.01)
    ait.click()
    ait.move(510,585)
    ait.click()
    sleep(1)
    ait.click()
    sleep(0.05)

    to_do = [1]
    mines = 0
    while(len(to_do) != 0):

        tiles = tile_array(board_data)


        to_do = []

        # for each numbered tile -> add all in vicinity to to_do
        for y in range(len(tiles)):
            for x in range(len(tiles[0])):
                if(0 < tiles[y][x]):
                    to_add = markable_in_vicinity(x,y, tiles)
                    for e in to_add:
                        if(e not in to_do):
                            to_do.append(e)


        # mark everything in to_do
        for to_mark in to_do:
            ait.move(x_0 + to_mark[0] * 25, y_0 + to_mark[1] * 25)
            if(to_mark[2] == 'f'):
                ait.click("R")
                mines += 1
            else:
                ait.click()
        if(mines == 99):
            return
            #tiles = tile_array(board_data)
            sc = screenshot()
            if(sc.getpixel((885, 488)) == (242, 242, 242)):
                return


        ait.move(510,585)
        ait.click()
        sleep(1)
        ait.click()
        sleep(0.05)

################################################################################
def mark_all_open(board_data):
    x_0, y_0 = board_data[0] + 10, board_data[1] + 10
    tiles = tile_array(board_data)
    to_do = []
    for y in range(len(tiles)):
        for x in range(len(tiles[0])):
            if(-1 == tiles[y][x]):
                to_do.append((x,y,'r'))

    for to_mark in to_do:
        ait.move(x_0 + to_mark[0] * 25, y_0 + to_mark[1] * 25)
        ait.click()



def run():
    board_data = [652, 352, 24, 20, 25]
    mark_all_determinants(board_data)


if __name__ == "__main__":


    root = Tk()
    root.geometry('500x100')
    root.title("The Broom")
    root.wm_attributes("-topmost", 1)
    root.btn = Button(root, text = "Do thing", command=run)
    root.btn.grid(row=1,column=1)
    root.mainloop()


