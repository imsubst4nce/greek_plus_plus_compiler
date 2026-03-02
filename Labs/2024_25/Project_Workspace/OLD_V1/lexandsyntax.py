######################################
# LEKTIKOS KAI SYNTAKTIKOS ANALYTIS  #
######################################

# A.M 5064 KOUTOULIS CHRISTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11.7

# O lektikos analytis apotelei to prwto stadio
# eksagei ola ta tokens, anti gia ena ena kai sto deftero stadio
# o syntaktikos analytis ta pairnei ws eisodo
# kai kanei tin syntaktiki analysi
# H ylopoihsh mas einai one-way lektiki se syntaktiki analysh
# kai oxi one-by-one gia kathe token, etsi einai pio grigori

import sys

from enum import Enum, auto

# ---------------- TOKEN DECLARATIONS ---------------- #
# TOKEN FAMILIES 
class TokenFamily(Enum):
    NUMBER = 0 # an ta valw ola auto ksekinaei apo 1
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    ASSIGNMENT = auto()
    RELATIONAL_OPERATOR = auto()
    DELIMITER = auto()
    GROUP_SYMBOL = auto()
    #QUOTE = auto() to vlepoume
    COMMENT = auto()
    PASSBYREFERENCE = auto()
    EOF = auto()
    ERROR = auto()

# DESMEYMENES LEKSEIS
KEYWORDS = {
    "πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος",
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "εώς", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία",
    "είσοδος", "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας",
    "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", "και", "όχι",
    "εκτέλεσε"
}

# PRAKSEIS KAI SYMVOLA
OPS_AND_SYMBOLS = {
    '+': TokenFamily.OPERATOR, '-': TokenFamily.OPERATOR, '*': TokenFamily.OPERATOR, '/': TokenFamily.OPERATOR,
    ';': TokenFamily.DELIMITER, ',': TokenFamily.DELIMITER,
    '(': TokenFamily.GROUP_SYMBOL, ')': TokenFamily.GROUP_SYMBOL,
    '[': TokenFamily.GROUP_SYMBOL, ']': TokenFamily.GROUP_SYMBOL,
}

# KENOI XARAKTIRES
WHITESPACES = {' ', '\t', '\r', '\n'}

# ANWTATOS ARITHMOS XARAKTIRWN LEKSIS
MAX_WORD_SIZE = 30

# ERRORS
INVALID_TOKEN_ERROR = 'InvalidTokenError'
INVALID_ASSIGNMENT_ERROR = 'InvalidAssignmentError'

# ---------------- KLASEIS ---------------- #

# KLASI TOKEN
class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return f'{self.recognized_string}\tfamily:"{self.family.name}",\tline: {self.line_number}'

# KLASI LEKTIKOU ANALYTI
class Lex:
    # CONSTRUCTOR METHODOS
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_char = None
        self.current_line = 1

        print("-- Lex Analyzer --")

        # ANOIGMA ARXEIOU
        try:
            print(f"Opening file '{file_name}'...")
            self.file = open(file_name, 'r', encoding='utf-8')
            print(f"Beginning lectical analysis...\n")
            self.next_char() 
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            sys.exit(1)
    
    # DESTRUCTOR METHODOS
    def __del__(self):
        print("\n-- Lex Analyzer finished --\n")
    
    # LEXER ERROR METHODOS - DEN SKAEI TO PROGRAMMA
    def throwLexError(self, errorType, line, invalid_token=''):
        match errorType:
            case 'InvalidTokenError':
                print(f"### Lexer error at line '{line}' => Invalid token '{invalid_token}'. ###")
            case 'InvalidAssignmentError':
                print(f"### Lexer error at line '{line}' => Bad use of ':' operator. Typically only '=' can follow. ###")

    # EPOMENH LEKSI
    def next_char(self):
        self.current_char = self.file.read(1)
        return self.current_char
    
    # EPOMENH GRAMMI
    def next_line(self):
        self.current_line += 1
        return self.current_line
    
    # PROSPERNAEI KENOUS XARAKTIRES
    def skip_whitespace(self):
        while self.current_char in WHITESPACES:
            if self.current_char == '\n': # AN EXW ALLAGH GRAMMHS ANANEWNW TO PEDIO
                self.next_line()
            self.next_char()

    # H SHMANTIKI SYNARTHSH POU THA EKSAGEI TO TOKEN
    def get_token(self):
        # TSEKAREI GIA WHITESPACE
        self.skip_whitespace()

        if not self.current_char:  # FTASAME SE EOF
            return Token("", TokenFamily.EOF, self.current_line)

        # IDENTIFIERS KAI KEYWORDS
        if self.current_char.isalpha() or self.current_char == '_':
            word = self.current_char
            self.next_char()
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                word += self.current_char
                self.next_char()
                if(len(word) >= MAX_WORD_SIZE):
                    break
            token_type = TokenFamily.KEYWORD if word in KEYWORDS else TokenFamily.IDENTIFIER
            return Token(word, token_type, self.current_line)

        # AKERAIOI
        if self.current_char.isdigit():
            word = self.current_char
            self.next_char()
            while self.current_char and self.current_char.isdigit():
                word += self.current_char
                self.next_char()
                if(len(word) >= MAX_WORD_SIZE):
                    break
            return Token(word, TokenFamily.NUMBER, self.current_line)

        # RELATIONAL OPS: <, >, <=, =, >=, <>
        if self.current_char in {'<', '>', '='}:
            word = self.current_char
            line = self.current_line
            next_word = self.next_char() # epomeni leksi

            if (word in {'<', '>'} and next_word == '=') or (word == '<' and next_word == '>'):  # <=, >=, <>
                word += next_word
                self.next_char()
            return Token(word, TokenFamily.RELATIONAL_OPERATOR, line)

        # ANATHESI
        if self.current_char == ':':
            self.next_char()
            if self.current_char == '=':
                self.next_char()
                return Token(":=", TokenFamily.ASSIGNMENT, self.current_line)
            self.throwLexError(INVALID_ASSIGNMENT_ERROR, self.current_line)
            return Token(":", TokenFamily.ERROR, self.current_line)  # Invalid ':'
       
        # PERASMA ME ANAFORA
        if self.current_char == '%':
            self.next_char()
            return Token("%", TokenFamily.PASSBYREFERENCE, self.current_line)
            
        # ARITHMITIKA OPS KAI SYMVOLA
        if self.current_char in OPS_AND_SYMBOLS:
            word = self.current_char
            token_type = OPS_AND_SYMBOLS.get(self.current_char)
            self.next_char()
            return Token(word, token_type, self.current_line)

        # SXOLIA
        if self.current_char == '{':
            while self.current_char and self.current_char != '}':
                if self.current_char == "\n": # se periptwsi pou to sxolio einai pollaples grammes prepei na allazei grammi
                    self.skip_whitespace()
                self.next_char()
            self.next_char()  
            return self.get_token()

        # mi dektoi xaraktires
        error_char = self.current_char
        self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, error_char)
        self.next_char()
        return Token(error_char, TokenFamily.ERROR, self.current_line)

    # SYNARTHSH POU KANEI TIN ANALYSH
    def analyze(self):
        tokens = []

        while True:
            token = self.get_token()
            
            if token.family == TokenFamily.EOF:
                print("-- Reached EOF --")
                break
            
            tokens.append(token) # DEN THELOUME TO EOF
            print(token)

        self.file.close()
        return tokens



class Syntax:
    # constructor
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

        print("-- Syntax Analyzer --")
        print("Beginning syntactical analysis...\n")

    # destructor
    def __del__(self):
        print("\n-- Syntax Analyzer finished --")
    
    # methodos pou epistrefei tokens
    def get_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            return self.current_token
        
    def throwInvalidError(self):
        print(f"Syntax Error: Got invalid phrase '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)
    
    def throwError(self, expected):
        print(f"Syntax Error: Expected {expected}, but got '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)

    def throwTypeError(self, expected):
        print(f"Syntax Error: Expected type '{expected.name}', but got type '{self.current_token.family.name}' at line {self.current_token.line_number}")
        sys.exit(1)

    # methodos analysis pou ksekinaei tin syntaktiki analysi me ti
    # methodo anadromikis katavasis
    def analyze(self):
        
        for token in self.tokens:
            if token.family.name =="ERROR":
                print(f"Syntax Error: Invalid token '{token.recognized_string}' at line {token.line_number}")
                sys.exit(1)



        self.program()

    # --------------------------------------- #
    # 38 private methodoi grammatikis glwssas #

    #SOS#
    # NA PROSTETHOUN OI ; DELIMITERS KAI ERRORS
    def program(self):
        if self.current_token.recognized_string != "πρόγραμμα":
            self.throwError("πρόγραμμα")

        self.get_token() #move to next token: <ID> 

        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.programblock()
    
    def programblock(self):
        self.declarations()
        self.subprograms()
        self.get_token()
        if self.current_token.recognized_string != "αρχή_προγράμματος":
            self.throwError("αρχή_προγράμματος")
        self.get_token()
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != "τέλος_προγράμματος":
            self.throwError("τέλος_προγράμματος")
    
    def declarations(self):
     
        while self.tokens[self.token_index+1].recognized_string =="δήλωση":
            self.get_token()
            self.varlist() 
        self.get_token()
            
            
    def varlist(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        
        while self.tokens[self.token_index+1].recognized_string ==",":
            self.get_token()
            self.get_token()
            if self.current_token.family != TokenFamily.IDENTIFIER:
                self.throwTypeError(TokenFamily.IDENTIFIER)  
        
    def subprograms(self):
       
        while self.current_token.recognized_string == "συνάρτηση" or self.current_token.recognized_string == "διαδικασία":
            if self.current_token.recognized_string == "συνάρτηση":
                self.func()
            elif self.current_token.recognized_string == "διαδικασία":
                self.proc()
            else:
                self.throwError("συνάρτηση or διαδικασία")
        

    def func(self):
        
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwError("(")
            
        self.formalparlist()
        
        
        if self.current_token.recognized_string != ")":
            self.throwError(")")
        
        self.funcblock()

    def proc(self):
        self.get_token()
        if self.current_token.recognized_string != "διαδικασία":
            self.throwError("διαδικασία")
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwError("(")
        self.get_token()
        self.formalparlist()
        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwError(")")
        self.get_token()
        self.procblock()
            
    def formalparlist(self):
        if self.tokens[self.token_index+1].family == TokenFamily.IDENTIFIER:
            self.varlist()
            self.get_token()
        else: self.get_token()
 
        
    def funcblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.throwError("διαπροσωπεία")
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()
        
        if self.current_token.recognized_string != "αρχή_συνάρτησης":
            self.throwError("αρχή_συνάρτησης")
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != "τέλος_συνάρτησης":
            self.throwError("τέλος_συνάρτησης")
    
    def procblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.throwError("διαπροσωπεία")
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()
        self.get_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            self.throwError("αρχή_διαδικασίας")
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            self.throwError("τέλος_διαδικασίας")
    
    def funcinput(self):
        if self.tokens[self.token_index+1].recognized_string == "είσοδος":
            self.get_token()
            self.varlist()

    def funcoutput(self):
        if self.tokens[self.token_index+1].recognized_string == "έξοδος":
            self.get_token()
            self.varlist()
    
    # to do
    #
    def sequence(self):
        self.statement()
        while self.current_token.recognized_string == ";":
            self.statement()
    
    def statement(self):
        # krufokoitazw mprosta
        next_token_string = self.tokens[self.token_index+1].recognized_string
        next_token_family = self.tokens[self.token_index+1].family

        if next_token_family == TokenFamily.IDENTIFIER:
            self.assignment_stat()
        elif next_token_string == 'εάν':
            self.if_stat()
        elif next_token_string == 'όσο':
            self.while_stat()
        elif next_token_string == 'επανάλαβε':
            self.do_stat()
        elif next_token_string == 'για':
            self.for_stat()
        elif next_token_string == 'διάβασε':
            self.input_stat()
        elif next_token_string == 'γράψε':
            self.print_stat()
        elif next_token_string == 'εκτέλεσε':
            self.call_stat()

        self.throwInvalidError()

    def assignment_stat(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT)
        self.expression()

    def if_stat(self):
        self.get_token()
        self.condition()
        self.get_token()
        if self.current_token.recognized_string != 'τότε':
            self.throwError('τότε')
        self.sequence()
        self.elsepart()
        self.get_token()
        if self.current_token.recognized_string != 'εάν_τότε':
            self.throwError('εάν_τότε')

    def elsepart(self):
        if self.tokens[self.token_index+1].recognized_string == 'αλλιώς':
            self.get_token()
            self.sequence()

    def while_stat(self):
        self.get_token()
        self.condition()
        self.get_token()
        if self.current_token.recognized_string != 'επανάλαβε':
            self.throwError('επανάλαβε')
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != 'όσο_τέλος':
            self.throwError('όσο_τέλος')
        
    def do_stat(self):
        self.get_token()
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != 'μέχρι':
            self.throwError('μέχρι')
        self.condition()
    
    def for_stat(self):
        self.get_token()
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT)
        self.expression()
        self.get_token()
        if self.current_token.recognized_string != 'έως':
            self.throwError('έως')
        self.expression()
        self.step()
        self.get_token()
        if self.current_token.recognized_string != 'επανάλαβε':
            self.throwError('επανάλαβε')
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != 'για_τέλος':
            self.throwError('για_τέλος')
    
    def step(self):
        if self.tokens[self.token_index+1].recognized_string == 'με_βήμα':
            self.get_token()
            self.expression()

    def print_stat(self):
        self.get_token()
        if self.current_token.recognized_string != 'γράψε':
            self.throwError('γράψε')
        self.expression()

    def input_stat(self):
        self.get_token()
        if self.current_token.recognized_string != 'διάβασε':
            self.throwError('διάβασε')
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

    def call_stat(self):
        self.get_token()
        if self.current_token.recognized_string != 'εκτέλεσε':
            self.throwError('εκτέλεσε')
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.idtail()

    def idtail(self):
        if self.tokens[self.token_index+1].recognized_string == '(':
            self.actualpars()

    def actualpars(self):
        self.get_token()
        self.actualparlist()
        self.get_token()
        if self.current_token.recognized_string != ')':
            self.throwError(')')
    
    
    def actualparlist(self):
        self.actualparitem()
        while self.current_token.recognized_string == ",":
            self.actualparitem()
    
    def actualparitem(self):
        self.get_token()
        self.expression()
        if self.current_token.recognized_string == "με_αναφορά":
            self.get_token()
            if self.current_token.family != TokenFamily.IDENTIFIER:
                self.throwTypeError(TokenFamily.IDENTIFIER)

                
    def condition(self):
        self.boolterm()
        while self.current_token.recognized_string == "ή":
            self.boolterm()
    
    def boolterm(self):
        self.boolfactor()
        while self.current_token.recognized_string == "και":
            self.boolfactor()

    def boolfactor(self):
        self.get_token()
        if self.current_token.recognized_string == "όχι":
            self.get_token()
            if self.current_token.recognized_string == "[":
                self.condition()
                self.get_token()
                if self.current_token.recognized_string != "]":
                    self.throwError("]")
        if self.current_token.recognized_string == "[":
            self.condition()
            self.get_token()
            if self.current_token.recognized_string != "]":
                self.throwError("]")
        else:
            self.expression()
            self.relational_oper()
            self.expression()
        
    def expression(self):
        self.optional_sign()
        self.term()
        while self.current_token.recognized_string == '+' or self.current_token.recognized_string == '-':
            self.term()

    def term(self):
        self.factor()
        while self.current_token.recognized_string == '*' or self.current_token.recognized_string == '/':
            self.factor()
    
    def factor(self):
        self.get_token()
        if self.current_token.family == TokenFamily.NUMBER:
            return
        elif self.current_token.family == TokenFamily.IDENTIFIER:
            self.idtail()
        elif self.current_token.recognized_string == '(':
            self.expression()
            self.get_token()
            if self.current_token.recognized_string != ')':
                self.throwError(')')
        

    def relational_oper(self):
        relational_operators = ['=', '<=', '>=', '<>', '<', '>']
        self.get_token()
        if self.current_token.recognized_string not in relational_operators:
            self.throwTypeError(TokenFamily.RELATIONAL_OPERATOR)
            
    def add_oper(self):
        add_operators = ['+', '-']
        self.get_token()
        if self.current_token.recognized_string not in add_operators:
            self.throwError('ADD_OPERATOR')
        
    def mul_oper(self):
        mul_operators = ['*', '/']
        self.get_token()
        if self.current_token.recognized_string not in mul_operators:
            self.throwError('MUL_OPERATOR')
    
    def optional_sign(self):
        next_token = self.tokens[self.token_index+1].recognized_string
        if next_token == '+' or next_token == '-':
            self.add_oper()

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Call should look like 'python syntaxer.py <file_name>'")
        print("Exiting...")
        sys.exit(1)

    if not sys.argv[1].endswith('.gr'):
        print("Error: File must be of .gr type")
        print("Exiting...")
        sys.exit(1)
    file_name = sys.argv[1]
    
    # Kataskevi antikeimenou tis klasis lexer kai klisi 
    # tis methodou lektikis analysis gia eksagwgi twn tokens
    lexer = Lex(file_name)
    tokens = lexer.analyze()
    del lexer

    # Kataskevi antikeimenou tis klasis syntaxer kai
    # klisi tis methodou syntaktikis analysis
    syntaxer = Syntax(tokens)
    syntaxer.analyze()
    del syntaxer
