global quadStartingLabel
quadStartingLabel = 100

# KLASH QUAD
class Quad:
    def __init__(self, label, operation, operand1, operand2, operand3):
        self.label = label
        self.operation = operation # e.g ('+', a, 1 , a) equals to a := a + 1
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
    
    def __str__(self):
        print(f'{self.label}: ({self.operation}, {self.operand1}, {self.operand2}, {self.operand3})')
class QuadList:
    def __init__(self, programList, quadCounter):
        self.programList = programList
        self.quadCounter = quadCounter

    def __str__(self):
        return f'QuadList(Quads: {self.programList}\nNumber of quads: {self.quadCounter}\n)'
    
    def backpatch(self, labelList, quadLabel):
        for l in labelList:
            for q in self.programList:
                if l == q.label:
                    q.op3 = quadLabel

    def genQuad(self, operator, operand1, operand2, operand3):
        global quadStartingLabel
        newQuad = Quad(quadStartingLabel, operator, operand1, operand2, operand3)
        self.programList.append(newQuad)
        self.quadCounter += 1
        quadStartingLabel += 1

    def nextQuad(self):
        return quadStartingLabel

class QuadPointer:
    def __init__(self, label):
        self.label = label

    def __str__(self):
        return f'{self.label}'
    
    def mergeList(self, l1, l2):
        return l1 + l2

class QuadPointerList:
    def __init__(self, labelList):
        self.labelList = labelList

    def __str__(self):
        return f'QuadPointerList(List of the labels: {self.labelList})'