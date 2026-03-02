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
# SYNTAKTIKOS ANALYTIS #
########################

class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]
        self.symbol_table = SymbolTable()
        self.quad_manager = QuadManager()
        
        # For expression evaluation 
        self.place_stack = []
        # For control flow
        self.if_list = []
        self.while_list = []
        self.for_list = []
        
        print("\n-- Syntax Analyzer --")
        print("Beginning syntactical analysis...\n")

    def __del__(self):
        print("\n-- Syntax Analyzer finished --")

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

    def semantic_error(self, message):
        
        print(f"Semantic Error at line {self.current_token.line_number}: {message}")
        sys.exit(1)

    def analyze(self):
        
        for token in self.tokens:
            if token.type.name == "ERROR":
                self.error(f"Got invalid phrase '{token.string}'")

        self.program()
        print("--No errors--")
        self.quad_manager.print_intermediate_code()

    def program(self):
        if self.current_token.string != "πρόγραμμα":
            self.error("Program should start with 'πρόγραμμα'")

        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.error("'πρόγραμμα' should be followed by <PROGRAM_NAME> of type <IDENTIFIER>")

        
        self.quad_manager.program_name = self.current_token.string

        
        self.declarations()
        next_token = self.next_token()
        if next_token and (next_token.string == "συνάρτηση" or next_token.string == "διαδικασία"):
            self.subprograms()

        
        self.quad_manager.gen_quad("begin_block", self.quad_manager.program_name, "_", "_")

        self.get_token()
        if self.current_token.string != "αρχή_προγράμματος":
            self.error("'αρχή_προγράμματος' not found")

        self.sequence()

        self.get_token()
        if self.current_token.string != "τέλος_προγράμματος":
            self.error("τέλος_προγράμματος", "τέλος_προγράμματος")

        
        self.quad_manager.gen_quad("halt", "_", "_", "_")
        self.quad_manager.gen_quad("end_block", self.quad_manager.program_name, "_", "_")

    def declarations(self):
        if self.next_token().string != "δήλωση":
            return
        while self.next_token().string == "δήλωση":
            self.get_token()
            self.varlist()

    def varlist(self):
        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.error("'δήλωση' should be of type: δήλωση <IDENTIFIER>, ... ,<IDENTIFIER>")

        
        var_name = self.current_token.string
        self.symbol_table.add_symbol(var_name, SymbolType.VARIABLE)

        while self.next_token().string == ',':
            self.get_token()
            self.varlist()

    def subprograms(self):
        if self.next_token().string == "συνάρτηση":
            self.func()
            self.subprograms()
            return
        elif self.next_token().string == "διαδικασία":
            self.proc()
            self.subprograms()
            return
        return

    def func(self):
        self.get_token()
        if self.current_token.string != "συνάρτηση":
            self.error("συνάρτηση", "συνάρτηση")

        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.error("'συνάρτηση' should be followed by <FUNCTION_NAME> of type <IDENTIFIER>")

        
        func_name = self.current_token.string
        self.symbol_table.add_symbol(func_name, SymbolType.FUNCTION)
        
        
        func_symbol = self.symbol_table.lookup(func_name)
        func_symbol.nesting_level = self.symbol_table.current_nesting_level()
        
        
        self.symbol_table.enter_scope(func_name)

        
        entry_label = self.quad_manager.next_quad()
        func_symbol.entry_label = entry_label
        self.quad_manager.gen_quad("begin_block", func_name, "_", "_")

        self.get_token()
        if self.current_token.string != "(":
            self.error("(", "(")

        self.formalparlist()

        self.get_token()
        if self.current_token.string != ")":
            self.error(")", ")")

        self.funcblock()

        
        self.symbol_table.finalize_scope(func_name)
        
        
        func_symbol.frame_length = self.symbol_table.get_frame_length(func_name)
        
        
        self.quad_manager.gen_quad("end_block", func_name, "_", "_")

        
        self.symbol_table.exit_scope()

    def proc(self):
        self.get_token()
        if self.current_token.string != "διαδικασία":
            self.error("διαδικασία", "διαδικασία")

        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.error("'διαδικασία' should be followed by <PROCESS_NAME> of type <IDENTIFIER>")

        
        proc_name = self.current_token.string
        self.symbol_table.add_symbol(proc_name, SymbolType.PROCEDURE)
        
        
        proc_symbol = self.symbol_table.lookup(proc_name)
        proc_symbol.nesting_level = self.symbol_table.current_nesting_level()
        
        
        self.symbol_table.enter_scope(proc_name)

        
        entry_label = self.quad_manager.next_quad()
        proc_symbol.entry_label = entry_label
        self.quad_manager.gen_quad("begin_block", proc_name, "_", "_")

        self.get_token()
        if self.current_token.string != "(":
            self.error("(", "(")

        self.formalparlist()

        self.get_token()
        if self.current_token.string != ")":
            self.error(")", ")")

        self.procblock()

        
        self.symbol_table.finalize_scope(proc_name)
        
        
        proc_symbol.frame_length = self.symbol_table.get_frame_length(proc_name)
        
        
        self.quad_manager.gen_quad("end_block", proc_name, "_", "_")

        
        self.symbol_table.exit_scope()

    def formalparlist(self):
        if self.next_token().string == ")":
            return
        
        
        func_name = self.symbol_table.current_scope()
        
        
        pass_by_reference = False
        if self.next_token().type == TokenFamily.PASSBYREFERENCE:
            self.get_token()  # consume '%'
            pass_by_reference = True
            
        
        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.error("Expected parameter name of type <IDENTIFIER>")
            
        
        param_name = self.current_token.string
        param_mode = "REF" if pass_by_reference else "CV"
        self.symbol_table.add_symbol(param_name, SymbolType.PARAMETER, param_mode)
        
        
        self.symbol_table.add_parameter(func_name, param_name, param_mode)
        
        
        while self.next_token().string == ',':
            self.get_token()  # consume ','
            
            
            pass_by_reference = False
            if self.next_token().type == TokenFamily.PASSBYREFERENCE:
                self.get_token()  # consume '%'
                pass_by_reference = True
                
            self.get_token()  # get  name
            
            if self.current_token.type != TokenFamily.IDENTIFIER:
                self.error("Expected parameter name of type <IDENTIFIER>")
                
            # add  to symbol table
            param_name = self.current_token.string
            param_mode = "REF" if pass_by_reference else "CV"
            self.symbol_table.add_symbol(param_name, SymbolType.PARAMETER, param_mode)
            
            # add   to function/procedure parameter list
            self.symbol_table.add_parameter(func_name, param_name, param_mode)

    def funcblock(self):
        self.get_token()
        if self.current_token.string != "διαπροσωπεία":
            self.error("διαπροσωπεία", "διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.string != "αρχή_συνάρτησης":
            self.error("αρχή_συνάρτησης", "αρχή_συνάρτησης")

        self.sequence()

        self.get_token()
        if self.current_token.string != "τέλος_συνάρτησης":
            self.error("τέλος_συνάρτησης", "τέλος_συνάρτησης")

    def procblock(self):
        self.get_token()
        if self.current_token.string != "διαπροσωπεία":
            self.error("διαπροσωπεία", "διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.string != "αρχή_διαδικασίας":
            self.error("αρχή_διαδικασίας", "αρχή_διαδικασίας")

        self.sequence()

        self.get_token()
        if self.current_token.string != "τέλος_διαδικασίας":
            self.error("τέλος_διαδικασίας", "τέλος_διαδικασίας")

    def funcinput(self):
        if self.next_token().string == "είσοδος":
            self.get_token()
            self.varlist()

    def funcoutput(self):
        if self.next_token().string == "έξοδος":
            self.get_token()
            self.varlist()

    def sequence(self):
        self.statement()
        while self.next_token().string == ';':
            self.get_token()
            self.statement()

    def statement(self):
        next_token = self.next_token()
        if next_token and next_token.type == TokenFamily.IDENTIFIER:
            self.assignment_stat()
            return
        elif next_token and next_token.string == "εάν":
            self.if_stat()
            return
        elif next_token and next_token.string == "όσο":
            self.while_stat()
            return
        elif next_token and next_token.string == "επανάλαβε":
            self.do_stat()
            return
        elif next_token and next_token.string == "για":
            self.for_stat()
            return
        elif next_token and next_token.string == "διάβασε":
            self.input_stat()
            return
        elif next_token and next_token.string == "γράψε":
            self.print_stat()
            return
        elif next_token and next_token.string == "εκτέλεσε":
            self.call_stat()
            return
        
        self.get_token()
        self.error("No assignment or <εάν, όσο, επανάλαβε, για, διάβασε, γράψε, εκτέλεσε> found.\nCheck for unnecessary extra ';' at end of block, unclosed comment or empty program block")

    def assignment_stat(self):
        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.error(f"Expected type {TokenFamily.IDENTIFIER.name}")

        target_var = self.current_token.string

        if not self.symbol_table.lookup(target_var) and not self.symbol_table.lookup_with_nesting(target_var):
            self.error(f"Undeclared variable '{target_var}'")

        self.get_token()
        if self.current_token.type != TokenFamily.ASSIGNMENT:
            self.error(":=", ":=")

        result = self.expression()
        self.quad_manager.gen_quad(":=", result, "_", target_var)
        
        if target_var == self.symbol_table.current_scope:
            func_symbol = self.symbol_table.lookup_in_all_scopes(target_var)
            if func_symbol and func_symbol.symbol_type == SymbolType.FUNCTION:
                self.quad_manager.gen_quad(":=", result, "_", "@RET")

    def if_stat(self):
        self.get_token()
        if self.current_token.string != "εάν":
            self.error("εάν", "εάν")

        # Krataw apotelesmata sinthikwn kai true/false jump listes
        true_list, false_list = self.condition()

        self.get_token()
        if self.current_token.string != "τότε":
            self.error("τότε", "τότε")

        # Ektelw backpatch tis true list stin trexousa tetrada
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

        self.sequence()

        # Dimiourgia jump tetradas gia to telos tis if
        jump_quad = self.quad_manager.gen_quad("jump", "_", "_", "_")
        end_if_list = self.quad_manager.make_list(jump_quad)

        # Ektelw backpatch tis false list stin trexousa tetrada
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.elsepart()

        # Ektelw backpatch tis end_if_list stin trexousa tetrada
        self.quad_manager.backpatch(end_if_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.string != "εάν_τέλος":
            self.error("εάν_τέλος", "εάν_τέλος")

    def elsepart(self):
        if self.next_token().string == "αλλιώς":
            self.get_token()
            self.sequence()

    def while_stat(self):
        self.get_token()
        if self.current_token.string != "όσο":
            self.error("όσο", "όσο")

        # Krataw arxi sinthikwn gia na epistrepsei stin epanalipsi
        while_start = self.quad_manager.next_quad()

        # Krataw apotelesmata sinthikwn kai true/false jump listes
        true_list, false_list = self.condition()

        self.get_token()
        if self.current_token.string != "επανάλαβε":
            self.error("επανάλαβε", "επανάλαβε")

        # Ektelw backpatch tis true list stin trexousa tetrada (loop body)
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

        self.sequence()

        # Paragwgh jump tetradas gia na epistrepsei stin sinthiki
        self.quad_manager.gen_quad("jump", "_", "_", while_start)

        # Ektelw backpatch tis false list stin epomeni tetrada (exit loop)
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.string != "όσο_τέλος":
            self.error("όσο_τέλος", "όσο_τέλος")

    def do_stat(self):
        self.get_token()
        if self.current_token.string != "επανάλαβε":
            self.error("επανάλαβε", "επανάλαβε")

        # Krataw arxi loop body gia na epistrepsei stin epanalipsi
        do_start = self.quad_manager.next_quad()

        self.sequence()

        self.get_token()
        if self.current_token.string != "μέχρι":
            self.syntax_error("μέχρι")

        # Krataw apotelesmata sinthikwn kai true/false jump listes
        true_list, false_list = self.condition()

        # Sto do-until prepei na kanoume jump back stin arxi an h synthiki apotimatai se FALSE
        # Ektelw backpatch tis false list stin arxi
        self.quad_manager.backpatch(false_list, do_start)

        # Ektelw backpatch tis true list stin eksodo (exit loop)
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

    def for_stat(self):
        self.get_token()
        if self.current_token.string != "για":
            self.syntax_error("για")

        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.syntax_error(f"Expected type {TokenFamily.IDENTIFIER.name}")

        counter_var = self.current_token.string

        if not self.symbol_table.lookup(counter_var) and not self.symbol_table.lookup_with_nesting(counter_var):
            self.syntax_error(f"Undeclared variable '{counter_var}'")

        self.get_token()
        if self.current_token.type != TokenFamily.ASSIGNMENT:
            self.syntax_error(f"Expected type {TokenFamily.ASSIGNMENT.name}")

        initial_value = self.expression()
        self.quad_manager.gen_quad(":=", initial_value, "_", counter_var)

        self.get_token()
        if self.current_token.string != "έως":
            self.syntax_error("έως")

        final_value = self.expression()
        final_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad(":=", final_value, "_", final_temp)

        step_value = "1"
        self.step()

        if hasattr(self, 'custom_step_value'):
            step_value = self.custom_step_value
            delattr(self, 'custom_step_value')

        step_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad(":=", step_value, "_", step_temp)

        for_start = self.quad_manager.next_quad()
        loop_body_quad = self.quad_manager.next_quad() + 2

        if step_value.startswith("-"):
            self.quad_manager.gen_quad(">=", counter_var, final_temp, str(loop_body_quad))
        else:
            self.quad_manager.gen_quad("<=", counter_var, final_temp, str(loop_body_quad))

        exit_quad = self.quad_manager.gen_quad("jump", "_", "_", "_")
        false_list = self.quad_manager.make_list(exit_quad)

        self.get_token()
        if self.current_token.string != "επανάλαβε":
            self.syntax_error("επανάλαβε")

        self.sequence()

        inc_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad("+", counter_var, step_temp, inc_temp)
        self.quad_manager.gen_quad(":=", inc_temp, "_", counter_var)

        self.quad_manager.gen_quad("jump", "_", "_", for_start)
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.string != "για_τέλος":
            self.syntax_error("για_τέλος")

    def step(self):
        if self.next_token().string == "με_βήμα":
            self.get_token()
            step_result = self.expression()
            self.custom_step_value = step_result

    def print_stat(self):
        self.get_token()
        if self.current_token.string != "γράψε":
            self.syntax_error("γράψε")

        output_value = self.expression()

        # Paragwgh tetradas ektypwshs
        self.quad_manager.gen_quad("out", output_value, "_", "_")

    def input_stat(self):
        self.get_token()
        if self.current_token.string != "διάβασε":
            self.syntax_error("διάβασε")

        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.syntax_error("'διάβασε' should be followed by type <IDENTIFIER>'")

        var_name = self.current_token.string

        # Elegxos an h metavliti uparxei ston pinaka symbolwn
        if not self.symbol_table.lookup(var_name) and not self.symbol_table.lookup_with_nesting(var_name):
            self.syntax_error(f"Undeclared variable '{var_name}'")

        # Paragwgh tetradas eisodou
        self.quad_manager.gen_quad("in", var_name,"_", "_")

    def call_stat(self):
        self.get_token()
        if self.current_token.string != "εκτέλεσε":
            self.syntax_error("εκτέλεσε")

        self.get_token()
        if self.current_token.type != TokenFamily.IDENTIFIER:
            self.syntax_error("'εκτέλεσε' should be followed by type <IDENTIFIER>'")

        proc_name = self.current_token.string

        # Elegxos an h diadikasia uparxei ston pinaka symbolwn
        proc_symbol = self.symbol_table.lookup(proc_name) or self.symbol_table.lookup_with_nesting(proc_name)
        if not proc_symbol or proc_symbol.symbol_type not in [SymbolType.PROCEDURE, SymbolType.FUNCTION]:
            self.syntax_error(f"Undefined procedure/function '{proc_name}'")

        # Lista parametrwn
        param_list = []

        # Elegxos an yparxoun parametroi
        if self.next_token().string == "(":
            self.get_token() # katanalwsh '('
            
            # Analisi parametrwn
            if self.next_token().string != ")":
                while True:
                    # Xeirismos parametrwn me anafora
                    if self.next_token().type == TokenFamily.PASSBYREFERENCE:
                        self.get_token()  # katanalwsh '%'
                        self.get_token()  # lipsi onomatos parametrou
                        if self.current_token.type != TokenFamily.IDENTIFIER:
                            self.syntax_error("Expected identifier after '%'")
                        param_list.append(("REF", self.current_token.string))
                    else:
                        # Xeirismos parametrwn me timh
                        param_value = self.expression()
                        param_list.append(("CV", param_value))

                    if self.next_token().string != ",":
                        break
                    self.get_token()  # katanalwsh ','

            self.get_token() # katanalwsh ')'

        # Elegxos arithmou parametrwn
        if len(param_list) != len(proc_symbol.parameters):
            self.semantic_error(f"Function/procedure '{proc_name}' expects {len(proc_symbol.parameters)} parameters but got {len(param_list)}")

        # Paragwgi tetradwn parametrwn
        for mode, param in param_list:
            self.quad_manager.gen_quad("par", param, mode, "_")

        # Ean einai synartisi dimiourgia temp gia to apotelesma
        if proc_symbol and proc_symbol.symbol_type == SymbolType.FUNCTION:
            result_temp = self.symbol_table.new_temp()
            self.quad_manager.gen_quad("par", result_temp, "RET", "_")

        # Paragwgh tetradas klhshs
        self.quad_manager.gen_quad("call", proc_name, "_", "_")

        # Ean einai synartisi epistrofi tou temp me to apotelesma
        if proc_symbol and proc_symbol.symbol_type == SymbolType.FUNCTION:
            return result_temp

    def idtail(self, func_name=None):
            
        if self.next_token().string == "(":
            return self.actualpars(func_name)
        return None

    def actualpars(self, func_name):
        self.get_token()
        if self.current_token.string != "(":
            self.syntax_error("(")

        # Elegxos an h synartisi yparxei ston pinaka symbolwn
        func_symbol = self.symbol_table.lookup(func_name) or self.symbol_table.lookup_with_nesting(func_name)
        if not func_symbol or func_symbol.symbol_type not in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
            self.semantic_error(f"Undefined function/procedure '{func_name}'")

        # Check if it's a procedure - procedures cannot be called in expressions
        if func_symbol.symbol_type == SymbolType.PROCEDURE:
            self.semantic_error(f"Procedure '{func_name}' cannot be called in an expression. Use 'εκτέλεσε' statement instead.")

        param_list = []
        if self.next_token().string != ")":
            while True:
                if self.next_token().type == TokenFamily.PASSBYREFERENCE:
                    self.get_token()  # katanalwsh '%'
                    self.get_token()  # lipsi onomatos parametrou
                    if self.current_token.type != TokenFamily.IDENTIFIER:
                        self.syntax_error("Expected identifier after '%'")
                    param_list.append(("REF", self.current_token.string))
                else:
                    param_value = self.expression()
                    param_list.append(("CV", param_value))
                if self.next_token().string != ",":
                    break
                self.get_token()  # katanalwsh ','
        self.get_token()
        if self.current_token.string != ")":
            self.syntax_error(")")

        # Elegxos arithmou parametrwn
        if len(param_list) != len(func_symbol.parameters):
            self.semantic_error(f"Function '{func_name}' expects {len(func_symbol.parameters)} parameters but got {len(param_list)}")

        # Generate quads for parameters
        for mode, param in param_list:
            self.quad_manager.gen_quad("par", param, mode, "_")

        # Only functions have return values - this should only be reached for functions now
        result_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad("par", result_temp, "RET", "_")
        self.quad_manager.gen_quad("call", func_name, "_", "_")
        return result_temp

    def factor(self):
        self.get_token()
        if self.current_token.type == TokenFamily.NUMBER:
            if int(self.current_token.string) < ACCEPTED_NUMBER_RANGE[0] or int(self.current_token.string) > ACCEPTED_NUMBER_RANGE[1]:
                self.syntax_error(f"Got number out of range '{self.current_token.string}'")
            return self.current_token.string
        elif self.current_token.string == "(":
            expr_result = self.expression()
            self.get_token()
            if self.current_token.string != ")":
                self.syntax_error(")")
            return expr_result
        elif self.current_token.type == TokenFamily.IDENTIFIER:
            var_name = self.current_token.string
            func_call_result = self.idtail(var_name)
            if func_call_result is not None:
                return func_call_result
            else:
                # Check if variable exists in current scope or outer scopes
                if not self.symbol_table.lookup(var_name) and not self.symbol_table.lookup_with_nesting(var_name):
                    self.syntax_error(f"Undeclared variable '{var_name}'")
                return var_name
        else:
            self.syntax_error("ID or (Expression) or NUMBER")
            return None

    def condition(self):
        # Krataw boolterm apotelesma kai true/false jump listes
        true_list, false_list = self.boolterm()

        # Epeksergasia OR operator
        while self.next_token().string == "ή":
            self.get_token()

            # Ektelw backpatch tis false list stin epomeni tetrada
            self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

            # Krataw epomeno boolterm apotelesma kai true/false jump listes
            next_true_list, next_false_list = self.boolterm()

            # Sinenwsi twn true lists
            true_list = self.quad_manager.merge_lists(true_list, next_true_list)

            # H nea false list einai h epomeni false list
            false_list = next_false_list

        # Prosarmogi twn jump stoxwn gia tis tetrades sygkrisis
        for quad_index in true_list:
            if 0 < quad_index <= len(self.quad_manager.quads):
                quad_num, op, arg1, arg2, _ = self.quad_manager.quads[quad_index - 1]
                if op in {'<', '>', '<=', '>=', '=', '<>'}:
                    # Gia tous comparison operators, to target einai h epomeni tetrada
                    self.quad_manager.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(self.quad_manager.next_quad()))

        return true_list, false_list

    def boolterm(self):
        # Krataw boolfactor apotelesma kai true/false jump listes
        true_list, false_list = self.boolfactor()

        # Epeksergasia AND operator
        while self.next_token().string == "και":
            self.get_token()

            # Ektelw backpatch tis true list stin epomeni tetrada
            self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

            # Krataw epomeno boolfactor apotelesma kai true/false jump listes
            next_true_list, next_false_list = self.boolfactor()

            # Sinenwsi twn false lists
            false_list = self.quad_manager.merge_lists(false_list, next_false_list)

            # H nea true list einai h epomeni true list
            true_list = next_true_list

        return true_list, false_list

    def boolfactor(self):
        # Elegxos gia NOT operator
        not_flag = False
        if self.next_token().string == "όχι":
            self.get_token()
            not_flag = True

        # Xeirismos sinthikis se parenthesi
        if self.next_token().string == "[":
            self.get_token()
            true_list, false_list = self.condition()
            self.get_token()
            if self.current_token.string != "]":
                self.syntax_error("]")

            # Ean yparxei NOT, kanw swap ta true kai false lists
            if not_flag:
                true_list, false_list = false_list, true_list

            return true_list, false_list

        # Xeirismos relational expression
        left_expr = self.expression()
        rel_op = self.relational_oper()
        right_expr = self.expression()

        # Dhmiourgia tetradas sygkrisis
        comp_quad = self.quad_manager.gen_quad(rel_op, left_expr, right_expr, "_")

        # Dhmiourgia listwn gia true kai false periptwseis
        if not_flag:
            # An yparxei NOT, kanw swap ta true kai false lists
            false_list = self.quad_manager.make_list(comp_quad)
            true_list = self.quad_manager.make_list(self.quad_manager.next_quad())
            # Prosthiki jump gia na skiparei to false case
            self.quad_manager.gen_quad("jump", "_", "_", "_")
        else:
            true_list = self.quad_manager.make_list(comp_quad)
            false_list = self.quad_manager.make_list(self.quad_manager.next_quad())
            # Prothiki jump gia na skiparei to true case
            self.quad_manager.gen_quad("jump", "_", "_", "_")

        return true_list, false_list

    def expression(self):
        # Xeirismos optional sign
        sign = None
        if (self.next_token().string == "+") or (self.next_token().string == "-"):
            sign = self.add_oper()

        # Krataw apotelesma apo term
        term_result = self.term()

        # Epeksergasia arnitikou sign an yparxei
        if sign == "-":
            # Dhmiourgia temp
            neg_temp = self.symbol_table.new_temp()
            self.quad_manager.gen_quad("-", "0", term_result, neg_temp)
            term_result = neg_temp

        # Epeksergasia perissoteron orwn
        while (self.next_token().string == "+") or (self.next_token().string == "-"):
            op = self.add_oper()
            next_term = self.term()

            # Dhmiourgia temp gia to apotelesma
            result_temp = self.symbol_table.new_temp()

            # Dhmiourgia tetradas
            self.quad_manager.gen_quad(op, term_result, next_term, result_temp)

            # Ananewsi tou trexontos apotelesmatos
            term_result = result_temp

        return term_result

    def term(self):
        # Krataw to apotelesma tou factor
        factor_result = self.factor()

        # Epeksergasia perissoteron paragontwn
        while (self.next_token().string == "*") or (self.next_token().string == "/"):
            op = self.mul_oper()
            next_factor = self.factor()

            # Dhmiourgia temp gia to apotelesma
            result_temp = self.symbol_table.new_temp()

            # Dhmiourgia tetradas
            self.quad_manager.gen_quad(op, factor_result, next_factor, result_temp)

            # Ananewsi tou trexontos apotelesmatos
            factor_result = result_temp

        return factor_result

    def relational_oper(self):
        self.get_token()
        if self.current_token.type != TokenFamily.RELATIONAL_OPERATOR:
            self.syntax_error(TokenFamily.RELATIONAL_OPERATOR.name)

        return self.current_token.string

    def add_oper(self):
        self.get_token()
        if (self.current_token.string != "+") and (self.current_token.string != "-"):
            self.syntax_error("+ or -")

        return self.current_token.string

    def mul_oper(self):
        self.get_token()
        if (self.current_token.string != "*") and (self.current_token.string != "/"):
            self.syntax_error("* or /")

        return self.current_token.string

    def optional_sign(self):
        if (self.next_token().string == "+") or (self.next_token().string == "-"):
            return self.add_oper()
        return None


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