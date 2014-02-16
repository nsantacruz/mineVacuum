#Cool. Please ask if anything's unclear, since I wrote this while half-asleep
#UPDATED: Probability is almost done. 
#Now able to generate binary equations for matrix (see getEquation())
#class pseudocode():
#return array of double array
#[0] array of positions to click
#[1] array of positions to flag
def solveForGrid(currGrid):
	#dimensions of grid
	w,h = (len(currGrid),len(currGrid[0]))
	
	solutions = [[] for i in range(2)] #cool syntax
		
	#update Square.adjacent property
	bsArray = getBorderSquares(currGrid,w,h)
	print(bsArray)
	#This and the accompanying US function basically create
	#the connectivity diagram. It makes every bs into a Square obj
	#then looks for aus. for every one it finds, it adds it to the Square.adjacent property
	#The same is done for US except it looks for bs to add to Square.adjacent
	#this allows you to jump back and forth between connected squares which is useful for making matrix
	#the functions need to called in this specific order
	# this.updateAdjacentBS(currGrid,bsArray,w,h)	
	# ausArray = this.getBorderUnrevealedSquares(bsArray)

	# this.updateAdjacentUS(ausArray)
	# rcm = this.makeReallyCoolMatrix(bsArray,w) #w is numCols (parameter of makeReallyCoolMatrix())


	
	# #begin to solve.
	# trivSolutions = this.solveTrivialSolutions(rcm)
	# # subsetSolutions = this.solveSubsets(rcm)
	# simEqSolutions = this.solveSimilarEquations(rcm)
	# this.addSolutions(solutions,trivSolutions)
	# # this.addSolutions(solutions,subsetSolutions)
	# this.addSolutions(solutions,simEqSolutions)
	# if (len(solutions[0]) and len(solutions[1])) == 0:
	# 	#PANIC! begin to guess, since you couldn't find anything
	# 	# guess = this.getBestProb(ausArray)
	# 	# this.addSolutions(solutions,guess)
	# 	None
	# return solutions



#############################################################################
#############################################################################
#############################################################################

#return array of bs. bs is array of Square obj.s
def getBorderSquares(this,currGrid,w,h):
	bsArray = []
	for i in range(h):
		for j in range(w):
			tempNum = currGrid[i][j]
			if tempNum in range(1,9) :
				for posi in getSurroundingPositions(j,i):
					adjNum = currGrid[posi[1]][posi[0]]
					if adjNum ==  '#':
						#just found a border square
						#make it into Square obj, to keep track of adj
						newNum = this.calcEffectiveNum(tempNum,(j,i),currGrid)
						tempSq = Square(newNum,pos=(j,i))
						#hope that's right order
						bsArray.append(tempSq)
	return bsArray
		

# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	def getBorderUnrevealedSquares(this,bsArray):
# 		unrevSqArray = []
# 		for sq in bsArray:
# 			for aus in sq.adjacent
# 				#make sure there's no duplicates
# 				if not aus in unrevSqArray:
# 					unrevSqArray.append(aus)
# 		return unrevSqArray
# 	
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	#updates adjacent arrays of 
# 	#both the bs and us. first loop through bs, cause that's what you have
# 	#while looping, keep track of us so you can loop through them afterward
# 	def updateAdjacentBS(this,currGrid,borderSquares,w,h):
# 		for bs in revealedSqs:
# 			if bs.number == 0:
# 				continue
# 			else:
# 				xPos = bs.position[0]
# 				yPos = bs.position[1]
# 				for posi in this.getSurroundingPositions(xPos,yPos):
# 					tempNum = currGrid[posi[1]][posi[0]]
# 					if tempNum == '#':
# 						tempSq = new Square('#',vis=False,pos=posi)
# 						bs.addAdj(tempSq)
# 			
# #############################################################################
# #############################################################################
# #############################################################################
# 	#looks for flags (i.e. '!') around given position to caculate how
# 	# many more mines need to be found
# 	def calcEffectiveNum(this,oldNum,position,currGrid):
# 		newNum = oldNum
# 		for posi in this.getSurroundingPositions(position[0],position[1])
# 			tempNum = currGrid[posi[1][posi[0]]
# 			if tempNum == '!'  #'!' represents a flag...
# 				newNum -= 1	
# 		return newNum
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	def updateAdjacentUS(this,unrevealedSquares):	
# 		for us in unrevealedSquares:
# 			xPos = us.position[0]
# 			yPos = us.position[1]
# 			for posi in this.getSurroundingPositions(xPos,yPos):
# 				tempNum = currGrid[posi[1]][posi[0]]
# 				if int(tempNum) in range(1,9):
# 					tempSq = new Square(tempNum,pos=posi)
# 					us.addAdj(tempSq)
# 			
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	# give it a x,y position and it returns all the valid positions directly adjacent
# 	def getSurroundingPositions(this,X,Y,w,h):
# 		posList = []
# 		for y in range(Y-1,Y+2):
# 			if y >= 0 and y < h:
# 				for x in range(X-1,X+2):
# 					if x >= 0 and x < w:
# 						posList.append((x,y))
# 		return posList
# 				
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	def makeReallyCoolMatrix(this,borderSquares,numCols):
# 		#return 2d array
# 		#each inner array has three values
# 		#[0] = binary representing aus
# 		#[1] = number of mines
# 		#[2] = I lied, 3d array. tuple of position
# 		matrix = []
# 		for sq in borderSquares:
# 			equation = this.getEquation(sq,numCols)
# 			#should there be any order to equations in matrix? dunno
# 			matrix.append(equation)
# 		return matrix
# 		
# #############################################################################
# #############################################################################
# #############################################################################	
# 	def getEquation(this,sq,numCols):
# 		#helper func to makeReallyCoolMatrix()
# 		#takes a Square object and returns equation for matrix which includes binary, solution and position
# 		#strategy: make binary num. indexes on this bin will be numbered from the right, like a decimal where 0 is the 1's position
# 		#loop through Square.adjacent (made up of Square objects)
# 		#for each sq, use its translate its 2d position to 1d (simple multiplication)
# 		#this will be its index in the binary num. somehow set that index to 1
# 		#once done, add solution (ie Square.number) and EDIT Square object (more convenient for finding aus)
# 		equation = []
# 		binary = 0b0
# 		for aus in sq.adjacent:
# 			tempPos = aus.position
# 			onedeeIndex = numCols*tempPos[0] + tempPos[1] + 1#tempPos is zero-based. onedeeIndex is not
# 			#!!!!! 1D Index of (2,3) = (2+1)(3+1)=12, 1D Index of (3,2)=(3+1)(2+1)=12 Doesn't work...
# 			#Look at an example 3 x 5 grid and look at each positions index.
# 			#1  2  3  4  5
# 			#6  7  8  9  10
# 			#11 12 13 14 15
# 			#The 1D Index of (2,3) is (5)*2 + (3+1) = 14 where 5 is numColumns, 2 and 3 are row and column
# 			#onedeeIndex = (# of columns)*tempPos[0] + tempPos[1]+1
# 			tempBin = onedeeIndex << 1
# 			binary = binary | tempBin #i'm pretty sure this correctly changes the desired index to 1
# 		equation.append(binary)
# 		equation.append(sq.number)
# 		equation.append(sq)
# 		return equation
# 		
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	def solveTrivialSolutions(this,reallyCoolMatrix):
# 		solutionArray = [[],[]]
# 		for eq in reallyCoolMatrix:
# 			numUnknowns = this.numOnes(eq[0])
# 			sqNum = eq[1]
# 			if numUnknowns == sqNum:
# 				adjArray = eq[2].adjacent
# 				for aus in adjArray:
# 					solutionArray[1].append(aus.position) #add positions of all adjacent us to flag section of solution array (i.e. [1])
# 			elif sqNum == 0: # or rather, effectively zero, since we accounted for flags when first setting num in getBorderSquares 
# 				adjArray = eq[2].adjacent
# 				for aus in adjArray:
# 					solutionArray[0].append(aus.position) #add positions of all adjacent us to click section of solution array (i.e. [0])
# 		return solutionArray
# 
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# #	def getSubsets(this,reallyCoolMatrix):
# 		# subsets = []
# 		# for eq in reallyCoolMatrix:
# 		# 	tempBin = eq[0]
# 		# 	tempSupersets = []
# 		# 	#there's definitely a better way of searching than brute force...
# 		# 	for otherEq in reallyCoolMatrix:
# 		# 		if otherEq[0] & tempBin == tempBin:
# 		# 			#found a subset
# 		# 			tempSupersets.append(otherEq)
# 		# 	if len(tempSupersets) != 0:
# 		# 		subsets.append((eq,tempSupersets))
# 		# return subsets
# 		#subsetArray = [[subset1,[supersetA1,supersetB1]],[subset2,[supersetA2]]]
# 		#return double array, each inner array has indexes of subset pairs (could be more than 2?)
# 		# in order to find larger subsets, probably loop through all subset pairs
# 		#that you just found and see if there are triple pairs. if no triple pairs, stop
# 		#if there are search for quad pairs etc. probably some type of while loop...
# 					
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	# def solveSubsets(this,reallyCoolMatrix):
# 	# 	subsets = this.getSubsets(reallyCoolMatrix)
# 	# 	for sub in subsets:
# 	# 		tempBool = sub[0][0]   #should be referencing the boolean in the equation that is a subset
# 	# 		for superSet in sub[1]:
# 
# 		#use '|' operations on subsets to solve.
# 		#in resulting equation, look for trivial solution or if it equals zero
# 				
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	def getSimilarEquations(this,reallyCoolMatrix):
# 		simEqs = []
# 		for eq in reallyCoolMatrix:
# 			tempBin = eq[0]
# 			tempSupersets = []
# 			#there's definitely a better way of searching than brute force...
# 			for otherEq in reallyCoolMatrix:
# 				if numOnes(otherEq[0] & tempBin) >= 2:
# 					#found a subset
# 					tempSupersets.append(otherEq)
# 			if len(tempSupersets) != 0:
# 				subsets.append((eq,tempSupersets))
# 		return subsets
# 		#gets eq.s with two or more spaces in common
# 		#return same as getSubsets()
# 					
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	# def solveSimilarEquations(this,simEqs):
# 				
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	#takes a aus and returns probability of mine being there
# 	def getProb(this,aus,rcm):
# 		#strategy: for any aus given, the probability is determined (hopefully this is right...)
# 		#by the probability of the abs who borders the least number of aus including this specific aus
# 		#this abs can be said to be the limiting factor for this aus, determining its probability
# 		abs = aus.adjacent
# 		#find abs with least aus (i.e. limiting factor)
# 		limitingFactor = None
# 		for sq in abs:
# 			if len(sq.adjacent) < len(limitingFactor.adjacent) or limitingFactor == None:
# 				limitingFactor = sq
# 		prob = sq.number/len(sq.adjacent)
# 		return prob
# 			
# #############################################################################
# #############################################################################
# #############################################################################
# 			
# 	def getBestProb(this,ausArray,rcm):
# 		lowestProb = 1
# 		bestAUS = None
# 		for aus in ausArray:
# 			tempProb = this.getProb(aus)
# 			if tempProb < lowestProb:
# 				lowestProb = tempProb
# 				bestAUS = aus
# 			
# 		#loop through ausArray and use getProb(aus) to get prob for each
# 		#save lowest prob (i.e. leaset prob to hit a mine) and it's corresponding aus
# 		#now you need to compare it with prob that there's a mine anywhere else
# 		#this could get complicated: need a way of finding minimum amount of mines in aus...
# 		#returns a solution array with one value
# 		#either a flag or click
#  				
# #############################################################################
# #############################################################################
# #############################################################################
# 		               
# 	#puts new solutions into solutions array
# 	#so that click solutions correspond and 
# 	#flag solutions correspond
# 	def addSolutions(this,solArray,newSols):
# 		for i in range(2):
# 			for j in range(len(newSols)):
# 				solArray[i].append(newSols[j])
# 
# #############################################################################
# #############################################################################
# #############################################################################
# 	
# 	#helper func for getProb()
# 	def numOnes(bin):
# 		count = 0
# 		while bin > 0:
# 			bin &= bin - 1
# 			count+= 1
# 		return count
# 	
print("yo")	
