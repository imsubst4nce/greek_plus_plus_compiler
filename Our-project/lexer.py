#####################
# LEKTIKOS ANALYTIS #
#####################

# A.M 5064 KOUTOULIS CHRISTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11.7

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

        print("-- Lexical Analyzer --")

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
        print("\nFile flushed & closed... Cleaning up... Done!")
    
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


# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Call should look like 'python lexer.py <file_name>'")
        print("Exiting...")
        sys.exit(1)

    file_name = str(sys.argv[1])
    lexer = Lex(file_name)
    # apothikevoume ta tokens gia na ta perasoume meta ston syntax analyzer
    # o opoios tha kanei tin syntaktiki analysh
    tokens = lexer.analyze()
    del lexer # kaloume ton destructor