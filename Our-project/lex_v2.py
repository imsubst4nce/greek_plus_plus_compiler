#####################
# LEKTIKOS ANALYTIS #
#####################

# A.M 5064 KOUTOULIS XRHSTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11

import sys
from enum import Enum, auto

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
    QUOTE = auto()
    COMMENT = auto()
    PASSBYREFERENCE = auto()
    EOF = auto()
    ERROR = auto()

# DESMEYMENES LEKSEIS
KEYWORDS = {
    "πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος",
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "εώς", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "αρχή_συνάρτησης", "τέλος_συνάρτησης",
    "αρχή_διαδικασίας", "τέλος_διαδικασίας", "συνάρτηση", "διαδικασία",
    "διαπροσωπεία", "είσοδος", "έξοδος", "ή", "και", "όχι"
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
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_char = None
        self.current_line = 1

        # ANOIGMA ARXEIOU
        try:
            self.file = open(file_name, 'r', encoding='utf-8')
            self.next_char() 
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            sys.exit(1)

    def next_char(self):
        self.current_char = self.file.read(1)
        return self.current_char
    
    def next_line(self):
        self.current_line += 1
        return self.current_line
    
    # PROSPERNAEI KENOUS XARAKTIRES
    def skip_whitespace(self):
        while self.current_char in WHITESPACES:
            if self.current_char == '\n':
                self.next_line()
            self.next_char()

    # H SHMANTIKI SYNARTHSH POU THA EKSAGEI TO TOKEN
    def get_token(self):
        # TSEKAREI GIA WHITESPACE
        self.skip_whitespace()

        if not self.current_char:  # FTASAME SE EOF
            return Token("", TokenFamily.EOF, self.current_line)

        # identifiers kai keywords
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

        # akeraioi
        if self.current_char.isdigit():
            word = self.current_char
            self.next_char()
            while self.current_char and self.current_char.isdigit():
                word += self.current_char
                self.next_char()
                if(len(word) >= MAX_WORD_SIZE):
                    break
            return Token(word, TokenFamily.NUMBER, self.current_line)

        # relOperators: <, >, <=, =, >=, <>
        if self.current_char in {'<', '>', '='}:
            word = self.current_char
            line = self.current_line
            next_word = self.next_char() # epomeni leksi

            if (next_word == ' '):
                self.next_char()
                return Token(word, TokenFamily.RELATIONAL_OPERATOR, line)
            elif (word in {'<', '>'} and next_word == '=') or (word == '<' and next_word == '>'):  # <=, >=, <>
                word += next_word
                self.next_char()
                return Token(word, TokenFamily.RELATIONAL_OPERATOR, line)
            word += next_word # THELEI DIORTHOSI!!!!
            self.next_char() # AN EXW PARAPANW APO DYO WORDS?
            return Token(word, TokenFamily.ERROR, line)

        # assignment
        if self.current_char == ':':
            self.next_char()
            if self.current_char == '=':
                self.next_char()
                return Token(":=", TokenFamily.ASSIGNMENT, self.current_line)
            return Token(":", TokenFamily.ERROR, self.current_line)  # Invalid ':'
       
        # perasma me anafora
        if self.current_char == '%':
            self.next_char()
            return Token("%", TokenFamily.PASSBYREFERENCE, self.current_line)
            
        # arithmitikes prakseis kai sumbola
        if self.current_char in OPS_AND_SYMBOLS:
            word = self.current_char
            token_type = OPS_AND_SYMBOLS.get(self.current_char)
            self.next_char()
            return Token(word, token_type, self.current_line)

        # sxolia
        if self.current_char == '{':
            while self.current_char and self.current_char != '}':
                if self.current_char == "\n": # se periptwsi pou to sxolio einai pollaples grammes prepei na allazei grammi
                    self.skip_whitespace()
                self.next_char()
            self.next_char()  
            return self.get_token()

        # mi dektoi xaraktires
        error_char = self.current_char
        self.next_char()
        return Token(error_char, TokenFamily.ERROR, self.current_line)

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


# Main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    lexer = Lex(file_name)
    lexer.analyze()