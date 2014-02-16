from tkinter import *
from tkinter import ttk
from time import sleep
def visualize(g):
    gridString=""
    for y in range(len(g.grid)):
        string=""
        for x in range(len(g.grid[y])):
            tempSq = g.grid[y][x]
            if tempSq.visible:
                string += str(tempSq.number) + '  '
                #print(tempSq.number)
            elif tempSq.flagged:
                string+='!  '
            else:
                string+='#  '
        gridString+= (string + '\n')
    return gridString

def makeArray(g):
    array = [[0 for j in range(len(g.grid[0]))] for i in range(len(g.grid))] #crazy stuff...
    for y in range(len(g.grid)):
        for x in range(len(g.grid[y])):
            tempSq = g.grid[y][x]
            if tempSq.visible:
                array[y][x] = tempSq.number
            elif tempSq.flagged:
                array[y][x] = '!'
            else:
                array[y][x] = '#'
    return array
root = 0
lableArray = []
def makeGUI(w,h):
	global root
	global lableArray
	lableArray = [[] for i in range(w)]
	root = Tk()
	root.title("yo")

	mainframe = ttk.Frame(root, padding="3 3 12 12")
	mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)
	for i in range(w):
		for j in range(h):
			tempVar = StringVar()
			l = ttk.Label(mainframe,textvariable=tempVar)
			l.pack()
			lableArray[i].append(tempVar)
	# root.mainloop()
def updateGUI(g):
	global root
	global lableArray
	sleep(1)
	array = makeArray(g)
	for i in range(len(array)):
		for j in range(len(array[0])):
			tempSq = array[i][j]
			tempLabel = lableArray[i][j]
			tempLabel.set(tempSq)
	root.update_idletasks()

 
