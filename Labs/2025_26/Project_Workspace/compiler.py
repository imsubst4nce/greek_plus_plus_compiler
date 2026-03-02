# ----------------- MYY802 - COMPILERS ----------------- #
# -------------------- SPRING 2026 --------------------- #
# --------- SEMESTER PROJECT: CASE++ COMPILER ---------- #

# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11

import sys
import os
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

ALLOWEDCHARS = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάέήίόύώΐΰϊϋ"

# Case++ Keywords (σύμφωνα με το επίσημο grammar/spec)
KEYWORDS = {
    'program', 'declare', 'if', 'else', 'while', 'switchcase', 'when',
    'default', 'whilecase', 'incase', 'untilcase', 'until', 'forcase',
    'return', 'print', 'input', 'function', 'in', 'inout', 'and', 'or', 'not'
}

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

WHITESPACES = {
    ' ',
    '\t',
    '\n',
    '\r'
}

MAXWORDSIZE = 30
ACCEPTEDNUMBERRANGE = (-32768, 32767)

class Token:
    def __init__(self, string, type_, line_number, file_name=None):
        self.string = string
        self.type = type_
        self.line_number = line_number
        self.file_name = file_name

    def __str__(self):
        return f'{self.string}\ttype:"{self.type.name}",\tline: {self.line_number}'

class Lex:
    def __init__(self, file_name):
        self.file_name = file_name
        self.current_char = None
        self.current_line = 1

        print("-- Lex Analyzer --")

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
        print("\n-- Lex Analyzer finished --")

    def throwLexError(self, errorType, line, invalid_token=''):
        match errorType:
            case 'InvalidTokenError':
                print(f"### Lexer error at line '{line}' => Invalid token '{invalid_token}'. ###")
            case 'InvalidAssignmentError':
                print(f"### Lexer error at line '{line}' => Bad use of ':' operator. Received: '{invalid_token}'. Did you mean to use ':='? ###")

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

        #########################################
        # Numbers
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
                    self.throwLexError("InvalidTokenError", self.current_line, word)
                    return Token(word, TokenFamilyEnum.ERROR, self.current_line, self.file_name)
            except ValueError:
                self.throwLexError("InvalidTokenError", self.current_line, word)
                return Token(word, TokenFamilyEnum.ERROR, self.current_line, self.file_name)
            return Token(word, TokenFamilyEnum.NUMBER, self.current_line, self.file_name)

        # Identifiers / Keywords
        if self.current_char in ALLOWEDCHARS:
            word = self.current_char
            self.next_char()
            while self.current_char and self.current_char in ALLOWEDCHARS:
                word += self.current_char
                self.next_char()
                if len(word) > MAXWORDSIZE:
                    break
            token_type = TokenFamilyEnum.KEYWORD if word in KEYWORDS else TokenFamilyEnum.IDENTIFIER
            return Token(word, token_type, self.current_line, self.file_name)

        # Relational operators, assignment (:=) and ':' delimiter
        if self.current_char in {'<', '>', '=', ':'}:
            line = self.current_line
            ch = self.current_char
            self.next_char()

            # Assignment :=
            if ch == ':' and self.current_char == '=':
                self.next_char()
                return Token(":=", TokenFamilyEnum.ASSIGNMENT, line, self.file_name)

            # Plain ':' used in case-like constructs
            if ch == ':':
                return Token(":", TokenFamilyEnum.DELIMITER, line, self.file_name)

            # Two-character relational operators: <=, >=, <>
            if ch in {'<', '>'} and self.current_char == '=':
                op = ch + '='
                self.next_char()
                return Token(op, TokenFamilyEnum.RELATIONAL_OPERATOR, line, self.file_name)
            if ch == '<' and self.current_char == '>':
                self.next_char()
                return Token("<>", TokenFamilyEnum.RELATIONAL_OPERATOR, line, self.file_name)

            # Single-character relational operators: <, >, =
            return Token(ch, TokenFamilyEnum.RELATIONAL_OPERATOR, line, self.file_name)

        # Pass by reference ^
        if self.current_char == '^':
            self.next_char()
            return Token("^", TokenFamilyEnum.PASS_BY_REFERENCE, self.current_line, self.file_name)

        # Comments and division operator
        if self.current_char == '/':
            line = self.current_line
            self.next_char()

            # Block comment /* ... */
            if self.current_char == '*':
                prev = ''
                self.next_char()
                while self.current_char:
                    if prev == '*' and self.current_char == '/':
                        self.next_char()
                        break
                    prev = self.current_char
                    self.next_char()
                return self.get_token()

            # Line comment // ...
            if self.current_char == '/':
                self.next_char()
                while self.current_char and self.current_char != '\n':
                    self.next_char()
                if self.current_char == '\n':
                    self.next_char()
                return self.get_token()

            # Division operator '/'
            return Token('/', TokenFamilyEnum.OPERATOR, line, self.file_name)

        # Operators/symbols
        if self.current_char in OPSANDSYMBOLS:
            word = self.current_char
            token_type = OPSANDSYMBOLS[self.current_char][0]
            self.next_char()
            return Token(word, token_type, self.current_line, self.file_name)

        # Error
        error_char = self.current_char
        self.next_char()
        self.throwLexError("InvalidTokenError", self.current_line, error_char)
        return Token(error_char, TokenFamilyEnum.ERROR, self.current_line, self.file_name)

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
        # Append an explicit EOF token to simplify parsing
        eof_line = tokens[-1].line_number if tokens else 0
        self.tokens = tokens + [Token("", TokenFamilyEnum.EOF, eof_line)]
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
        if self.tokenindex >= 0:
            self.currenttoken = self.tokens[self.tokenindex]
        return self.currenttoken

    def error(self, message, expected=None):
        if expected:
            print(f"Syntax Error at line {self.currenttoken.line_number}: Expected {expected}, but got '{self.currenttoken.string}'.")
        else:
            print(f"Syntax Error at line {self.currenttoken.line_number}: {message}.")
        sys.exit(1)

    def analyze(self):
        # Entry point: program
        self.program()
        if self.currenttoken.type != TokenFamilyEnum.EOF:
            self.error("Unexpected tokens after end of program")
        print("-- Finished with no errors --")

    # ---------- Helper methods ----------

    def expect_string(self, value):
        if self.currenttoken.string != value:
            self.error(f"Expected '{value}'", expected=value)
        self.gettoken()

    def expect_type(self, token_type, description=None):
        if self.currenttoken.type != token_type:
            desc = description or token_type.name
            self.error(f"Expected {desc}")
        self.gettoken()

    def is_statement_start(self, token):
        if token.type == TokenFamilyEnum.IDENTIFIER:
            return True  # assignment_stat
        if token.string in {
            'if', 'while', 'switchcase', 'whilecase', 'incase',
            'forcase', 'untilcase', 'input', 'print', 'return'
        }:
            return True
        return False

    # ---------- Grammar implementation ----------

    # program : 'program' ID programblock ;
    def program(self):
        self.expect_string('program')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier after 'program'")
        self.programblock()

    # programblock : '{' declarations functions statements_sequence '}' ;
    def programblock(self):
        self.expect_string('{')
        self.declarations()
        self.functions()
        self.statements_sequence()
        self.expect_string('}')

    # declarations : ( 'declare' varlist ';')* ;
    def declarations(self):
        while self.currenttoken.string == 'declare':
            self.gettoken()
            self.varlist()
            self.expect_string(';')

    # varlist : ID ( ',' ID )* | ε ;
    def varlist(self):
        if self.currenttoken.type == TokenFamilyEnum.IDENTIFIER:
            self.gettoken()
            while self.currenttoken.string == ',':
                self.gettoken()
                self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier in variable list")
        # ε-production: nothing when no identifier

    # functions : ( function )* ;
    def functions(self):
        while self.currenttoken.string == 'function':
            self.function()

    # function : 'function' ID formalpars programblock ;
    def function(self):
        self.expect_string('function')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "function name")
        self.formalpars()
        self.programblock()

    # formalpars : '(' formalparlist ')' ;
    def formalpars(self):
        self.expect_string('(')
        self.formalparlist()
        self.expect_string(')')

    # formalparlist : formalparitem ( ',' formalparitem )* | ε ;
    def formalparlist(self):
        if self.currenttoken.string in {'in', 'inout'}:
            self.formalparitem()
            while self.currenttoken.string == ',':
                self.gettoken()
                self.formalparitem()
        # ε-production otherwise

    # formalparitem : 'in' ID | 'inout' ID ;
    def formalparitem(self):
        if self.currenttoken.string not in {'in', 'inout'}:
            self.error("Expected 'in' or 'inout' in formal parameter list")
        self.gettoken()
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier in formal parameter list")

    # statements : statement | '{' statements_sequence '}' ;
    def statements(self):
        if self.currenttoken.string == '{':
            self.gettoken()
            self.statements_sequence()
            self.expect_string('}')
        else:
            self.statement()

    # statements_sequence : statement ( ';' statement )* | ε ;
    def statements_sequence(self):
        if self.is_statement_start(self.currenttoken):
            self.statement()
            while self.currenttoken.string == ';':
                self.gettoken()
                if self.is_statement_start(self.currenttoken):
                    self.statement()
                else:
                    break
        # ε-production otherwise

    # statement : assignment_stat | if_stat | while_stat | switchcase_stat
    #           | whilecase_stat | incase_stat | forcase_stat | untilcase_stat
    #           | input_stat | print_stat | return_stat ;
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
            self.error("Invalid statement start")

    # assignment_stat : ID ':=' expression ;
    def assignment_stat(self):
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier in assignment")
        if self.currenttoken.type != TokenFamilyEnum.ASSIGNMENT or self.currenttoken.string != ':=':
            self.error("Expected ':=' in assignment", expected=":=")
        self.gettoken()
        self.expression()

    # if_stat : 'if' condition statements elsepart ;
    def if_stat(self):
        self.expect_string('if')
        self.condition()
        self.statements()
        self.elsepart()

    # elsepart : 'else' statements | ε ;
    def elsepart(self):
        if self.currenttoken.string == 'else':
            self.gettoken()
            self.statements()

    # while_stat : 'while' condition statements ;
    def while_stat(self):
        self.expect_string('while')
        self.condition()
        self.statements()

    # switchcase_stat :
    #   'switchcase' ( 'when' condition ':' statements )* 'default' ':' statements ;
    def switchcase_stat(self):
        self.expect_string('switchcase')
        while self.currenttoken.string == 'when':
            self.gettoken()
            self.condition()
            self.expect_string(':')
            self.statements()
        self.expect_string('default')
        self.expect_string(':')
        self.statements()

    # whilecase_stat :
    #   'whilecase' ( 'when' condition ':' statements )* 'default' ':' statements ;
    def whilecase_stat(self):
        self.expect_string('whilecase')
        while self.currenttoken.string == 'when':
            self.gettoken()
            self.condition()
            self.expect_string(':')
            self.statements()
        self.expect_string('default')
        self.expect_string(':')
        self.statements()

    # incase_stat : 'incase' ( 'when' condition ':' statements )* ;
    def incase_stat(self):
        self.expect_string('incase')
        while self.currenttoken.string == 'when':
            self.gettoken()
            self.condition()
            self.expect_string(':')
            self.statements()

    # forcase_stat : 'forcase' ID '=' INTEGER ( 'when' condition ':' statements )* ;
    def forcase_stat(self):
        self.expect_string('forcase')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier after 'forcase'")
        self.expect_string('=')
        self.expect_type(TokenFamilyEnum.NUMBER, "integer value after '=' in forcase")
        while self.currenttoken.string == 'when':
            self.gettoken()
            self.condition()
            self.expect_string(':')
            self.statements()

    # untilcase_stat :
    #   'untilcase' ( 'when' condition ':' statements )* 'until' condition ;
    def untilcase_stat(self):
        self.expect_string('untilcase')
        while self.currenttoken.string == 'when':
            self.gettoken()
            self.condition()
            self.expect_string(':')
            self.statements()
        self.expect_string('until')
        self.condition()

    # input_stat : 'input' ID ;
    def input_stat(self):
        self.expect_string('input')
        self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier in input statement")

    # print_stat : 'print' expression ;
    def print_stat(self):
        self.expect_string('print')
        self.expression()

    # return_stat : 'return' expression ;
    def return_stat(self):
        self.expect_string('return')
        self.expression()

    # actualpars : '(' actualparlist ')' ;
    def actualpars(self):
        self.expect_string('(')
        self.actualparlist()
        self.expect_string(')')

    # actualparlist : actualparitem ( ',' actualparitem )* | ε ;
    def actualparlist(self):
        if self.currenttoken.string in {'in', 'inout'}:
            self.actualparitem()
            while self.currenttoken.string == ',':
                self.gettoken()
                self.actualparitem()
        # ε-production otherwise

    # actualparitem : 'in' expression | 'inout' ID ;
    def actualparitem(self):
        if self.currenttoken.string == 'in':
            self.gettoken()
            self.expression()
        elif self.currenttoken.string == 'inout':
            self.gettoken()
            self.expect_type(TokenFamilyEnum.IDENTIFIER, "identifier in inout actual parameter")
        else:
            self.error("Expected 'in' or 'inout' in actual parameter list")

    # condition : boolterm ( 'or' boolterm )* ;
    def condition(self):
        self.boolterm()
        while self.currenttoken.string == 'or':
            self.gettoken()
            self.boolterm()

    # boolterm : boolfactor ( 'and' boolfactor )* ;
    def boolterm(self):
        self.boolfactor()
        while self.currenttoken.string == 'and':
            self.gettoken()
            self.boolfactor()

    # boolfactor :
    #   'not' '[' condition ']'
    # | '[' condition ']'
    # | expression relational_oper expression ;
    def boolfactor(self):
        if self.currenttoken.string == 'not':
            self.gettoken()
            self.expect_string('[')
            self.condition()
            self.expect_string(']')
        elif self.currenttoken.string == '[':
            self.gettoken()
            self.condition()
            self.expect_string(']')
        else:
            self.expression()
            self.relational_oper()
            self.expression()

    # expression : optional_sign term ( add_oper term )* ;
    def expression(self):
        self.optional_sign()
        self.term()
        while self.currenttoken.string in {'+', '-'}:
            self.add_oper()
            self.term()

    # term : factor ( mul_oper factor )* ;
    def term(self):
        self.factor()
        while self.currenttoken.string in {'*', '/'}:
            self.mul_oper()
            self.factor()

    # factor : INTEGER | '(' expression ')' | ID idtail ;
    def factor(self):
        if self.currenttoken.type == TokenFamilyEnum.NUMBER:
            self.gettoken()
        elif self.currenttoken.string == '(':
            self.gettoken()
            self.expression()
            self.expect_string(')')
        elif self.currenttoken.type == TokenFamilyEnum.IDENTIFIER:
            self.gettoken()
            self.idtail()
        else:
            self.error("Invalid factor")

    # idtail : actualpars | ε ;
    def idtail(self):
        if self.currenttoken.string == '(':
            self.actualpars()
        # ε-production otherwise

    # relational_oper : '=' | '<=' | '>=' | '<>' | '<' | '>' ;
    def relational_oper(self):
        if self.currenttoken.string in {'=', '<=', '>=', '<>', '<', '>'}:
            self.gettoken()
        else:
            self.error("Expected relational operator (=, <, >, <>, <=, >=)")

    # add_oper : '+' | '-' ;
    def add_oper(self):
        if self.currenttoken.string in {'+', '-'}:
            self.gettoken()
        else:
            self.error("Expected '+' or '-'")

    # mul_oper : '*' | '/' ;
    def mul_oper(self):
        if self.currenttoken.string in {'*', '/'}:
            self.gettoken()
        else:
            self.error("Expected '*' or '/'")

    # optional_sign : add_oper | ε ;
    def optional_sign(self):
        if self.currenttoken.string in {'+', '-'}:
            self.gettoken()

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