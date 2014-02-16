#UPDATES#
#adjacent arrays now update for both bs and us each time a space is clicked (still needs a bit of work)
#updated to agree with rest of world: the (row, column) standard has been adopted

from Square import *
from GridVisualizer import *
import random
class MineSweeper():
	def __init__(this,wid=9,hei=9,mines=10):
		this.grid = []
		this.numMines = mines
		this.mines = []
		this.startedGame = False
		this.h = hei
		this.w = wid
		for y in range(wid):
			this.grid.append([])
			for x in range(hei):
				tempSq = Square(0,vis=False)
				tempSq.setPosition(x,y)
				this.grid[y].append(tempSq)
				
	def addMines(this,x,y): #parameters signify spot that was clicked, don't add mines around it
		minesToPlace = this.numMines
		while(minesToPlace>0):
			randY = random.randint(0,this.h-1)
			randX = random.randint(0,this.w-1)
			if this.grid[randY][randX].number != -1 and not (randY in range(y-1,y+2) and randX in range(x-1,x+2)):
				tempMine = Square(-1)
				tempMine.setPosition(randX,randY)
				this.mines.append(tempMine)
				this.grid[randY][randX] = tempMine
				minesToPlace-=1

	def addNumbers(this):
		for mine in this.mines:
			mineX = mine.position[0]
			mineY = mine.position[1]
			#print(mine.number)
			for pos in this.getSurroundingPositions(mineX,mineY):
				if this.grid[pos[1]][pos[0]].number != -1:
					this.grid[pos[1]][pos[0]].number+=1
								
	def chooseSpace(this,x,y):
		#if first click, add mines but not around spot that was clicked
		if not this.startedGame:
			this.addMines(x,y)
			this.addNumbers()
			this.startedGame = True
		revealed = this.revealSpace(x,y)
		this.updateAdjacent(revealed)
	# a cool recursive function, but I think it's a bit too lenient when it comes 
	#to revealing squares, maybe that's just me...
	#prevRevealedTiles is a parameter used to pass the revealedTiles list between 
	#different levels of the functions recursion. Pretty cool...
	#returns a list of revealed tiles, usefule for solving hopefully
	def revealSpace(this,x,y,prevRevealedList=None):
		tempSq = this.grid[y][x]
		if prevRevealedList:
			revealedList = prevRevealedList
		else:
			revealedList = []
		if not (tempSq.visible or tempSq.flagged):
			if tempSq.number == -1:
				print('Game Over :(')
			#if you found a 0, you can safely reveal all surrounding tiles
			elif tempSq.number == 0:
				tempSq.visible = True
				revealedList.append(tempSq)
				for pos in this.getSurroundingPositions(x,y):
					this.revealSpace(pos[0],pos[1],prevRevealedList=revealedList)
			else: #number is 1-8
				tempSq.visible = True
				revealedList.append(tempSq)
		#print(len(revealedList)) watch as it grows!
		return revealedList
	#uses list of squares that were just revealed to update adjacent arrays of 
	#both the bs and us. first loop through bs, cause that's what you have
	#while looping, keep track of us so you can loop through them afterward
	def updateAdjacent(this,revealedSqs):
		unrevealedList = []
		#border squares
		for bs in revealedSqs:
			if bs.number == 0:
				continue
			else:
				xPos = bs.position[0]
				yPos = bs.position[1]
				for pos in this.getSurroundingPositions(xPos,yPos):
					tempSq = this.grid[pos[1]][pos[0]]
					if not tempSq.visible:
						bs.addAdj(tempSq)
						#make sure this is not already in the unrevealedList
						if not tempSq in unrevealedList:
							unrevealedList.append(tempSq)
						
		#unrevealed squares
		for us in unrevealedList:
			xPos = us.position[0]
			yPos = us.position[1]
			for pos in this.getSurroundingPositions(xPos,yPos):
				tempSq = this.grid[pos[1]][pos[0]]
				if tempSq.visible:
					us.addAdj(tempSq)
						
	# give it a x,y position and it returns all the valid positions directly adjacent	
	def getSurroundingPositions(this,X,Y):
		posList = []
		for y in range(Y-1,Y+2):
			if y >= 0 and y < this.h:
				for x in range(X-1,X+2):
					if x >= 0 and x < this.w:
						posList.append((x,y))
		return posList
ms = MineSweeper(wid=9,hei=9, mines=10)
ms.chooseSpace(0,0)
#print(len(ms.grid[0][2].adjacent))
visualize(ms)
