#Cool. Please ask if anything's unclear, since I wrote this while half-asleep
#UPDATED: Probability is almost done. 
#Now able to generate binary equations for matrix (see getEquation())
#class pseudocode():
#return array of double array
#[0] array of positions to click
#[1] array of positions to flag
from Square import *
import random
class pseudocode():
	def __init__(this):
		this.numGuesses = 0 #for testing, totally legit
		
	def solveForGrid(this,currGrid,numMines):
		#dimensions of grid
		w,h = (len(currGrid),len(currGrid[0]))
		
		solutions = [[] for i in range(2)] #cool syntax
			
		#update Square.adjacent property
		bsArray = this.getBorderSquares(currGrid,w,h)
		#This and the accompanying US function basically create
		#the connectivity diagram. It makes every bs into a Square obj
		#then looks for aus. for every one it finds, it adds it to the Square.adjacent property
		#The same is done for US except it looks for bs to add to Square.adjacent
		#this allows you to jump back and forth between connected squares which is useful for making matrix
		#the functions need to called in this specific order
		this.updateAdjacentBS(currGrid,bsArray,w,h)	
		ausArray = this.getBorderUnrevealedSquares(bsArray)
		rcm = this.makeReallyCoolMatrix(bsArray,h) #w is numCols (parameter of makeReallyCoolMatrix())
		#begin to solve.
		trivSolutions = this.solveTrivialSolutions(rcm,h)
		# print("triv = ",trivSolutions)
		yo = this.getSimilarEquations(rcm)
		for i in range(len(yo)):
			#print(yo[i][0][2].position)
			for j in range(len(yo[i][1])):
				#print("-----",yo[i][1][j][2].position)
				None
		subsetSolutions = this.solveSubsets(rcm,h)
		# print("sub = ",subsetSolutions)
		# simEqSolutions = solveSimilarEquations(rcm)
		this.addSolutions(solutions,trivSolutions)
		this.addSolutions(solutions,subsetSolutions)
		# this.addSolutions(solutions,simEqSolutions)
		if (len(solutions[0]) + len(solutions[1])) is 0:
			#PANIC! begin to guess, since you couldn't find anything
			guess = this.getBestProb(currGrid,ausArray,rcm,numMines,w,h)
			this.numGuesses += 1
			# print("GUESSING = ",guess)
			this.addSolutions(solutions,guess)
		return solutions



	#############################################################################
	#############################################################################
	#############################################################################

	#return array of bs. bs is array of Square obj.s
	def getBorderSquares(this,currGrid,w,h):
		bsArray = []
		for i in range(w):
			for j in range(h):
				tempNum = currGrid[i][j]
				if tempNum in range(1,9) :
					for posi in this.getSurroundingPositions(i,j,w,h):
						adjNum = currGrid[posi[0]][posi[1]]
						if adjNum ==  '#':
							#just found a border square
							#make it into Square obj, to keep track of adj
							newNum = this.calcEffectiveNum(tempNum,(i,j),currGrid,w,h)
							tempSq = Square(newNum,pos=(i,j))
							#hope that's right order
							bsArray.append(tempSq)
							break
		return bsArray
			

	#############################################################################
	#############################################################################
	#############################################################################
			
	def getBorderUnrevealedSquares(this,bsArray):
		unrevSqArray = []
		for sq in bsArray:
			for aus in sq.adjacent:
				#while we're at it, also update aus
				aus.addAdj(sq)
				#make sure there's no duplicates
				if not aus in unrevSqArray:
					unrevSqArray.append(aus)
		return unrevSqArray

	#############################################################################
	#############################################################################
	#############################################################################
			
	#updates adjacent arrays of 
	#both the bs and us. first loop through bs, cause that's what you have
	#while looping, keep track of us so you can loop through them afterward
	def updateAdjacentBS(this,currGrid,borderSquares,w,h):
		for bs in borderSquares:
			# let's see what happens...
			xPos = bs.position[0]
			yPos = bs.position[1]
			for posi in this.getSurroundingPositions(xPos,yPos,w,h):
				tempNum = currGrid[posi[0]][posi[1]]
				if tempNum is '#':
					tempSq = Square('#',vis=False,pos=posi)
					currGrid[posi[0]][posi[1]] = tempSq
					bs.addAdj(tempSq)
				elif type(tempNum) is Square:
					bs.addAdj(tempNum) 
	# #############################################################################
	# #############################################################################
	# #############################################################################
	#looks for flags (i.e. '!') around given position to caculate how
	# many more mines need to be found
	def calcEffectiveNum(this,oldNum,position,currGrid,w,h):
		newNum = oldNum
		for posi in this.getSurroundingPositions(position[0],position[1],w,h):
			tempNum = currGrid[posi[0]][posi[1]]
			if tempNum == '!':  #'!' represents a flag...
				newNum -= 1	
		return newNum
	#############################################################################
	#############################################################################
	#############################################################################
			
	# give it a x,y position and it returns all the valid positions directly adjacent
	def getSurroundingPositions(this,X,Y,w,h):
		posList = []
		for y in range(Y-1,Y+2):
			if y >= 0 and y < h:
				for x in range(X-1,X+2):
					if x >= 0 and x < w:
						posList.append((x,y))
		return posList
				
	#############################################################################
	#############################################################################
	#############################################################################
			
	def makeReallyCoolMatrix(this,borderSquares,numRows):
		#return 2d array
		#each inner array has three values
		#[0] = binary representing aus
		#[1] = number of mines
		#[2] = square object (mostly for finding position, but also useful for adjacent matrix
		matrix = []
		for sq in borderSquares:
			equation = this.getEquation(sq,numRows)
			#should there be any order to equations in matrix? dunno
			matrix.append(equation)
		return matrix
		
	#############################################################################
	#############################################################################
	#############################################################################	
	def getEquation(this,sq,numRows):
		#helper func to makeReallyCoolMatrix()
		#takes a Square object and returns equation for matrix which includes binary, solution and position
		#strategy: make binary num. indexes on this bin will be numbered from the right, like a decimal where 0 is the 1's position
		#loop through Square.adjacent (made up of Square objects)
		#for each sq, use its translate its 2d position to 1d (simple multiplication)
		#this will be its index in the binary num. somehow set that index to 1
		#once done, add solution (ie Square.number) and EDIT Square object (more convenient for finding aus)
		equation = []
		binary = 0b0
		for aus in sq.adjacent:
			tempPos = aus.position
			onedeeIndex = numRows*tempPos[1] + tempPos[0] #tempPos is zero-based. onedeeIndex is not
			#!!!!! 1D Index of (2,3) = (2+1)(3+1)=12, 1D Index of (3,2)=(3+1)(2+1)=12 Doesn't work...
			#Look at an example 3 x 5 grid and look at each positions index.
			#1  2  3  4  5
			#6  7  8  9  10
			#11 12 13 14 15
			#The 1D Index of (2,3) is (5)*2 + (3+1) = 14 where 5 is numColumns, 2 and 3 are row and column
			#onedeeIndex = (# of columns)*tempPos[0] + tempPos[1]+1
			tempBin = 1 << onedeeIndex #in layman's terms: put a 1 at the onedeeIndex position of the binary number 
			binary = binary | tempBin #i'm pretty sure this correctly changes the desired index to 1
		equation.append(binary)
		equation.append(sq.number)
		equation.append(sq)
		return equation
		
	#############################################################################
	#############################################################################
	#############################################################################
			
	def solveTrivialSolutions(this,reallyCoolMatrix,numRows):
		solutionArray = [[],[]]
		for eq in reallyCoolMatrix:
			tempSolution = this.solveTrivialSolution(eq,numRows)
			if len(tempSolution[0]) > 0:
				if not tempSolution[0][0] in solutionArray[0]: 
					this.addSolutions(solutionArray,tempSolution)
			elif len(tempSolution[1]) > 0:
				if not tempSolution[1][0] in solutionArray[1]:
					this.addSolutions(solutionArray,tempSolution)
		return solutionArray

	#############################################################################
	#############################################################################
	#############################################################################

	def solveTrivialSolution(this,eq,numRows,subset=False):
		solutionArray = [[],[]]
		numUnknowns = this.numOnes(eq[0])
		sqNum = eq[1]
		adjArray = []
		if subset: #meaning: we're calling func from solveSubsets. now need to use given bin to figure out which aus are not part of subset. Those are the ones we can solve for.
			for aus in eq[2].adjacent:
				tempPos = aus.position
				oneDeeIndex = numRows*tempPos[1] + tempPos[0]
				tempBin = 1 << oneDeeIndex
				if eq[0] & tempBin != 0:
					adjArray.append(aus)
		else:
			adjArray = eq[2].adjacent
		if numUnknowns == sqNum and sqNum != 0: 
			for aus in adjArray:
				solutionArray[1].append(aus.position) #add positions of all adjacent us to flag section of solution array (i.e. [1])
		elif sqNum == 0: # or rather, effectively zero, since we accounted for flags when first setting num in getBorderSquares 
			for aus in adjArray:
				solutionArray[0].append(aus.position) #add positions of all adjacent us to click section of solution array (i.e. [0])
		return solutionArray

	#############################################################################
	#############################################################################
	#############################################################################
			
	def getSubsets(this,reallyCoolMatrix):
		subsets = []
		duplicateEqArray = [] #don't allow for a subset/superset pair to be repeated
		for eq in reallyCoolMatrix:
			tempBin = eq[0]
			if tempBin in duplicateEqArray:
				continue
			tempSupersets = []
			#there's definitely a better way of searching than brute force...
			for otherEq in reallyCoolMatrix:
				if otherEq != eq: #don't count eq as superset of itself. that's just silly
					if otherEq[0] & tempBin == tempBin:
						#found a subset
						tempSupersets.append(otherEq)
						if otherEq[0] == tempBin:
							duplicateEqArray.append(tempBin)
			if len(tempSupersets) != 0:
				subsets.append((eq,tempSupersets))
		return subsets
		# subsetArray = [[subset1,[supersetA1,supersetB1]],[subset2,[supersetA2]]]
		# return double array, each inner array has indexes of subset pairs (could be more than 2?)
		# in order to find larger subsets, probably loop through all subset pairs
		# that you just found and see if there are triple pairs. if no triple pairs, stop
		# if there are search for quad pairs etc. probably some type of while loop...
					
	############################################################################
	############################################################################
	############################################################################
			
	def solveSubsets(this,reallyCoolMatrix,numRows):
		subsets = this.getSubsets(reallyCoolMatrix)
		solutionArray = [[],[]]
		for sub in subsets:
			subBool = sub[0][0]   #should be referencing the boolean in the equation that is a subset
			for sup in sub[1]:
				# print('curr sup = ',sup[2].position)
				supBool = sup[0]
				nonSetBool = supBool ^ subBool #xor is so cool =D
				effectiveSupNum = sup[1] - sub[0][1]
				effectiveEq = [nonSetBool,effectiveSupNum,sup[2]]
				tempSolutions = this.solveTrivialSolution(effectiveEq,numRows,True)
				# print('tempSol = ',tempSolutions)
				this.addSolutions(solutionArray,tempSolutions)
		return solutionArray

	#############################################################################
	#############################################################################
	#############################################################################
			
	def getSimilarEquations(this,reallyCoolMatrix):
		simEqs = []
		duplicateEqArray = [] #don't allow for a subset/superset pair to be repeated
		for eq in reallyCoolMatrix:
			tempBin = eq[0]
			if tempBin in duplicateEqArray:
				continue
			tempSupersets = []
			#there's definitely a better way of searching than brute force...
			for otherEq in reallyCoolMatrix:
				if otherEq != eq: #don't count eq as superset of itself. that's just silly
					if this.numOnes(otherEq[0] & tempBin) >= 2 and not otherEq[0] & tempBin == tempBin:
						#found a subset
						tempSupersets.append(otherEq)
						if otherEq[0] == tempBin:
							duplicateEqArray.append(tempBin)
			if len(tempSupersets) != 0:
				simEqs.append((eq,tempSupersets))
		return simEqs
		#gets eq.s with two or more spaces in common
		#return same as getSubsets()
					
	# #############################################################################
	# #############################################################################
	# #############################################################################
	# 			
	# 	# def solveSimilarEquations(simEqs):
	# 				
	#############################################################################
	#############################################################################
	#############################################################################
				
	#takes a aus and returns probability of mine being there
	def getProb(this,aus):
		#strategy: for any aus given, the probability is determined (hopefully this is right...)
		#by the probability of the abs who borders the least number of aus including this specific aus
		#this abs can be said to be the limiting factor for this aus, determining its probability
		aBS = aus.adjacent
		#find abs with least aus (i.e. limiting factor)
		limitingFactor = None
		for sq in aBS:
			if limitingFactor == None:
				limitingFactor = sq
			elif len(sq.adjacent) < len(limitingFactor.adjacent): # stupid, but pretty sure these need to be split up so doesn't check for .adjacent on None
				limitingFactor = sq
		prob = sq.number/len(sq.adjacent)
		return prob
				
	#############################################################################
	#############################################################################
	#############################################################################
			
	def getBestProb(this,currGrid,ausArray,rcm,numMines,w,h):
		lowestProb = 1
		# PROB_THRESHHOLD = 0.1 # what is highest prob that you're willing to guess in unknown. OHHH... 
		bestUSPos = None
		for aus in ausArray:
			tempProb = this.getProb(aus)
			if tempProb < lowestProb:
				lowestProb = tempProb
				bestUSPos = aus.position
		numOtherMines = numMines - this.minMinesInAus(rcm)
		otherUS = this.getOtherUS(currGrid,ausArray,w,h)
		otherProb = 1
		if len(otherUS) > 0: # avoid division by zero
			otherProb = numOtherMines/len(otherUS)
		if otherProb <= lowestProb and len(otherUS) > 0: 
			#choose random us, excluding aus
			rand = random.randint(0,len(otherUS)-1)
			bestUSPos = otherUS[rand]
		if bestUSPos is None:
			print('oh no...')
			print(len(otherUS),len(ausArray))
			return [[],[]]
		else:
			return [[bestUSPos],[]] # solution array where only entry is click position.	

		#now compare to prob of finding mine anywhere else...
			
		#loop through ausArray and use getProb(aus) to get prob for each
		#save lowest prob (i.e. leaset prob to hit a mine) and it's corresponding aus
		#now you need to compare it with prob that there's a mine anywhere else
		#this could get complicated: need a way of finding minimum amount of mines in aus...
		#returns a solution array with one value
		#either a flag or click
				
	#############################################################################
	#############################################################################
	#############################################################################
	def minMinesInAus(this,rcm):
		#strategy: sum up all bs number's that have unique adjacent arrays. I think this is a good estimation (hopefully)
		minMines = 0
		uniqueBins = [] #check to make sure no ovelapping bs nums were counted
		for eq in rcm:
			isUnique = True
			tempBin = eq[0]
			if len(uniqueBins) != 0: #if it's 0, add it no matter what
				for ub in uniqueBins:
					#needed to play around a bit with this (fun!). tries to limit number of bs nums counted
					if this.numOnes(tempBin & ub) > 1 and this.numOnes(tempBin) > 1 and this.numOnes(ub) > 1:
						isUnique = False
						break
					elif tempBin & ub != 0:
						isUnique = False
						break
			if isUnique:
				uniqueBins.append(tempBin)
				minMines += eq[1]
		return minMines
	#############################################################################
	#############################################################################
	#############################################################################
	def getOtherUS(this,currGrid,aus,w,h):
		usPositions = []
		for y in range(h):
			for x in range(w):
				tempNum = currGrid[x][y]
				if tempNum is '#':
					# make sure this isn't an aus...
					unique = True
					for us in aus:
						if us.position is (x,y):
							unique = False
							break
					if unique:
						usPositions.append((x,y))
		return usPositions

	#############################################################################
	#############################################################################
	#############################################################################
			       
	#puts new solutions into solutions array
	#so that click solutions correspond and 
	#flag solutions correspond
	def addSolutions(this,solArray,newSols):
		for i in range(2):
			for j in range(len(newSols[i])):
				if not newSols[i][j] in solArray[i]:
					solArray[i].append(newSols[i][j])

	#############################################################################
	#############################################################################
	#############################################################################

	#helper func for getProb() among others
	#surprisingly helpful, attaboy helper func!
	def numOnes(this,bin):
		count = 0
		while bin > 0:
			bin &= bin - 1
			count+= 1
		return count

