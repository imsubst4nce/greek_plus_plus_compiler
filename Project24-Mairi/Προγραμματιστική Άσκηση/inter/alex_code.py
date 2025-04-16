import sys

#TOKENS
greeklow = 'αβγδεζηθικλμνξοπρστφχψυως'
greeklowtone = 'άέήίόύώ'
greekcap = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΦΧΨΥΩ'
englow = 'abcdefghijklmnopqrstuvwxyz'
engcap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
numops = {'+','-','*','/'}
aops = {'<','>','=','<=','>=','<>'}
asym = {':='}
separators = {';',','}
groupsym = {'(',')','[',']'}
comments = {'{','}'}
whitespaces = {' ','\n','\t','\r'}
reference = {'%'}
keywords = {"πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος",
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "εώς", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία",
    "είσοδος", "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας",
    "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", "και", "όχι",
    "εκτέλεσε"} 



############
## Τοκενς ##
############

class Token:
        def __init__(self, recognized_string, family, line_number):
               self.recognized_string = recognized_string
               self.family = family
               self.line_number = line_number

        def __str__(self):
                return f'string: {self.recognized_string} family: "{self.family}", line: {self.line_number}'

#######################
## Λεκτικος Αναλυτης ##
#######################

class Lex:
        def __init__(self, file_name):
                self.file_name = file_name
                self.position = 0
                self.current_line = 1
                self.tokens = []

                print(f"Trying to open file: {self.file_name}") 
                try:
                        with open(self.file_name, 'r', encoding='utf-8') as f: # ανοιγμα αρχειου
                                self.source = f.read()
                                print("File content loaded successfully.")
                except FileNotFoundError:
                        print(f'Error: File "{self.file_name}" not found.')
                        sys.exit(1)

                self.current_char = self.source[self.position] if self.source else None
                # print(self.source) κανε print στην οθονη το αρχειο    

        # πηγαινε στην επομενη θεση στο αρχειο
        def advance(self):
                self.position += 1
                if self.position < len(self.source):
                        self.current_char = self.source[self.position]
                else:
                        self.current_char = None

        # πηγαινε στην επομενη γραμμη στο αρχειο
        def advance_line(self):
                self.current_line += 1

        # προσπερασε τα κενα (και ειδικους χαρακτηρες που δεν χρειαζονται)
        def skip_whitespaces(self):
                while self.current_char and self.current_char in whitespaces:
                        if self.current_char == '\n':
                                self.advance_line()
                        self.advance()
        
        # προσπερασε τα σχολια
        def skip_comment(self):
                if self.current_char == '{':
                        while self.current_char and self.current_char != '}':
                                if self.current_char in whitespaces:
                                        if self.current_char == '\n':
                                                self.advance_line() 
                                self.advance()
                        if self.current_char == '}':
                                self.advance()
                                self.skip_whitespaces()
                        else:
                                raise Exception(f'Unclosed comment at line {self.current_line}')
        
        # παρε και επεστρεψε αναγνωριστικα και δεσμευμενες λεξεις
        def get_word(self):
                word = ''
                if self.current_char and (self.current_char in englow or self.current_char in engcap or self.current_char in greeklow or self.current_char in greekcap or self.current_char in greeklowtone):
                        word += self.current_char
                        self.advance()
                        while self.current_char and len(word) <= 30 and (self.current_char in englow or self.current_char in engcap or self.current_char in greeklow or self.current_char in greekcap or self.current_char in greeklowtone or self.current_char in digits or self.current_char == '_'):
                                word += self.current_char
                                self.advance()
                
                        if word in keywords:
                                return Token(word, 'KEYWORD', self.current_line)
                        else:
                                return Token(word, 'IDENTIFIER', self.current_line)

        # παρε και επεστρεψε ακεραιες σταθερες και αριθμους
        def get_number(self):
                number = ''
                if self.current_char and self.current_char in digits:
                        while self.current_char and len(number) <= 30 and self.current_char in digits:
                                number += self.current_char
                                self.advance()
                        return Token(number, 'NUMBER', self.current_line)
        
        # παρε και επεστρεψε συμβολα αριθμητικων πραξεων
        def get_numop(self):
                nop = ''
                if self.current_char and self.current_char in numops:
                        nop += self.current_char
                        self.advance()
                        return Token(nop, 'NUMERICAL OPERATOR', self.current_line)
        
        # παρε και επεστρεψε τελεστες συσχετισης
        def get_aop(self):
                aop =''
                acheck = ''
                if self.current_char and self.current_char in {'<','>','='}:
                        aop += self.current_char
                        self.advance()
                        acheck = self.current_char
                        if self.current_char and ((aop in {'<','>'} and acheck == '=') or (aop == '<' and acheck == '>')):
                                acheck = aop + acheck
                                self.advance()
                                return Token(acheck, 'ASSOCIATIVE OPERATOR', self.current_line)
                        else:
                                return Token(aop, 'ASSOCIATIVE OPERATOR', self.current_line)

        # παρε και επεστρεψε συμβολα αναθεσης      
        def get_asym(self):
                assym = ''
                if self.current_char and self.current_char == ':':
                        assym += self.current_char
                        self.advance()
                        if self.current_char and self.current_char == '=':
                                assym += self.current_char
                                self.advance()
                                return Token(assym, 'ASSIGNMENT OPERATOR', self.current_line)
                        else:
                                raise Exception('Wrong assignment')
        
        # παρε και επεστρεψε διαχωριστες
        def get_separators(self):
                sep = ''
                if self.current_char and self.current_char in separators:
                        sep += self.current_char
                        self.advance()
                        return Token(sep, 'SEPARATOR', self.current_line)
        
        # παρε και επεστρεψε συμβολα ομαδοποιησης
        def get_groupsym(self):
                gsym = ''
                if self.current_char and self.current_char in groupsym:
                        gsym += self.current_char
                        self.advance()
                        return Token(gsym, 'GROUP SYMBOL', self.current_line)

        # παρε και επεστρεψε συμβολα περασματος παραμετρων με αναφορα    
        def get_reference(self):
                ref = ''
                if self.current_char and self.current_char in reference:
                        ref += self.current_char
                        self.advance()
                        return Token(ref, 'REFERENCE', self.current_line)
        
        # παρε και επεστρεψε token
        def get_token(self):
                while self.current_char:

                        # προσπερναμε κενα (και χαρακτηρες που δεν χρειαζονται) και σχολια
                        self.skip_whitespaces()
                        self.skip_comment()
                        
                        # αν ο χαρακτηρας ειναι none τοτε εχουμε φτασει στο τελος του αρχειου
                        if self.current_char is None:
                                print(f'End of file reached at line {self.current_line}')
                                return None

                        # ελεγχουμε τι χαρακτηρας ειναι και τον επιστρεφουμε
                        if self.current_char and (self.current_char in englow or self.current_char in engcap or self.current_char in greeklow or self.current_char in greekcap or self.current_char in greeklowtone):
                                return self.get_word()
                        elif self.current_char and self.current_char in digits:
                                return self.get_number()
                        elif self.current_char and self.current_char in numops:
                                return self.get_numop()
                        elif self.current_char and self.current_char in {'<','>','='}:
                                return self.get_aop()
                        elif self.current_char and self.current_char == ':':
                                return self.get_asym()
                        elif self.current_char and self.current_char in separators:
                                return self.get_separators()
                        elif self.current_char and self.current_char in groupsym:
                                return self.get_groupsym()
                        elif self.current_char and self.current_char in reference:
                                return self.get_reference()
                        else:
                                raise Exception(f"Invalid character: '{self.current_char}' at line: {self.current_line}")
        
        # φτιαχνουμε λιστα με τα tokens που βρηκαμε
        def tokenize(self):
                print('\nStarting lexical analysis...')
                while self.current_char:
                        token = self.get_token()
                        if token:
                                self.tokens.append(token)
                return self.tokens

##########################
## Συντακτικος Αναλυτης ##
##########################

global tmpVarCount
tmpVarCount = 0
global tmpVarList
tmpVarList = []

class Syntax:
        def __init__(self, tokens, generated_program):
                self.tokens = tokens
                self.generated_program = generated_program
                self.position = 0
                self.current_token = self.tokens[self.position]
        
        def newTemp(self):
                global tmpVarCount,tmpVarList
                s ="T_" + str(tmpVarCount)
                tmpVarCount = tmpVarCount+1
                tmpVarList.append(s)
                return s

        # παρε το επομενο token απο τον πινακα
        def advance(self):
                self.position += 1
                if self.position < len(self.tokens):
                        self.current_token = self.tokens[self.position]
                else:
                        self.current_token = None
        # βοηθητικη συναρτηση που κοιταει αν το string του token ειναι ιδιο με αυτο που περιμενουμε
        def match_string(self, expected_string):
                if self.current_token and self.current_token.recognized_string == expected_string:
                        return True
                raise Exception(f"Syntax Error: Expected {expected_string} but got {self.current_token.recognized_string if self.current_token else 'EOF'} at line {self.current_token.line_number if self.current_token else 'unknown'}")
        
        # βοηθητικη συναρτηση που κοιταει αν το family του token ειναι ιδιο με αυτο που περιμενουμε
        def match_family(self, expected_family):
                if self.current_token and self.current_token.family == expected_family:
                        return True
                raise Exception(f"Syntax Error: Expected {expected_family} but got {self.current_token.family if self.current_token else 'EOF'} at line {self.current_token.line_number if self.current_token else 'unknown'}")
        
        # ο συντακτικος αναλυτης 
        def syntax_analyzer(self):
                #global token
                #token = self.current_token
                self.program()

        # συναρτηση error η οποια δεν χρειαστηκε αλλα μπορει να υλοποιηθει κανονικα για να ειναι πιο optimized τα errors
        def error(msg):
                print(msg)

        ######################################################
        # ολες οι συναρτησεις για την γραμματικη της greek++ #
        ######################################################
                ######################################
                        ######################
                                ######
        
        def program(self):
                self.match_string('πρόγραμμα')
                self.advance()
                self.match_family('IDENTIFIER')
                self.advance()
                self.programblock()
        
        def programblock(self):
                self.declarations()
                self.subprograms()
                self.match_string('αρχή_προγράμματος')
                self.advance()
                self.sequence()
                self.match_string('τέλος_προγράμματος')

        def declarations(self):
                while self.current_token and self.current_token.recognized_string == 'δήλωση':
                        self.advance()
                        self.varlist()
        
        def varlist(self):
                self.match_family('IDENTIFIER')
                self.advance()
                while self.current_token and self.current_token.recognized_string == ',':
                        self.advance()
                        self.match_family('IDENTIFIER')
                        self.advance()
        
        def subprograms(self):
                while self.current_token and self.current_token.recognized_string in ['συνάρτηση', 'διαδικασία']:
                        if self.current_token.recognized_string == 'συνάρτηση':
                                self.func()
                                self.advance()
                        else:
                                self.proc()
                                self.advance()
                                

        def func(self):
                self.match_string('συνάρτηση')
                self.advance()
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string('(')
                self.advance()
                self.formalparlist()
                self.match_string(')')
                self.advance()
                self.funcblock()
                
        
        def proc(self):
                self.match_string('διαδικασία')
                self.advance()
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string('(')
                self.advance()
                self.formalparlist()
                self.match_string(')')
                self.advance()
                self.procblock()
        
        def formalparlist(self):
                if self.current_token and self.current_token.family == "IDENTIFIER":
                        self.varlist()
        
        def funcblock(self):
                self.match_string('διαπροσωπεία')
                self.advance()
                self.funcinput()
                self.funcoutput()
                self.declarations()
                self.subprograms()
                self.match_string('αρχή_συνάρτησης')
                self.advance()
                self.sequence()
                self.match_string('τέλος_συνάρτησης')

        def procblock(self):
                self.match_string('διαπροσωπεία')
                self.advance()
                self.funcinput()
                self.funcoutput()
                self.declarations()
                self.subprograms()
                self.match_string('αρχή_διαδικασίας')
                self.advance()
                self.sequence()
                self.match_string('τέλος_διαδικασίας')
                
        def funcinput(self):
                while self.current_token and self.current_token.recognized_string == 'είσοδος':
                        self.advance()
                        self.varlist()

        def funcoutput(self):
                while self.current_token and self.current_token.recognized_string == 'έξοδος':
                        self.advance()
                        self.varlist()

        def sequence(self):
                self.statement()
                while self.current_token and self.current_token.recognized_string == ";":
                        self.advance()
                        self.statement()
        
        def statement(self):
                token = self.current_token
                if token:
                        if token.family == 'IDENTIFIER':
                                self.assignment_stat()
                        elif token.recognized_string == 'εάν':
                                self.if_stat()
                        elif token.recognized_string == 'όσο':
                                self.while_stat()
                        elif token.recognized_string == 'επανάλαβε':
                                self.do_stat()
                        elif token.recognized_string == 'για':
                                self.for_stat()
                        elif token.recognized_string == 'διάβασε':
                                self.input_stat()
                        elif token.recognized_string == 'γράψε':
                                self.print_stat()
                        elif token.recognized_string == 'εκτέλεσε':
                                self.call_stat()
                        else:
                                raise Exception(f'Syntax Error: Unexpected token {token.recognized_string} at line {token.line_number}')

        def assignment_stat(self):
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string(':=')
                self.advance()
                self.expression()
        
        def if_stat(self):
                self.match_string('εάν')
                self.advance()
                self.condition()
                self.match_string('τότε')
                self.advance()
                self.sequence()
                self.elsepart()
                self.match_string('εάν_τέλος')
                self.advance()

        def elsepart(self):
                if self.current_token and self.current_token.recognized_string == 'αλλιώς':
                        self.advance()
                        self.sequence()

        def while_stat(self):
                self.match_string('όσο')
                self.advance()
                self.condition()
                self.match_string('επανάλαβε')
                self.advance()
                self.sequence()
                self.match_string('όσο_τέλος')
                self.advance()

        def do_stat(self):
                self.match_string('επανάλαβε')
                self.advance()
                self.sequence()
                self.match_string('μέχρι')       
                self.advance()
                self.condition()

        def for_stat(self):
                self.match_string('για')
                self.advance()
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string(':=')
                self.advance()
                self.expression()
                self.match_string('εώς')
                self.advance()
                self.expression()
                self.step()
                self.match_string('επανάλαβε')
                self.advance()
                self.sequence()
                self.match_string('για_τέλος')
                self.advance()

        def step(self):
                if self.current_token and self.current_token.recognized_string == 'με_βήμα':
                        self.advance()
                        self.expression()
        
        def print_stat(self):
                self.match_string('γράψε')
                self.advance()
                self.expression()

        def input_stat(self):
                self.match_string('διάβασε')
                self.advance()
                self.match_family('IDENTIFIER')
                self.advance()
                
        def call_stat(self):
                self.match_string('εκτέλεσε')
                self.advance()
                self.match_family('IDENTIFIER')
                self.advance()
                self.idtail()

        def idtail(self):
                if self.current_token and self.current_token.recognized_string == '(':
                        self.actualpars()

        def actualpars(self):
                self.match_string('(')
                self.advance()
                self.actualparlist()
                self.match_string(')')
                self.advance()

        def actualparlist(self):
                if self.current_token and (self.current_token.recognized_string in {'+','-'} or self.current_token.family in {'NUMBER','IDENTIFIER'} or self.current_token.recognized_string == '(' or self.current_token.recognized_string == '%'):
                        self.actualparitem()
                        while self.current_token and self.current_token.recognized_string == ',':
                                self.advance()
                                self.actualparitem()

        def actualparitem(self):
                if self.current_token and (self.current_token.recognized_string in {'+','-'} or self.current_token.family in {'NUMBER','IDENTIFIER'} or self.current_token.recognized_string == '('):
                        self.expression()
                elif self.current_token and self.current_token.recognized_string == '%':
                        self.advance()
                        self.match_family('IDENTIFIER')
                        self.advance()
                else:
                        raise Exception('Syntax Error in actualparitem')

        def condition(self):
                self.boolterm()
                while self.current_token and self.current_token.recognized_string == 'ή':
                        self.advance()
                        self.boolterm()

        def boolterm(self):
                self.boolfactor()
                while self.current_token and self.current_token.recognized_string == 'και':
                        self.advance()
                        self.boolfactor()

        def boolfactor(self):
                if self.current_token.recognized_string == 'όχι':
                        self.advance()
                        self.match_string('[')
                        self.advance()
                        self.condition()
                        self.match_string(']')
                        self.advance()
                elif self.current_token.recognized_string == '[':
                        self.advance()
                        self.condition()
                        self.match_string(']')
                        self.advance()
                else: 
                        self.expression()
                        self.relational_oper()
                        self.expression()

        def expression(self):
                self.optional_sign()
                self.term()
                while self.current_token.recognized_string in {'+', '-'}:
                        self.add_oper()
                        self.term()

        def term(self):
                self.factor()
                while self.current_token.recognized_string in {'*', '/'}:
                        self.mul_oper()
                        self.factor()

        def factor(self):
                if self.current_token.family == 'NUMBER':
                        self.advance()
                elif self.current_token.recognized_string == '(':
                        self.advance()
                        self.expression()
                        self.match_string(')')
                        self.advance()
                elif self.current_token.family == 'IDENTIFIER':
                        self.advance()
                        self.idtail()
                else:
                        raise Exception('Syntax Error in factor')

        def relational_oper(self):
                self.match_family('ASSOCIATIVE OPERATOR')
                self.advance()
                
        def add_oper(self):
                if self.current_token.recognized_string in {'+', '-'}:
                        self.advance()
                else:
                        raise Exception('Syntax Error in add operator')

        def mul_oper(self):
                if self.current_token.recognized_string in {'*', '/'}:
                        self.advance()
                else:
                        raise Exception('Syntax Error in mul operator')
        
        def optional_sign(self):
                if self.current_token and self.current_token.recognized_string in {'+', '-'}:
                        self.add_oper()

########################
## Ενδιαμεσος Κωδικας ##
########################

global quadLabel
quadLabel = 100

class Quad:
        def __init__(self, label, op, op1, op2, op3):
                self.label = label
                self.op = op
                self.op1 = op1
                self.op2 = op2
                self.op3 = op3
        
        def __str__(self):
                return f"{self.label}: '{self.op},{self.op1},{self.op2},{self.op3}'"
        
class QuadPointer:
        def __init__(self, label):
                self.label = label
        
        def __str__(self):
                return f"{self.label}"

class QuadList:
        def __init__(self, programList, quad_counter):
                self.programList = programList
                self.quad_counter = quad_counter
        
        def __str__(self):
                return f"Quad List: {self.programList} \n Number of quads created: {self.quad_counter}"

        def backpatch(self, quadPointerList, label):
                for pointer in quadPointerList.labelList:
                        for quad in self.programList:
                                if quad.label == pointer:
                                        if quad.op3 == '_':
                                                quad.op3 = label

        def genQuad(self, op, op1, op2, op3):
                #global quadLabel
                quad = Quad(quadLabel, op, op1, op2, op3)
                #quadPointer = QuadPointer(quadLabel)
                self.programList.append(quad)
                #self.quadPointers.append(quadPointer)
                quadLabel += 1
                self.quad_counter += 1

        def nextQuad(self):
                #global quadLabel
                return quadLabel
        
        def deleteQuad(self):
                if self.programList:
                        self.programList.pop()
        
        def makeList(self, label):
                return QuadPointerList([label])
        
        def emptyList(self):
                return QuadPointerList([])
        
        def printQuads(self, filename):
                with open(filename, 'w') as f:
                        for q in self.programList:
                                f.write(str(q) + '\n')

class QuadPointerList:
        def __init__(self, labelList):
                self.labelList = labelList
        
        def __str__(self):
                return f"{self.labelList}"

        def mergeList(self, otherList):
                return QuadPointerList(self.labelList + otherList.labelList)
        
        def append(self, label):
                self.labelList.append(label)

######################
## Πινακας Συμβολων ##
######################

class Entity:
        def _init__(self, name):
                self.name = name

class Variable(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.datatype = "INTEGER"
        self.offset = 0
        self.nestinglevel = 0

class Parameter(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.datatype = "INTEGER"
        self.mode = "cv"
        self.offset = 0
        self.nestinglevel = 0

class Function(Entity):
    def __init__(self, name, startingQuad, activationRecord):
        super().__init__(name)
        self.datatype = "INTEGER"
        self.startingQuad = startingQuad
        self.nestinglevel = 0
        self.offset=0
        self.activationRecord=activationRecord

class TemporaryVariable(Entity):
    def __init__(self,name,datatype,offset):
        super().__init__(name)
        self.datatype="INTEGER"
        self.offset=0

class FormalParameters(Entity):
    def __init__(self,datatype,mode):
        super().__init__(name)
        self.datatype="INTEGER"
        self.mode="cv"
        self.nestinglevel=0
        self.offset=0
        
class Scope:
    def __init__(self, name):
        self.name = name
        self.entities = []
        self.nestinglevel = 0

    def insert_entity(self, entity):
        if isinstance(entity, Variable) or isinstance(entity, Parameter) or isinstance(entity, TemporaryVariable) or isinstance(entity, Function):
            if self.entities:
                last_offset = self.entities[-1].offset
                entity.offset = last_offset + 4  
            else:
                entity.offset = 12  
            entity.nestinglevel = self.nestinglevel
        elif isinstance(entity,Function):
            return
        self.entities.append(entity)

    def search_entity(self,name):
        for entity in self.entities:
            if entity.name==name:
                return entity
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Pass a file as an argument")
        sys.exit(1)

    file_name = sys.argv[1]

    try:
        tokens = Lex(file_name).tokenize() # κληση του λεκτικου αναλυτη
        print('Generating tokens...')
        print('Lexical analysis succesfully completed!')
        print('Tokens generated!')
        #for token in tokens:
            #print(token) # τυπωσε τα tokens που βρηκε ο λεκτικος αναλυτης
        parser = Syntax(tokens) # δημιουργια του συντακτικου αναλυτη
        print('\nStarting syntax analysis...')
        parser.program() # εναρξη της συντακτικης αναλυσης
        print('Syntax analysis succesfully completed!')
    except Exception as e:
        print(f'\nError during syntax analysis: {str(e)}')