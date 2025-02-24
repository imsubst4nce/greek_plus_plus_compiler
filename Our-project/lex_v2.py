import sys
import re
from enum import Enum, auto

# TOKEN FAMILIES 
class TokenType(Enum):
    NUMBER = auto()
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

class Token:
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        return f'{self.recognized_string} family:"{self.family.name}", line: {self.line_number}'

# LEKTIKOS ANALYTIS
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

    def skip_whitespace(self):
        #SKIPAREI KENOUS XARAKTIRES
        while self.current_char in {' ', '\t', '\r', '\n'}:
            if self.current_char == '\n':
                self.current_line += 1
            self.next_char()

    def get_token(self):
        #H SHMANTIKI SYNARTHSH POU THA EKSAGEI TO TOKEN
        self.skip_whitespace()

        if not self.current_char:  # EOF
            return Token("", TokenType.EOF, self.current_line)

        # identifiers kai keywords
        if self.current_char.isalpha() or self.current_char == '_':
            leksi = self.current_char
            self.next_char()
            while self.current_char and (self.current_char.isalnum() or self.current_char == '_'):
                leksi += self.current_char
                self.next_char()
            token_type = TokenType.KEYWORD if leksi in KEYWORDS else TokenType.IDENTIFIER
            return Token(leksi, token_type, self.current_line)

        # akeraioi
        if self.current_char.isdigit():
            leksi = self.current_char
            self.next_char()
            while self.current_char and self.current_char.isdigit():
                leksi += self.current_char
                self.next_char()
            return Token(leksi, TokenType.NUMBER, self.current_line)

        # Relational Operators: <, >, <=, =, >=, <>
        if self.current_char in {'<', '>', '='}:
            leksi = self.current_char
            self.next_char()
            if (leksi in {'<', '>'} and self.current_char == '=') or (leksi == '<' and self.current_char == '>'):  # <=, >=, <>
                leksi += self.current_char
                self.next_char()
            return Token(leksi, TokenType.RELATIONAL_OPERATOR, self.current_line)

        # assignment
        if self.current_char == ':':
            self.next_char()
            if self.current_char == '=':
                self.next_char()
                return Token(":=", TokenType.ASSIGNMENT, self.current_line)
            return Token(":", TokenType.ERROR, self.current_line)  # Invalid ':'
       
        # perasma me anafora
        if self.current_char == '%':
            self.next_char()
            return Token("%", TokenType.PASSBYREFERENCE, self.current_line)
            
        # arithmitikes prakseis kai sumbola
        token_map = {
            '+': TokenType.OPERATOR, '-': TokenType.OPERATOR, '*': TokenType.OPERATOR, '/': TokenType.OPERATOR,
            ';': TokenType.DELIMITER, ',': TokenType.DELIMITER,
            '(': TokenType.GROUP_SYMBOL, ')': TokenType.GROUP_SYMBOL,
            '[': TokenType.GROUP_SYMBOL, ']': TokenType.GROUP_SYMBOL,
        }
        
        if self.current_char in token_map:
            leksi = self.current_char
            token_type = token_map[self.current_char]
            self.next_char()
            return Token(leksi, token_type, self.current_line)

        #sxolia
        if self.current_char == '{':
            while self.current_char and self.current_char != '}':
                self.next_char()
            self.next_char()  
            return self.get_token()  

        # mi dektoi xaraktires
        error_char = self.current_char
        self.next_char()
        return Token(error_char, TokenType.ERROR, self.current_line)

    def analyze(self):
        tokens = []
        while True:
            token = self.get_token()
            if token.family == TokenType.EOF:
                break  
            print(token)  
            tokens.append(token)

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