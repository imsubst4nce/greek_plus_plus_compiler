# ----------------- MYY802 - COMPILERS ----------------- #
# -------------------- SPRING 2025 --------------------- #
# --------- SEMESTER PROJECT: GREEK++ COMPILER --------- #

# A.M 5064 KOUTOULIS CHRISTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11.7

import sys
from enum import Enum, auto

# ---------------- TOKEN DECLARATIONS ---------------- #

# TOKEN FAMILIES 
class TokenFamily(Enum):
    NUMBER = 0 # an ta valw ola auto() ksekinaei apo 1, giafto to vazw apo 0
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
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "έως", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία",
    "είσοδος", "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας",
    "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", "και", "όχι",
    "εκτέλεσε"
}

# PRAKSEIS KAI SYMVOLA
OPS_AND_SYMBOLS = {
    '+': TokenFamily.OPERATOR, '-': TokenFamily.OPERATOR,
    '*': TokenFamily.OPERATOR, '/': TokenFamily.OPERATOR,
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

#####################
# LEKTIKOS ANALYTIS #
#####################

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
            # Tsekare an o epomenos xaraktiras einai psifio h whitespace
            if self.current_char and (self.current_char.isalpha() or self.current_char == '_'):
                word += self.current_char
                self.next_char()
                while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                    word += self.current_char
                    self.next_char()
                self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, word)
                return Token(word, TokenFamily.ERROR, self.current_line)
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
            return Token(":", TokenFamily.ERROR, self.current_line)  # Mh egkyro ':'
       
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
                if self.current_char == "\n": # se periptwsi pou to sxolio einai pollaples grammes prepei na prosmetrountai
                    self.skip_whitespace()
                self.next_char()
            self.next_char()  
            return self.get_token()

        # MI DEKTOI XARAKTIRES
        error_char = self.current_char
        self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, error_char)
        self.next_char()
        return Token(error_char, TokenFamily.ERROR, self.current_line)

    # SYNARTHSH POU KANEI TIN LEKTIKH ANALYSH
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

########################
# SYNTAKTIKOS ANALYTIS #
########################

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

            #to ebala gia na testarw pio token diabazw 
            #print(self.current_token)
            return self.current_token
        
    def next_token(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None

    def previous_token(self):
        self.token_index -= 1
        self.current_token = self.tokens[self.token_index]
        print(self.current_token)
        return self.current_token

    def throwInvalidError(self):
        print(f"Syntax Error at line {self.current_token.line_number}: Got invalid phrase '{self.current_token.recognized_string}'.")
        sys.exit(1)
    
    def error_expected(self, expected):
        print(f"Syntax Error at line {self.current_token.line_number}: Expected '{expected}', but got '{self.current_token.recognized_string}'.")
        sys.exit(1)

    def throwTypeError(self, expected):
        print(f"Syntax Error at line {self.current_token.line_number}: Expected type '{expected.name}', but got type '{self.current_token.family.name}'.")
        sys.exit(1)

    def error_message(self, message):
        print(f"Syntax Error at line {self.current_token.line_number}: {message}.")
        sys.exit(1)
        

    # methodos analysis pou ksekinaei tin syntaktiki analysi me ti
    # methodo anadromikis katavasis
    def analyze(self):
        
        for token in self.tokens:
            if token.family.name =="ERROR":
                print(f"Syntax Error: Lectical analysis found invalid token '{token.recognized_string}' at line {token.line_number}")
                sys.exit(1)

        self.program()
        print(f"--No errors--")


    # --------------------------------------- #
    # 38 private methodoi grammatikis glwssas #

    def program(self):
        #print("entered program()")
        #print(self.current_token)
        if self.current_token.recognized_string != "πρόγραμμα":
            self.error_message("Program should start with 'πρόγραμμα'")
        
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'πρόγραμμα' should be followed by <PROGRAM_NAME> of type <IDENTIFIER>")

        self.programblock()
        
    def programblock(self):
        #print("entered programblock()")

        self.declarations()
        if (self.next_token().recognized_string!="συνάρτηση") and (self.next_token().recognized_string!="διαδικασία"):
            self.get_token()
            self.error_message("No subprograms (functions, processes) were initialised before 'αρχή_προγράμματος'")

        self.subprograms()
        ### continue with arxi programmatos 
        self.get_token()
        if self.current_token.recognized_string!="αρχή_προγράμματος":
            self.error_message("'αρχή_προγράμματος' not found")
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string!="τέλος_προγράμματος":
            self.error_expected("τέλος_προγράμματος")

            

    def declarations(self):
        #print("entered declarations()")

        if self.next_token().recognized_string != "δήλωση":
            return
        while self.next_token().recognized_string == "δήλωση":
            self.get_token()
            self.varlist()

    def varlist(self):
        #print("entered varlist()")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'δήλωση' should be of type: δήλωση <IDENTIFIER>, ... ,<IDENTIFIER>")
        while self.next_token().recognized_string == ',':
            self.get_token()

            self.varlist()
       
        
    def subprograms(self):
        #print("entered subprograms()")

        if self.next_token().recognized_string == "συνάρτηση":
            self.func()
            self.subprograms()
            return
        elif self.next_token().recognized_string == "διαδικασία":
            self.proc()
            self.subprograms()
            return
        


    def func(self):
        #print("entered func()")

        self.get_token()
        if self.current_token.recognized_string != "συνάρτηση":
            self.error_expected("συνάρτηση")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'συνάρτηση' should be followed by <FUNCTION_NAME> of type <IDENTIFIER>")

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.error_expected("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.error_expected(")")

        self.funcblock()


    def proc(self):
        #print("entered proc()")

        self.get_token()
        if self.current_token.recognized_string != "διαδικασία":
            self.error_expected("διαδικασία")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'διαδικασία' should be followed by <PROCESS_NAME> of type <IDENTIFIER>")

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.error_expected("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.error_expected(")")

        self.procblock()

    def formalparlist(self):
        #print("entered formalparlist()")

        if self.next_token().recognized_string == ")":
            return
        self.varlist()

    def funcblock(self):
        #print("entered funcblock()")

        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.error_expected("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_συνάρτησης":
            self.error_expected("αρχή_συνάρτησης")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_συνάρτησης":
            self.error_expected("τέλος_συνάρτησης")


        
    def procblock(self):
        #print("entered procblock()")

        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.error_expected("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            error_expected("αρχή_διαδικασίας")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            self.error_expected("τέλος_διαδικασίας")

    def funcinput(self):
        #print("entered funcinput()")

        if self.next_token().recognized_string == "είσοδος":
            self.get_token()
            self.varlist()
        else:
            return
    

    def funcoutput(self):
        #print("entered funcoutput()")

        if self.next_token().recognized_string == "έξοδος":
            self.get_token()
            self.varlist()
        else:
            return

    def sequence(self):
        #print("entered sequence()")

        self.statement()
        while self.next_token().recognized_string == ';':
            self.get_token()

            self.statement()

    def statement(self):
        #print("entered statement()")

        if self.next_token().family==TokenFamily.IDENTIFIER:
            self.assignment_stat()
            return
        elif self.next_token().recognized_string=="εάν":
            self.if_stat()
            return
        elif self.next_token().recognized_string=="όσο":
            self.while_stat()
            return
        elif self.next_token().recognized_string=="επανάλαβε":
            self.do_stat()
            return
        elif self.next_token().recognized_string=="για":
            self.for_stat()
            return
        elif self.next_token().recognized_string=="διάβασε":
            self.input_stat()
            return
        elif self.next_token().recognized_string=="γράψε":
            self.print_stat()
            return
        elif self.next_token().recognized_string=="εκτέλεσε":
            self.call_stat()
            return  

        #print("\nERROR: NO VALID STATEMENT.\n")
        self.get_token()
        self.error_message("No assignment or <εάν, όσο, επανάλαβε, για, διάβασε, γράψε, εκτέλεσε> found.\nCheck for unnecessary extra ';' at end of block")


            
        ##fix print error here
        #else:
            #self.get_token()
            #self.throwInvalidError()


    def assignment_stat(self):
        #print("entered assignment_stat()")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        self.get_token()
        if self.current_token.family!= TokenFamily.ASSIGNMENT:
            self.error_expected(":=")

        self.expression()

    def if_stat(self):
        #print("entered if_stat()")

        self.get_token()
        if self.current_token.recognized_string!="εάν":
            self.error_expected("εάν")

        self.condition()

        self.get_token()
        if self.current_token.recognized_string!="τότε":
            self.error_expected("τότε")

        self.sequence()
        self.elsepart()

        self.get_token()
        if self.current_token.recognized_string!="εάν_τέλος":
            self.error_expected("εάν_τέλος")

        ##continue

    def elsepart(self):
        #print("entered else_stat()")
        if self.next_token().recognized_string=="αλλιώς":
            self.get_token()
            self.sequence()
        else: return

    def while_stat(self):
        #print("entered while_stat()")
        self.get_token()
        if self.current_token.recognized_string!="όσο":
            self.error_expected("όσο")
        self.condition()

        self.get_token()
        if self.current_token.recognized_string!="επανάλαβε":
            self.error_expected("επανάλαβε")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string!="όσο_τέλος":
            self.error_expected("όσο_τέλος")

    def do_stat(self):
        #print("entered do_stat()")

        self.get_token()
        if self.current_token.recognized_string!="επανάλαβε":
            self.error_expected("επανάλαβε")

        self.sequence()
        self.get_token()
        if self.current_token.recognized_string!="μέχρι":
            self.error_expected("μέχρι")
        self.condition()

    def for_stat(self):
        #print("entered for_stat()")
        self.get_token()
        if self.current_token.recognized_string!="για":
            self.error_expected("για")

        self.get_token()
        if self.current_token.family!=TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        self.get_token()
        if self.current_token.family!=TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT)

        self.expression()
        self.get_token()
        if self.current_token.recognized_string!="έως":
            self.error_expected("έως")
        self.expression()

        self.step()
        self.get_token()
        if self.current_token.recognized_string!="επανάλαβε":
            self.error_expected("επανάλαβε")
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string!="για_τέλος":
            self.error_expected("για_τέλος")


    def step(self):
        if self.next_token().recognized_string=="με_βήμα":
            self.get_token()
            self.expression()
        else: return

    def print_stat(self):
        self.get_token()
        self.expression()

    def input_stat(self):
        self.get_token()
        self.get_token()
        if self.current_token.family!=TokenFamily.IDENTIFIER:
            self.error_message("'διάβασε' should be followed by type <IDENTIFIER>'")

    def call_stat(self):
        self.get_token()
        self.get_token()
        if self.current_token.family!=TokenFamily.IDENTIFIER:
            self.error_message("'εκτέλεσε' should be followed by type <IDENTIFIER>'")
        self.idtail()
        

    def idtail(self):
        #print("entered idtail()")

        if self.next_token().recognized_string == "(":
            self.actualpars()

    def actualpars(self):
        #print("entered actualpars()")

        self.get_token()
        if self.current_token.recognized_string!="(":
            self.error_expected("(")
        self.actualparlist()
        self.get_token()
        if self.current_token.recognized_string!=")":
            self.error_expected(")")


    def actualparlist(self):
        #print("entered actualparlist()")

        if self.next_token().recognized_string==")":
            return
        self.actualparitem()
        while self.next_token().recognized_string==",":
            self.get_token()
            self.actualparitem()

    def actualparitem(self):
        #print("entered actualparitem()")

        if self.next_token().family==TokenFamily.PASSBYREFERENCE:
            self.get_token()

            self.get_token()
            if self.current_token.family!=TokenFamily.IDENTIFIER:
                self.error_message("'%' should be followed by type <IDENTIFIER>'")

            return
        else: self.expression()


    def condition(self):
        #print("entered condition()")

        self.boolterm()
        while self.next_token().recognized_string=="ή":
            self.get_token()
            self.boolterm()

    def boolterm(self):
        #print("entered boolterm()")

        self.boolfactor()
        while self.next_token().recognized_string=="και":
            self.get_token()
            self.boolfactor()

    def boolfactor(self):
        #print("entered boolfactor()")
        if self.next_token().recognized_string == "όχι":
            self.get_token()

            
        if self.next_token().recognized_string=="[":
            self.get_token()
            self.condition()
            self.get_token() 
            if self.current_token.recognized_string!="]":
                self.error_expected("]")
            return
        
        self.expression()
        self.relational_oper()
        self.expression()        



    def expression(self):
        #print("entered expression()")

        self.optional_sign()
        self.term()
        while (self.next_token().recognized_string=="+") or (self.next_token().recognized_string=="-"):
            self.add_oper()
            self.term()

    def term(self):
        #print("entered term()")

        self.factor()
        while (self.next_token().recognized_string=="*") or (self.next_token().recognized_string=="/"):
            self.mul_oper()
            self.factor()

    def factor(self):
        #print("entered factor()")

        self.get_token()
        if self.current_token.family == TokenFamily.NUMBER:
            return
        elif self.current_token.recognized_string=="(":
            self.expression()
            self.get_token()
            if self.current_token.recognized_string!=")":
                self.error_expected(")")  
        elif self.current_token.family==TokenFamily.IDENTIFIER:
            #self.get_token()
            self.idtail()
        else:
            self.error_expected("ID or (Expression) or NUMBER")

    def relational_oper(self):
        #print("entered relational_oper()")

        self.get_token()
        if self.current_token.family!=TokenFamily.RELATIONAL_OPERATOR:
            self.throwTypeError(TokenFamily.RELATIONAL_OPERATOR)


    def add_oper(self):
        #print("entered add_oper()")

        self.get_token()
        if (self.current_token.recognized_string!="+") and (self.current_token.recognized_string!="-"):
            #self.get_token()
            self.error_expected("+ or -")

    def mul_oper(self):
        #print("entered mul_oper()")

        self.get_token()
        if (self.current_token.recognized_string!="*") and (self.current_token.recognized_string!="/"):
            self.error_expected("* or /")

    def optional_sign(self):
        #print("entered optional_sign()")

        if (self.next_token().recognized_string=="+") or (self.next_token().recognized_string=="-"):
            self.add_oper()
        #else: print("no sign")




# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Call should look like 'python syntax.py <file_name>'")
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