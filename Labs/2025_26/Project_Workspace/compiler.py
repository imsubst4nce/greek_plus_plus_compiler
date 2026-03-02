# ----------------- MYY802 - COMPILERS ----------------- #
# -------------------- SPRING 2026 --------------------- #
# --------- SEMESTER PROJECT: CASE++ COMPILER ---------- #

# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11

import sys
from enum import Enum, auto

class TokenFamilyEnum(Enum):
    NUMBER = 0
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    ASSIGNMENT = auto()
    RELATIONALOPERATOR = auto()
    DELIMITER = auto()
    GROUPSYMBOL = auto()
    COMMENT = auto()
    PASSBYREFERENCE = auto()
    EOF = auto()
    ERROR = auto()

# CASE++ supported characters (ίδιοι με CASE)
ALLOWEDCHARS = "αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάέήίόύώΐΰϊϋabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"

# CASE++ KEYWORDS (ΝΕΑ - προσαρμοσμένα από grammar/spec σου)
KEYWORDS = {
    'program', 'declare', 'function', 'in', 'inout', 
    'if', 'else', 'while', 'switchcase', 'whilecase', 'incase', 
    'forcase', 'untilcase', 'print', 'input', 'return', 
    'and', 'or', 'not', 'when', 'default', 'until'
}

# Operators & symbols
OPSANDSYMBOLS = {
    '+': (TokenFamilyEnum.OPERATOR, '+'),
    '-': (TokenFamilyEnum.OPERATOR, '-'),
    '*': (TokenFamilyEnum.OPERATOR, '*'),
    '/': (TokenFamilyEnum.OPERATOR, '/'),
    ',': (TokenFamilyEnum.DELIMITER, ','),
    ';': (TokenFamilyEnum.DELIMITER, ';'),
    '(': (TokenFamilyEnum.GROUPSYMBOL, '('),
    ')': (TokenFamilyEnum.GROUPSYMBOL, ')'),
    '{': (TokenFamilyEnum.GROUPSYMBOL, '{'),
    '}': (TokenFamilyEnum.GROUPSYMBOL, '}')
}

WHITESPACES = set(' \t\n\r')

MAXWORDSIZE = 30
ACCEPTEDNUMBERRANGE = (-32768, 32767)

class Token:
    def __init__(self, string, type_, linenumber, filename=None):
        self.string = string
        self.type = type_
        self.linenumber = linenumber
        self.filename = filename

    def __str__(self):
        return f"{self.string}({self.type.name}), {self.linenumber}"

class Lex:
    def __init__(self, filename):
        self.filename = filename
        self.currentchar = None
        self.currentline = 1
        print("-- Lexical Analysis --")
        try:
            print(f"Opening file {filename}...")
            self.file = open(filename, 'r', encoding='utf-8')
            print("Beginning lexical analysis...")
            self.nextchar()
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
            sys.exit(1)

    def __del__(self):
        print("-- Lexical Analysis end --")

    def throwLexError(self, errorType, line, invalidtoken):
        match errorType:
            case 'InvalidTokenError':
                print(f"Lexer error at line {line}: Invalid token '{invalidtoken}'.")
            case 'InvalidAssignmentError':
                print(f"Lexer error at line {line}: Bad use of ':='. Received '{invalidtoken}'. Typically only ':' can follow.")

    def nextchar(self):
        self.currentchar = self.file.read(1)
        return self.currentchar

    def nextline(self):
        self.currentline += 1
        return self.currentline

    def skipwhitespaces(self):
        while self.currentchar in WHITESPACES:
            if self.currentchar == '\n':
                self.nextline()
            self.nextchar()

    def gettoken(self):
        self.skipwhitespaces()
        if not self.currentchar:
            return Token("", TokenFamilyEnum.EOF, self.currentline, self.filename)

        # Numbers
        if self.currentchar.isdigit():
            word = self.currentchar
            self.nextchar()
            while self.currentchar and self.currentchar.isdigit():
                word += self.currentchar
                self.nextchar()
                if len(word) > MAXWORDSIZE:
                    break
            if int(word) < ACCEPTEDNUMBERRANGE[0] or int(word) > ACCEPTEDNUMBERRANGE[1]:
                self.throwLexError("InvalidTokenError", self.currentline, word)
                return Token(word, TokenFamilyEnum.ERROR, self.currentline, self.filename)
            return Token(word, TokenFamilyEnum.NUMBER, self.currentline, self.filename)

        # Identifiers / Keywords
        if self.currentchar in ALLOWEDCHARS and self.currentchar != '_':  # No underscore start
            word = self.currentchar
            self.nextchar()
            while self.currentchar and self.currentchar in ALLOWEDCHARS:
                word += self.currentchar
                self.nextchar()
                if len(word) > MAXWORDSIZE:
                    break
            tokentype = TokenFamilyEnum.KEYWORD if word in KEYWORDS else TokenFamilyEnum.IDENTIFIER
            return Token(word, tokentype, self.currentline, self.filename)

        # Relational operators (π.χ. ==, <=)
        if self.currentchar in {'<', '>', '='}:
            word = self.currentchar
            line = self.currentline
            self.nextchar()
            nextword = self.nextchar()
            if word in {'<', '>'} and nextword == '=':
                word += nextword
                self.nextchar()
            elif word == '=' and nextword == ':':  # :=
                assignment = word + nextword
                self.nextchar()
                return Token(assignment, TokenFamilyEnum.ASSIGNMENT, self.currentline, self.filename)
            return Token(word, TokenFamilyEnum.RELATIONALOPERATOR, line, self.filename)

        # Pass by reference ^
        if self.currentchar == '^':
            self.nextchar()
            return Token("^", TokenFamilyEnum.PASSBYREFERENCE, self.currentline, self.filename)

        # Operators/symbols
        if self.currentchar in OPSANDSYMBOLS:
            word = self.currentchar
            tokentype = OPSANDSYMBOLS[self.currentchar][0]
            self.nextchar()
            return Token(word, tokentype, self.currentline, self.filename)

        # # Comments /* */
        # if self.currentchar == '/':
        #     self.nextchar()
        #     if self.currentchar == '/':
        #         self.nextline()
        #         self.nextchar()
        #     if self.currentchar == '*':
        #         self.skipwhitespaces()
        #         self.nextchar()
        #         self.nextchar()
        #         return self.gettoken()
        # errorchar = self.currentchar
        # self.nextchar()
        # self.throwLexError("InvalidTokenError", self.currentline, errorchar)
        # return Token(errorchar, TokenFamilyEnum.ERROR, self.currentline, self.filename)

    def analyze(self):
        tokens = []
        while True:
            token = self.gettoken()
            if token.type == TokenFamilyEnum.EOF:
                print("-- Reached EOF --")
                break
            tokens.append(token)
            print(token)
        self.file.close()
        return tokens

class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.tokenindex = 0
        self.currenttoken = self.tokens[self.tokenindex]
        print("-- Syntactical Analysis --")
        print("Beginning syntactical analysis...")

    def __del__(self):
        print("-- Syntactical Analysis end --")

    def gettoken(self):
        self.tokenindex += 1
        if self.tokenindex < len(self.tokens):
            self.currenttoken = self.tokens[self.tokenindex]
            return self.currenttoken

    def nexttoken(self):
        if self.tokenindex + 1 < len(self.tokens):
            return self.tokens[self.tokenindex + 1]
        return None

    def previoustoken(self):
        self.tokenindex -= 1
        self.currenttoken = self.tokens[self.tokenindex]
        return self.currenttoken

    def error(self, message, expected=None):
        if expected:
            print(f"Syntax Error at line {self.currenttoken.linenumber}: Expected {expected}, but got '{self.currenttoken.string}'.")
        else:
            print(f"Syntax Error at line {self.currenttoken.linenumber}: {message}.")
        sys.exit(1)

    def analyze(self):
        # Βασικός έλεγχος CASE++ grammar (επέκταση για caseblock, forcase++ κλπ)
        i = 0
        while i < len(self.tokens):
            token = self.tokens[i]
            if token.type.name == 'ERROR':
                self.error(f"Got invalid phrase '{token.string}'")
            # Νέος έλεγχος π.χ. για case++ ID { ... }
            if token.string == 'case++':
                if i+1 >= len(self.tokens) or self.tokens[i+1].type != TokenFamilyEnum.IDENTIFIER:
                    self.error("Expected ID after case++")
                i += 3  # skip ID {
            # Άλλοι έλεγχοι από grammar: declare++, iff condition { ...
            i += 1
        print("-- Finished with no errors --")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Usage python compiler.py <filename>.c++")
        print("Exiting...")
        sys.exit(1)

    if not sys.argv[1].endswith('.c++'):
        print("Error: File must be of .c++ type")
        print("Exiting...")
        sys.exit(1)

    filename = sys.argv[1]

    lexer = Lex(filename)
    tokenlist = lexer.analyze()
    del lexer

    parser = Syntax(tokenlist)
    parser.analyze()
    del parser