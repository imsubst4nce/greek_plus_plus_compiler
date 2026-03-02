# Case++ compiler (lexical + syntax analysis)
# Onomateponimo: Nikolaos Koutsounikolis
# Username: cs205108
# A.M 5108

import sys
from enum import Enum, auto

class TokenFamilyEnum(Enum):
    NUMBER = 0
    IDENTIFIER = auto()
    KEYWORD = auto()
    OPERATOR = auto()
    ASSIGNMENT = auto()
    RELATIONAL_OPERATOR = auto()
    DELIMITER = auto()
    GROUP_SYMBOL = auto()
    COMMENT = auto()
    PASS_BY_REFERENCE = auto()
    EOF = auto()
    ERROR = auto()

# Keywords
KEYWORDS = {
    'program', 'declare', 'if', 'else', 'while', 'switchcase', 'when',
    'default', 'whilecase', 'incase', 'untilcase', 'until', 'forcase',
    'return', 'print', 'input', 'function', 'in', 'inout', 'and', 'or', 'not'
}

# Operators and symbols
OPSANDSYMBOLS = {
    '+': (TokenFamilyEnum.OPERATOR, '+'),
    '-': (TokenFamilyEnum.OPERATOR, '-'),
    '*': (TokenFamilyEnum.OPERATOR, '*'),
    '/': (TokenFamilyEnum.OPERATOR, '/'),
    ',': (TokenFamilyEnum.DELIMITER, ','),
    ';': (TokenFamilyEnum.DELIMITER, ';'),
    '(': (TokenFamilyEnum.GROUP_SYMBOL, '('),
    ')': (TokenFamilyEnum.GROUP_SYMBOL, ')'),
    '{': (TokenFamilyEnum.GROUP_SYMBOL, '{'),
    '}': (TokenFamilyEnum.GROUP_SYMBOL, '}'),
    '[': (TokenFamilyEnum.GROUP_SYMBOL, '['),
    ']': (TokenFamilyEnum.GROUP_SYMBOL, ']'),
}

# Whitespace characters
WHITESPACES = {
    ' ',
    '\t',
    '\n',
    '\r'
}

# Maximum word size
MAXWORDSIZE = 30

# Accepted number range
ACCEPTEDNUMBERRANGE = (-32767, 32767)

# Token class
class Token:
    def __init__(self, string, type_, line_number, file_name=None):
        self.string = string
        self.type = type_
        self.line_number = line_number
        self.file_name = file_name

    def __str__(self):
        return f'{self.string}\ttype:"{self.type.name}",\tline: {self.line_number}'

# Lex class
class Lex:
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_char = None
        self.current_line = 1

        print("-- Lexical Analyzer --")

        try:
            print(f"Opening file '{file_name}'...")
            self.file = open(file_name, 'r', encoding='utf-8')
            print(f"Beginning lexical analysis...\n")
            self.next_char()
        except FileNotFoundError:
            print(f"Error: File '{file_name}' not found.")
            sys.exit(1)

    def __del__(self):
        if hasattr(self, 'file'):
            self.file.close()
        print("\n-- Lexical Analyzer finished --")

    def throwLexError(self, errorType, line, invalid_token=''):
        match errorType:
            case 'InvalidTokenError':
                print(f"### Lexical error at line '{line}' => Invalid token '{invalid_token}'. ###")
            case 'InvalidAssignmentError':
                print(f"### Lexical error at line '{line}' => Bad use of ':' operator. Received: '{invalid_token}'. Did you mean to use ':='? ###")
            case 'UnterminatedCommentError':
                print(f"### Lexical error at line '{line}' => Unterminated comment. ###")

    def next_char(self):
        self.current_char = self.file.read(1)
        if self.current_char == '\n':
            self.current_line += 1
        return self.current_char

    def skip_whitespace(self):
        while self.current_char in WHITESPACES:
            self.next_char()

    def get_token(self):
        self.skip_whitespace()

        if not self.current_char:
            return Token("", TokenFamilyEnum.EOF, self.current_line, self.file_name)

        start_line = self.current_line

        if self.current_char.isdigit():
            word = self.current_char
            self.next_char()
            while self.current_char and self.current_char.isdigit():
                word += self.current_char
                self.next_char()
                if len(word) > MAXWORDSIZE:
                    break
            try:
                num = int(word)
                if num < ACCEPTEDNUMBERRANGE[0] or num > ACCEPTEDNUMBERRANGE[1]:
                    self.throwLexError("InvalidTokenError", start_line, word)
                    return Token(word, TokenFamilyEnum.ERROR, start_line, self.file_name)
            except ValueError:
                self.throwLexError("InvalidTokenError", start_line, word)
                return Token(word, TokenFamilyEnum.ERROR, start_line, self.file_name)
            return Token(word, TokenFamilyEnum.NUMBER, start_line, self.file_name)

        if self.current_char.isalpha():
            word = self.current_char
            self.next_char()
            while self.current_char and (self.current_char.isalpha() or self.current_char.isdigit()):
                word += self.current_char
                self.next_char()
                if len(word) > MAXWORDSIZE:
                    break
            token_type = TokenFamilyEnum.KEYWORD if word in KEYWORDS else TokenFamilyEnum.IDENTIFIER
            return Token(word, token_type, start_line, self.file_name)

        if self.current_char in {'<', '>', '=', ':'}:
            line = start_line
            ch = self.current_char
            self.next_char()

            if ch == ':' and self.current_char == '=':
                self.next_char()
                return Token(":=", TokenFamilyEnum.ASSIGNMENT, line, self.file_name)

            if ch == ':':
                return Token(":", TokenFamilyEnum.DELIMITER, line, self.file_name)

            if ch in {'<', '>'} and self.current_char == '=':
                op = ch + '='
                self.next_char()
                return Token(op, TokenFamilyEnum.RELATIONAL_OPERATOR, line, self.file_name)
            if ch == '<' and self.current_char == '>':
                self.next_char()
                return Token("<>", TokenFamilyEnum.RELATIONAL_OPERATOR, line, self.file_name)

            return Token(ch, TokenFamilyEnum.RELATIONAL_OPERATOR, line, self.file_name)

        if self.current_char == '^':
            self.next_char()
            return Token("^", TokenFamilyEnum.PASS_BY_REFERENCE, start_line, self.file_name)

        if self.current_char == '/':
            line = start_line
            self.next_char()

            if self.current_char == '*':
                prev = ''
                self.next_char()
                while self.current_char:
                    if prev == '*' and self.current_char == '/':
                        self.next_char()
                        break
                    prev = self.current_char
                    self.next_char()
                if not self.current_char and prev != '/':
                    self.throwLexError("UnterminatedCommentError", line)
                    return Token("", TokenFamilyEnum.ERROR, line, self.file_name)
                return self.get_token()

            if self.current_char == '/':
                self.next_char()
                while self.current_char and self.current_char != '\n':
                    self.next_char()
                if self.current_char == '\n':
                    self.next_char()
                return self.get_token()

            return Token('/', TokenFamilyEnum.OPERATOR, line, self.file_name)

        if self.current_char in OPSANDSYMBOLS:
            word = self.current_char
            token_type = OPSANDSYMBOLS[self.current_char][0]
            self.next_char()
            return Token(word, token_type, start_line, self.file_name)

        error_char = self.current_char
        self.next_char()
        self.throwLexError("InvalidTokenError", start_line, error_char)
        return Token(error_char, TokenFamilyEnum.ERROR, start_line, self.file_name)

    def analyze(self):
        tokens = []

        while True:
            token = self.get_token()

            if token.type == TokenFamilyEnum.EOF:
                print("-- Reached EOF --")
                break

            tokens.append(token)
            print(token)

        return tokens

class Syntax:
    def __init__(self, tokens):
        eof_line = tokens[-1].line_number if tokens else 0
        self.tokens = tokens + [Token("", TokenFamilyEnum.EOF, eof_line)]
        self.tokenindex = 0
        self.currenttoken = self.tokens[self.tokenindex]
        print("-- Syntax Analyzer --")
        print("Beginning syntax analysis...\n")

    def __del__(self):
        print("-- Syntax Analyzer finished --")

    def get_token(self):
        self.tokenindex += 1
        if self.tokenindex < len(self.tokens):
            self.currenttoken = self.tokens[self.tokenindex]
        return self.currenttoken

    def throwSyntaxError(self, message, expected=None):
        if expected:
            print(f"### Syntax error at line {self.currenttoken.line_number}: Expected {expected}, but got '{self.currenttoken.string}'. ###")
        else:
            print(f"### Syntax error at line {self.currenttoken.line_number}: {message}. ###")
        sys.exit(1)

    def analyze(self):
        self.program()
        if self.currenttoken.type != TokenFamilyEnum.EOF:
            self.throwSyntaxError("Unexpected tokens after end of program")
        print("-- Finished with no errors --")

    def expect_string(self, value):
        if self.currenttoken.string != value:
            self.throwSyntaxError(f"Expected '{value}'", expected=value)
        self.get_token()

    def expect_type(self, token_type, description=None):
        if self.currenttoken.type != token_type:
            self.throwSyntaxError(description or f"Expected {token_type.name}")
        self.get_token()

    def is_statement_start(self, token):
        if token.type == TokenFamilyEnum.IDENTIFIER:
            return True
        return token.string in {
            'if', 'while', 'switchcase', 'whilecase', 'incase', 'forcase',
            'untilcase', 'input', 'print', 'return'
        }

    def program(self):
        self.expect_string('program')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier after 'program'")
        self.programblock()

    def programblock(self):
        self.expect_string('{')
        self.declarations()
        self.functions()
        self.statements_sequence()
        self.expect_string('}')

    def declarations(self):
        while self.currenttoken.string == 'declare':
            self.get_token()
            self.varlist()
            self.expect_string(';')

    def varlist(self):
        if self.currenttoken.type == TokenFamilyEnum.IDENTIFIER:
            self.get_token()
            while self.currenttoken.string == ',':
                self.get_token()
                self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier in varlist")

    def functions(self):
        while self.currenttoken.string == 'function':
            self.function()

    def function(self):
        self.expect_string('function')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected function name")
        self.formalpars()
        self.programblock()

    def formalpars(self):
        self.expect_string('(')
        self.formalparlist()
        self.expect_string(')')

    def formalparlist(self):
        if self.currenttoken.string in {'in', 'inout'}:
            self.formalparitem()
            while self.currenttoken.string == ',':
                self.get_token()
                self.formalparitem()

    def formalparitem(self):
        if self.currenttoken.string not in {'in', 'inout'}:
            self.throwSyntaxError("Expected 'in' or 'inout' in formal parameter list")
        self.get_token()
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier in formal parameters")

    def statements(self):
        if self.currenttoken.string == '{':
            self.get_token()
            self.statements_sequence()
            self.expect_string('}')
        else:
            self.statement()

    def statements_sequence(self):
        if self.is_statement_start(self.currenttoken):
            self.statement()
            while self.currenttoken.string == ';':
                self.get_token()
                if self.is_statement_start(self.currenttoken):
                    self.statement()
                else:
                    break

    def statement(self):
        if self.currenttoken.type == TokenFamilyEnum.IDENTIFIER:
            self.assignment_stat()
        elif self.currenttoken.string == 'if':
            self.if_stat()
        elif self.currenttoken.string == 'while':
            self.while_stat()
        elif self.currenttoken.string == 'switchcase':
            self.switchcase_stat()
        elif self.currenttoken.string == 'whilecase':
            self.whilecase_stat()
        elif self.currenttoken.string == 'incase':
            self.incase_stat()
        elif self.currenttoken.string == 'forcase':
            self.forcase_stat()
        elif self.currenttoken.string == 'untilcase':
            self.untilcase_stat()
        elif self.currenttoken.string == 'input':
            self.input_stat()
        elif self.currenttoken.string == 'print':
            self.print_stat()
        elif self.currenttoken.string == 'return':
            self.return_stat()
        else:
            self.throwSyntaxError("Invalid statement start")

    def assignment_stat(self):
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier in assignment")
        if self.currenttoken.type != TokenFamilyEnum.ASSIGNMENT or self.currenttoken.string != ':=':
            self.throwSyntaxError("Expected ':='", expected=":=")
        self.get_token()
        self.expression()

    def if_stat(self):
        self.expect_string('if')
        self.condition()
        self.statements()
        self.elsepart()

    def elsepart(self):
        if self.currenttoken.string == 'else':
            self.get_token()
            self.statements()

    def while_stat(self):
        self.expect_string('while')
        self.condition()
        self.statements()

    def switchcase_stat(self):
        self.expect_string('switchcase')
        while self.currenttoken.string == 'when':
            self.get_token()
            self.condition()
            self.expect_string(':')
            self.statements()
        self.expect_string('default')
        self.expect_string(':')
        self.statements()

    def whilecase_stat(self):
        self.expect_string('whilecase')
        while self.currenttoken.string == 'when':
            self.get_token()
            self.condition()
            self.expect_string(':')
            self.statements()
        self.expect_string('default')
        self.expect_string(':')
        self.statements()

    def incase_stat(self):
        self.expect_string('incase')
        while self.currenttoken.string == 'when':
            self.get_token()
            self.condition()
            self.expect_string(':')
            self.statements()

    def forcase_stat(self):
        self.expect_string('forcase')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier after 'forcase'")
        self.expect_string('=')
        self.expect_type(TokenFamilyEnum.NUMBER, "Expected integer after '=' in forcase")
        while self.currenttoken.string == 'when':
            self.get_token()
            self.condition()
            self.expect_string(':')
            self.statements()

    def untilcase_stat(self):
        self.expect_string('untilcase')
        while self.currenttoken.string == 'when':
            self.get_token()
            self.condition()
            self.expect_string(':')
            self.statements()
        self.expect_string('until')
        self.condition()

    def input_stat(self):
        self.expect_string('input')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier in input")

    def print_stat(self):
        self.expect_string('print')
        self.expression()

    def return_stat(self):
        self.expect_string('return')
        self.expression()

    def actualpars(self):
        self.expect_string('(')
        self.actualparlist()
        self.expect_string(')')

    def actualparlist(self):
        if self.currenttoken.string in {'in', 'inout'}:
            self.actualparitem()
            while self.currenttoken.string == ',':
                self.get_token()
                self.actualparitem()

    def actualparitem(self):
        if self.currenttoken.string == 'in':
            self.get_token()
            self.expression()
        elif self.currenttoken.string == 'inout':
            self.get_token()
            self.expect_type(TokenFamilyEnum.IDENTIFIER, "Expected identifier after 'inout'")
        else:
            self.throwSyntaxError("Expected 'in' or 'inout' in actual parameter list")

    def condition(self):
        self.boolterm()
        while self.currenttoken.string == 'or':
            self.get_token()
            self.boolterm()

    def boolterm(self):
        self.boolfactor()
        while self.currenttoken.string == 'and':
            self.get_token()
            self.boolfactor()

    def boolfactor(self):
        if self.currenttoken.string == 'not':
            self.get_token()
            self.expect_string('[')
            self.condition()
            self.expect_string(']')
        elif self.currenttoken.string == '[':
            self.get_token()
            self.condition()
            self.expect_string(']')
        else:
            self.expression()
            self.relational_oper()
            self.expression()

    def expression(self):
        self.optional_sign()
        self.term()
        while self.currenttoken.string in {'+', '-'}:
            self.add_oper()
            self.term()

    def term(self):
        self.factor()
        while self.currenttoken.string in {'*', '/'}:
            self.mul_oper()
            self.factor()

    def factor(self):
        if self.currenttoken.type == TokenFamilyEnum.NUMBER:
            self.get_token()
        elif self.currenttoken.string == '(':
            self.get_token()
            self.expression()
            self.expect_string(')')
        elif self.currenttoken.type == TokenFamilyEnum.IDENTIFIER:
            self.get_token()
            self.idtail()
        else:
            self.throwSyntaxError("Invalid factor")

    def idtail(self):
        if self.currenttoken.string == '(':
            self.actualpars()

    def relational_oper(self):
        if self.currenttoken.string in {'=', '<=', '>=', '<>', '<', '>'}:
            self.get_token()
        else:
            self.throwSyntaxError("Expected relational operator (=, <, >, <>, <=, >=)")

    def add_oper(self):
        if self.currenttoken.string in {'+', '-'}:
            self.get_token()
        else:
            self.throwSyntaxError("Expected '+' or '-'")

    def mul_oper(self):
        if self.currenttoken.string in {'*', '/'}:
            self.get_token()
        else:
            self.throwSyntaxError("Expected '*' or '/'")

    def optional_sign(self):
        if self.currenttoken.string in {'+', '-'}:
            self.get_token()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Usage: python compiler.py <filename>.c++")
        sys.exit(1)

    filename = sys.argv[1]
    if not filename.endswith('.c++'):
        print("Error: File must end with .c++")
        sys.exit(1)

    lexer = Lex(filename)
    tokenlist = lexer.analyze()
    del lexer

    parser = Syntax(tokenlist)
    parser.analyze()
    del parser