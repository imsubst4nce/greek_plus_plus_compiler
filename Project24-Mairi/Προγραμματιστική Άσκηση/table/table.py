class Entity:
    def __init__(self, name):
        self.name = name

class Variable(Entity):
    def __init__(self, name, datatype, offset):
        super().__init__(name)
        self.datatype = datatype
        self.offset = offset

class Parameter(Entity):
    def __init__(self, name, datatype, mode, offset):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode
        self.offset = offset
        
class FormalParameter:
    def __init__(self, datatype, mode):
        self.datatype = datatype
        self.mode = mode

class Function(Entity):
    def __init__(self, name, datatype, startingQuad, framelength, formalParameters):
        super().__init__(name)
        self.datatype = datatype
        self.startingQuad = startingQuad
        self.framelength = framelength
        self.formalParameters = formalParameters

## h dikh mas glwssa den exei procedures, opote thn afairesa san klash, 
## omws to erwthma einai ti fields exei to function?? 
## kai einai subclass tou entity?? maybe???

##class TemporaryVariable(Entity):
##    def __init__(self, name, datatype, offset):
##        super().__init__(name)
##        self.datatype = datatype
##        self.offset = offset

class TemporaryVariable(Variable):  # TemporaryVariable is a subclass of Variable
    def __init__(self, name, datatype, offset):
        super().__init__(name, datatype, offset)

class SymbolicConstant(Entity): ##evala to entity giati einai subclass
    def __init__(self, name, datatype, value):
        super().__init__(name) ##giati einai to constructor tou entity
        self.datatype = datatype
        self.value = value

class Scope:
    def __init__(self, name, nestingLevel, entitiesList, nextScope):
        self.name=name
        self.nestingLevel=nestingLevel
        self.entitiesList=entitiesList
        self.nextScope=nextScope

    

