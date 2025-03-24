# KLASH QUAD
class Quad:
    def __init__(self):
        print("Initializing Quad class...")
        self.lastTemp = "T_0" # last temp variable inits to T_0
        self.label = None # label will be given by calling backpatch method

    # Creates a new quad
    def genQuad(self, operator, operand1, operand2, operand3):
        self.operator = operator
        self.operand1 = operand1
        self.operand2 = operand2
        self.operand3 = operand3
    
    # Returns next quad's label
    def nextQuad(self):
        return
    
    # Next temp variable name is created and returned
    def newTemp(self):
        newTemp = "T_" + str(int(self.lastTemp[2])+1)
        self.lastTemp = newTemp
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

    # Iterates over the quads from the list
    # and if it finds the quad under the given label,
    # 
    def backpatch(self, list, label):
    
if __name__ == "__main__":
    quad = Quad()