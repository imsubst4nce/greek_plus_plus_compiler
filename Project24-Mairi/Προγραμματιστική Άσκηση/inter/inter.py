##ZACHRA ELISAVET ALLA GKAMPOU, 5052
##MARIA KATOLI, 5083

global quadLabel
quadLabel=100 #as poume to prwto label

class Quad:
    def __init__(self, label, op, op1, op2, op3):
        self.label=label
        self.op=op
        self.op1=op1
        self.op2=op2
        self.op3=op3

    def __str__(self):
        return f'Quad(Label: {self.label}\nQuad: "{self.op},{self.op1},{self.op2},{self.op3}\n")'

class QuadList:
     def __init__(self, programList, quad_counter):
        self.programList=programList
        self.quad_counter=quad_counter

    def __str__(self):
        return f'QuadList(Quads: {self.programList}\nNumber of quads: {self.quad_counter}\n)'

    def backPatch(self, labelList, quadLabel):
        for l in labelList: #gia kathe label sto labelList
            for q in self.programList: #gia kathe quad sto quadList mas 
                if l.label==q.label: #an to label tou quad einai iso me to label pou grafei h labelList
                    q.op3=l.label #op3==label

    def genQuad(self, operator, operand1, operand2, operand3):
        newQuad=Quad(quadLabel,operator,operand1,operand2,operand3)
        self.programList.append(newQuad)
        self.quad_counter+=1
        quadLabel+=1

    def makeList(self, label):
        return [label]

    def emptyList(self):
        return []

    def nextQuad(self):
        return quadLabel

class QuadPointer:
    def __init__(self, label):
        self.label=label

    def __str__(self):
        return f'QuadPointer(Label: {self.label}\n)'

class QuadPointerList:
    def __init__(self, labelList):
        self.labelList=labelList

    def __str__(self):
        return f'QuadPointerList(List of the labels: {self.labelList}\n)'

    def mergeList(self, l1, l2):
        l=list(set(l1+l2))
        return l
    
    
    
