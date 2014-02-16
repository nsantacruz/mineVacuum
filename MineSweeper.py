#UPDATES#
#adjacent arrays now update for both bs and us each time a space is clicked (still needs a bit of work)
#updated to agree with rest of world: the (row, column) standard has been adopted

from Square import *
from GridVisualizer import *
from pseudocode import *
import random
import time
class MineSweeper():
	def __init__(this,wid=None,hei=None,mines=None,difficulty=None):
		this.grid = []
		this.foundMine = False # used to alert game when you lose, hope to never have to use it...
		this.numRevealed = 0 # you win when numRevealed = w * h - totalMines
		this.mines = []
		this.startedGame = False
		if (wid and hei and mines):
			this.h = hei
			this.w = wid
			this.numMines = mines
			this.totalMines = mines
		elif not difficulty is None:
			if difficulty is 0:
				this.h = 9
				this.w = 9
				this.numMines = 10
			elif difficulty is 1:
				this.h = 16
				this.w = 16
				this.numMines = 40
			elif difficulty is 2:
				this.h = 30
				this.w = 16
				this.numMines = 99
			this.totalMines = this.numMines
		for y in range(this.w):
			this.grid.append([])
			for x in range(this.h):
				tempSq = Square(0,vis=False)
				tempSq.setPosition(x,y)
				this.grid[y].append(tempSq)
				
	def addMines(this,x,y): #parameters signify spot that was clicked, don't add mines around it
		minesToPlace = this.numMines
		while(minesToPlace>0):
			randY = random.randint(0,this.h-1)
			randX = random.randint(0,this.w-1)
			if this.grid[randX][randY].number != -1 and not (randY in range(y-1,y+2) and randX in range(x-1,x+2)):
				tempMine = Square(-1)
				tempMine.setPosition(randX,randY)
				this.mines.append(tempMine)
				this.grid[randX][randY] = tempMine
				minesToPlace-=1

	def addNumbers(this):
		for mine in this.mines:
			mineX = mine.position[0]
			mineY = mine.position[1]
			#print(mine.number)
			for pos in this.getSurroundingPositions(mineX,mineY):
				if this.grid[pos[0]][pos[1]].number != -1:
					this.grid[pos[0]][pos[1]].number+=1
								
	def chooseSpace(this,x,y):
		#if first click, add mines but not around spot that was clicked
		if not this.startedGame:
			this.addMines(x,y)
			this.addNumbers()
			this.startedGame = True
		revealed = this.revealSpace(x,y)
		this.numRevealed += len(revealed)
		this.updateAdjacent(revealed)
	
	def flagSpace(this,x,y):
		tempSq = this.grid[x][y]
		tempSq.flagged = True
		this.numMines -= 1
	
	def useSolutions(this,solArray):
		for clickMe in solArray[0]:
			this.chooseSpace(clickMe[0],clickMe[1])
		for flagMe in solArray[1]:
			this.flagSpace(flagMe[0],flagMe[1])
	# a cool recursive function, but I think it's a bit too lenient when it comes 
	#to revealing squares, maybe that's just me...
	#prevRevealedTiles is a parameter used to pass the revealedTiles list between 
	#different levels of the functions recursion. Pretty cool...
	#returns a list of revealed tiles, usefule for solving hopefully
	def revealSpace(this,x,y,prevRevealedList=None):
		tempSq = this.grid[x][y]
		if prevRevealedList:
			revealedList = prevRevealedList
		else:
			revealedList = []
		if not (tempSq.visible or tempSq.flagged):
			if tempSq.number == -1:
				# print('Game Over :(')
				this.foundMine = True
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
					tempSq = this.grid[pos[0]][pos[1]]
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
				tempSq = this.grid[pos[0]][pos[1]]
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
	
	def hasWon(this):
		# check out error as to why sometimes it doesnt' recognize that all tiles are revealed. It's really annoying. ps I'm tired...
		if (this.numRevealed == ((this.w * this.h) - this.totalMines)):
			return True
		# elif this.numMines is 0 :
		# 	# print(this.numRevealed,'    ',this.w * this.h - this.totalMines)
		# 	return True
		else:
			return False
	def hasLost(this):
		if this.foundMine:
			return True
		else:
			return False
class AwesomeSauce():
	def __init__(this,numTrials):
		for k in range(0,1):
			for j in range(2):
				this.numSuGue = 0
				this.totNumGue = 0
				totalWins = 0
				this.numRevealed = 0
				stT = time.time()
				for i in range(numTrials):
					result = this.test(j)
					if i % 100 is 0:
						# print("only ", numTrials - i, " games left!")
						None
					totalWins += result
				totT = time.time() - stT
				print("wow you're slow. Took you ",round(totT/60,4)," minutes!")
				# perc = round(totalWins/numTrials * 100,4)
				# gPerc = round(this.numSuGue/this.totNumGue * 100,4)
				if k is 0:
					rPerc = round(this.numRevealed/(numTrials*(9*9 - 10)) * 100,4)
					print("BEGINNER")
				elif k is 1:
					rPerc = round(this.numRevealed/(numTrials*(16*16 - 40)) * 100,4)
					print("MEDIUM")
				elif k is 2:
					rPerc = round(this.numRevealed/(numTrials*(16*30 - 99)) * 100,4)
					print("EXPERT")


				# print(perc,"% of the time you're a winner :)")
				# print(gPerc,"% of the time you guessed correctly!")
				print(rPerc,"% of mines revealed!")

	def test(this,choice):
		ms = MineSweeper(difficulty=0)
		if choice is 0:
			ms.chooseSpace(round(ms.w/2),round(ms.h/2))
		elif choice is 1:
			ms.chooseSpace(0,0)
		pc = pseudocode()
		#print(len(ms.grid[0][2].adjacent))
		stepNum = 1
		start_time = time.time()
		while (not ms.hasWon() and not ms.hasLost()):
			msArray = makeArray(ms)
			solutions = pc.solveForGrid(msArray,ms.numMines)
			# if (len(solutions[0]) or len(solutions[1])) is 0:
			# 	continue
			ms.useSolutions(solutions)
			# makeGUI(ms.w,ms.h)
			print('NUM MINES = ', ms.numMines,'       STEP NUM = ',stepNum)
			print(visualize(ms))
			stepNum+=1
		elapsed_time = round((time.time() - start_time) * 1000)/1000
		# print('nssbox, it took you ', elapsed_time,' seconds but it was worth it!') 
		this.numRevealed += ms.numRevealed
		if ms.hasWon():
			# print('wow...that actually worked!')		
			this.numSuGue += pc.numGuesses
			this.totNumGue += pc.numGuesses
			return 1
		elif ms.hasLost():
			# print('but...but you"re a robot, how could you fail me!!??')
			this.numSuGue += (pc.numGuesses - 1)
			this.totNumGue += pc.numGuesses
			return 0
yo = AwesomeSauce(1)
