# KLASH QUAD
class Quad:
    def __init__(self):
        # probably to be moved in genQuad
        # self.operation = operation # e.g ('+', a, 1 , a)
        # self.operand1 = operand1
        # self.operand2 = operand2
        # self.operand3 = operand3
        # self.label = None # label will be given by calling backpatch method
        self.quadlist = [] # init quads list
        self.tempvar = "T_0" # last temp variable inits to T_0
    
    def __str__(self):
        print(f'({self.operation},{self.operand1},{self.operand2},{self.operand3})')

    # Creates a new quad
    def genQuad(self, operation, operand1, operand2, operand3):
        self.operation = operation # e.g ('+', a, 1 , a)
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
        self.label = None # init quad label is None and will be replaced during backpatching
        self.quadlist.append([operation, operand1, operand2, operand3, self.label])
    
    # Returns next quad's label
    # Needs to be fixed!!!
    def nextQuad(self):
        if not self.quadlist:
            return 0
        return # if there are quads what does it return?
    
    # Next temp variable name is created and returned
    def newTemp(self):
        newTemp = "T_" + str(int(self.tempvar[2])+1)
        self.tempvar = newTemp
        return newTemp

    # Returns an empty list which later on
    # will hold the labels of all the quads
    def emptyList(self):
        return []
    
    # Returns a list that contains only
    # the label of the quad
    def makeList(self, label):
        return [label]
    
    # Create and return a new list that
    # holds the items of both lists 1 & 2
    def mergeLists(self, list1, list2):
        return list1 + list2

    # Replaces empty quad labels with the 
    # list: contains the indices where all the 'None' labeled quads are
    # label: the label that will replace 'None'
    def backpatch(self, list, label):
        for index in list:
            self.quadlist[index].label = label
        
        list.clear() # once finished deallocate memory

    
if __name__ == "__main__":
    newquad = Quad()