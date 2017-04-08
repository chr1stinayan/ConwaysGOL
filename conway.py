from Tkinter import *
import copy

def createGrid(canvas, width, height):
    for x in range(0,700, width):
        canvas.create_line(x, 0, x, 600, fill="#05f")
    for y in range(0, 700, height):
      canvas.create_line(0, y, 600, y, fill="#000")
    return canvas

def updateGrid(canvas, grid, x_size, y_size, genText, currentGenNo, maxGenNo, master):
    canvas = createGrid(canvas, x_size, y_size)
    genText.set("Generation " + str(currentGenNo))
    grid = generation(grid)
    for i in range(0, len(grid)):
        for j in range(0, len(grid[0])):
            if grid[i][j] == 1:
                canvas.create_rectangle(j*x_size, i*y_size, (j+1)*x_size, (i+1)*y_size, fill="#05f")
            else:
                canvas.create_rectangle(j*x_size, i*y_size, (j+1)*x_size, (i+1)*y_size, fill="#fff")
    currentGenNo += 1
    if currentGenNo == maxGenNo:
        genText.set("Generation " + str(currentGenNo) + " - Done Iterating")
    else:
        master.after(1000, updateGrid, canvas, grid, x_size, y_size, genText, currentGenNo, maxGenNo, master)


def generation(grid):
    rows = len(grid)
    cols = len(grid[0])
    newGrid = copy.deepcopy(grid) #prevent aliasing
    numNeighbours = 0
    for i in range(0, rows):
        for j in range(0, cols):
            numNeighbours = findNeighbours(grid, i, j)
            if grid[i][j] == 0: #if cell is dead
                if numNeighbours == 3:
                    newGrid[i][j] = 1
            else: #cell is alive
                if numNeighbours < 2 or numNeighbours > 3:
                    newGrid[i][j] = 0
    return newGrid

def findNeighbours(grid, x, y): #fin ds number of live neighbours
    #cells contains all the neighbours in a grid
    cells = [(x-1, y-1), (x-1, y), (x-1, y+1), (x, y-1), (x, y+1), (x+1, y-1), (x+1, y), (x+1, y+1)]
    validNeighbours = []
    for i in cells: #check if neighbour is within bounds of the grid
        (x, y) = i
        if (x > -1 and x < len(grid)) and (y > -1 and y < len(grid[0])):
            validNeighbours.append((x, y))
    numNeighbours = 0
    if len(validNeighbours) > 0:
        for x, y in validNeighbours:
            if grid[x][y] == 1:
                numNeighbours += 1
    return numNeighbours

def fileToGrid(filePath):
    grid = []
    with open(filePath) as input:
        for line in input:
            newLine = [ch for ch in list(line) if ch!=' ' and ch != '\n']
            strippedLine = []
            i = 0
            length = len(newLine)
            while i < length and newLine[i] != '\n':
                strippedLine.append(int(newLine[i]))
                i += 1
            if strippedLine != []:
                grid.append(strippedLine)
    digits = grid[0] # file IO splits digits in number of generations
    strDigits = ''
    for digit in digits:
        strDigits += str(digit)
    grid[0] = int(strDigits) #joins digits of first line back together to get number of generations
    return grid

def main():
    grid = fileToGrid('in.txt')
    numGenerations = grid[0]
    grid = grid[1:]
    index = 1
    master = Tk()
    master.title('Conway\'s Game of Life')
    canvas_width = 600
    canvas_height = 600
    x_size = canvas_height/len(grid[0])
    y_size = canvas_width/len(grid)
    genText = StringVar()
    label = Label(master, textvariable=genText, fg='blue', font="Verdana 18 bold")
    label.pack()
    labelCanvas = Canvas(master, width=100, height=80)
    labelCanvas.pack()
    gridCanvas= createGrid(Canvas(master, width=canvas_width, height=canvas_height), x_size, y_size)
    gridCanvas.pack()
    updateGrid(gridCanvas, grid, x_size, y_size, genText, 1, numGenerations, master)
    master.mainloop()
main()


