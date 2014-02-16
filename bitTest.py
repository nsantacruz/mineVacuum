def numOnes(bin):
	count = 0
	while bin > 0:
		bin &= bin - 1
		count+= 1
	return count
	
print(numOnes(0b111001)) # 4 ones
