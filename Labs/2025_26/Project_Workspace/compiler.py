""" 
    MYY802 - COMPILERS
    SPRING SEMESTER OF 2026
    SEMESTER PROJECT: CASE++ COMPILER

    A.M 5108 KOUTSONIKOLIS NIKOLAOS
    PYTHON VERSION: 3.11.5
"""

import sys
import os
from enum import Enum, auto

# ---------------- TOKEN DECLARATIONS ---------------- #

# TOKEN FAMILIES
class TokenFamily(Enum):
    NUMBER = 0
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    ASSIGNMENT = auto()
    RELATIONAL_OPERATOR = auto()
    DELIMITER = auto()
    GROUP_SYMBOL = auto()
    COMMENT = auto()
    PASSBYREFERENCE = auto()
    EOF = auto()
    ERROR = auto()

# case++ supported characters
ALLOWED_CHARS = "αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάέήίόύώΐΰϊϋabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"

# supported keywords
KEYWORDS = {
    "πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος",
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "έως", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία",
    "είσοδος", "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας",
    "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", "και", "όχι",
    "εκτέλεσε"
}

# supported operators and symbols
OPS_AND_SYMBOLS = {
    '+': TokenFamily.OPERATOR, '-': TokenFamily.OPERATOR,
    '*': TokenFamily.OPERATOR, '/': TokenFamily.OPERATOR,
    ';': TokenFamily.DELIMITER, ',': TokenFamily.DELIMITER,
    '(': TokenFamily.GROUP_SYMBOL, ')': TokenFamily.GROUP_SYMBOL,
    '[': TokenFamily.GROUP_SYMBOL, ']': TokenFamily.GROUP_SYMBOL,
}

# blank characters and whitespaces
WHITESPACES = {' ', '\t', '\r', '\n'}

# language word size and accepted number range
MAX_WORD_SIZE = 30
ACCEPTED_NUMBER_RANGE = [-32768, 32767]

# error types
INVALID_TOKEN_ERROR = 'InvalidTokenError'
INVALID_ASSIGNMENT_ERROR = 'InvalidAssignmentError'

####################
# Lexical Analysis #
####################

# Token Class
class Token:
    def __init__(self, string, type, line_number, file_name=None):
        self.string = string
        self.type = type
        self.line_number = line_number
        self.file_name = file_name

    def __str__(self):
        return f'{self.string}\ttype:"{self.type.name}",\tline: {self.line_number}'

# Lex Class
class Lex:
    # Constructor method
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_char = None
        self.current_line = 1

        print("-- Lexical Analysis --")

        # File open
        try:
            print(f"Opening file '{file_name}'...")
            self.file = open(file_name, 'r', encoding='utf-8')
            print(f"Beginning lexical analysis...\n")
            self.next_char()
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            sys.exit(1)

    # Destructor method
    def __del__(self):
        print("\n-- Lexical Analysis end --")

    # Lex error method -  doesn't end the program just displays error messages in console
    def throwLexError(self, errorType, line, invalid_token=''):
        match errorType:
            case 'InvalidTokenError':
                print(f"### Lexer error at line '{line}' => Invalid token '{invalid_token}'. ###")
            case 'InvalidAssignmentError':
                print(f"### Lexer error at line '{line}' => Bad use of ':' operator. Received: '{invalid_token}'. Typically only '=' can follow. ###")

    # Next token
    def next_char(self):
        self.current_char = self.file.read(1)
        return self.current_char

    # Next line
    def next_line(self):
        self.current_line += 1
        return self.current_line

    # Bypass whitespaces
    def skip_whitespace(self):
        while self.current_char in WHITESPACES:
            if self.current_char == '\n': # If there is a new line, update the field as well
                self.next_line()
            self.next_char()

    # Key method that exports the token and does the whole job
    def get_token(self):
        # Checks for a whitespace
        self.skip_whitespace()

        # Reached EOF
        if not self.current_char:
            return Token("", TokenFamily.EOF, self.current_line, self.file_name)

        # Integers
        if self.current_char.isdigit():
            word = self.current_char
            self.next_char()
            while self.current_char and self.current_char.isdigit():
                word += self.current_char
                self.next_char()
                if(len(word) >= MAX_WORD_SIZE):
                    break
            # Check if next char is digit or a whitespace
            if self.current_char and (self.current_char in ALLOWED_CHARS):
                word += self.current_char
                self.next_char()
                while self.current_char and (self.current_char in ALLOWED_CHARS):
                    word += self.current_char
                    self.next_char()
                self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, word)
                return Token(word, TokenFamily.ERROR, self.current_line, self.file_name)
            return Token(word, TokenFamily.NUMBER, self.current_line, self.file_name)

        # Identifiers and keywords
        if self.current_char in ALLOWED_CHARS and self.current_char != '_': # Prevent identifiers from starting with underscore
            word = self.current_char
            self.next_char()
            while self.current_char and (self.current_char in ALLOWED_CHARS):
                word += self.current_char
                self.next_char()
                if(len(word) >= MAX_WORD_SIZE):
                    break
            token_type = TokenFamily.KEYWORD if word in KEYWORDS else TokenFamily.IDENTIFIER
            return Token(word, token_type, self.current_line, self.file_name)

        # Relational operators
        if self.current_char in {'<', '>', '='}:
            word = self.current_char
            line = self.current_line
            next_word = self.next_char() # next token
            if (word in {'<', '>'} and next_word == '=') or (word == '<' and next_word == '>'):  # <=, >=, <>
                word += next_word
                self.next_char()
            return Token(word, TokenFamily.RELATIONAL_OPERATOR, line, self.file_name)

        # Assignment
        if self.current_char == ':':
            word = self.current_char
            next_word = self.next_char()
            if next_word == '=':
                assignment = word + next_word
                self.next_char()
                return Token(assignment, TokenFamily.ASSIGNMENT, self.current_line, self.file_name)
            self.throwLexError(INVALID_ASSIGNMENT_ERROR, self.current_line, word+next_word)
            return Token(word+next_word, TokenFamily.ERROR, self.current_line, self.file_name)  # Invalid ':'

        # Pass by reference
        if self.current_char == '%':
            self.next_char()
            return Token("%", TokenFamily.PASSBYREFERENCE, self.current_line, self.file_name)

        # Numeric operators and symbols
        if self.current_char in OPS_AND_SYMBOLS:
            word = self.current_char
            token_type = OPS_AND_SYMBOLS.get(self.current_char)
            self.next_char()
            return Token(word, token_type, self.current_line, self.file_name)

        # Commments
        if self.current_char == '{':
            while self.current_char and self.current_char != '}':
                if self.current_char == "\n": # for multi-line comments
                    self.skip_whitespace()
                self.next_char()
            self.next_char()
            return self.get_token()

        # Non-accepted tokens
        error_char = self.current_char
        self.next_char()
        self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, error_char)
        return Token(error_char, TokenFamily.ERROR, self.current_line, self.file_name)

    # Main method that keeps track of tokens and is responsible for the lexical analysis
    def analyze(self):
        tokens = []

        while True:
            token = self.get_token()

            if token.type == TokenFamily.EOF: # we do not want the EOF token
                print("-- Reached EOF --")
                break

            tokens.append(token)
            print(token)

        self.file.close()
        return tokens

########################
# Syntactical Analysis #
########################

class Syntax:
    # Constructor method
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

        print("\n-- Syntactical Analysis --")
        print("Beginning syntactical analysis...\n")

    # Destructor method
    def __del__(self):
        print("\n-- Syntactical Analysis end --")

    def get_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            return self.current_token

    def next_token(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None

    def previous_token(self):
        self.token_index -= 1
        self.current_token = self.tokens[self.token_index]
        return self.current_token

    def error(self, message, expected=None):
        if expected:
            print(f"Syntax Error at line {self.current_token.line_number}: Expected '{expected}', but got '{self.current_token.string}'.")
        else:
            print(f"Syntax Error at line {self.current_token.line_number}: {message}.")
        sys.exit(1)

    def analyze(self):
        for token in self.tokens:
            if token.type.name == "ERROR":
                self.error(f"Got invalid phrase '{token.string}'")

        self.program()
        print("-- Finished with no errors --")

# Main method
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Usage: 'python compiler.py <file_name>.c++'")
        print("Exiting...")
        sys.exit(1)

    if not sys.argv[1].endswith('.c++'):
        print("Error: File must be of .c++ type")
        print("Exiting...")
        sys.exit(1)

    filename = sys.argv[1]
    
    lexer = Lex(filename)
    token_list = lexer.analyze()
    del lexer
    
    parser = Syntax(token_list)
    parser.analyze()
    del parser