#added equation property so that we can easily match up equation to square
#used in getProb() func in pseudocode
#make sure to set Square.equation property when first making matrix in makeReallyCoolMatrix()
class Square():
    def __init__(this,num,*adj,vis=False,pos=(0,0)):
        this.number = num
        this.visible = vis
        this.flagged = False
        this.position = pos
        this.adjacent = []
        this.equation = []
        if adj:
            this.adjacent = adj
            for x in this.adjacent:
                #print(x.number)
                None

    def addAdj(this,*adj):
        for x in adj:
            this.adjacent.append(x)
            #print(x.number)
    def setPosition(this,x,y):
        this.position = [x,y]
	
    def setEquation(this,equation):
            this.equation = equation

sq1 = Square(1)
sq2 = Square(2)
usq1 = Square(-1,sq1,sq2)
sq1.addAdj(usq1,sq2)
