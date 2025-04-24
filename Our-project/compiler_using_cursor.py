# ----------------- MYY802 - COMPILERS ----------------- #
# -------------------- SPRING 2025 --------------------- #
# --------- SEMESTER PROJECT: GREEK++ COMPILER --------- #

# A.M 5064 KOUTOULIS CHRISTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11.7

import sys
import os
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
    def __init__(self, recognized_string, family, line_number, file_name=None):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number
        self.file_name = file_name

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
        print("\n-- Lex Analyzer finished --")

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
            return Token("", TokenFamily.EOF, self.current_line, self.file_name)

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
            return Token(word, token_type, self.current_line, self.file_name)

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
                return Token(word, TokenFamily.ERROR, self.current_line, self.file_name)
            return Token(word, TokenFamily.NUMBER, self.current_line, self.file_name)

        # RELATIONAL OPS: <, >, <=, =, >=, <>
        if self.current_char in {'<', '>', '='}:
            word = self.current_char
            line = self.current_line
            next_word = self.next_char() # epomeni leksi

            if (word in {'<', '>'} and next_word == '=') or (word == '<' and next_word == '>'):  # <=, >=, <>
                word += next_word
                self.next_char()
            return Token(word, TokenFamily.RELATIONAL_OPERATOR, line, self.file_name)

        # ANATHESI
        if self.current_char == ':':
            self.next_char()
            if self.current_char == '=':
                self.next_char()
                return Token(":=", TokenFamily.ASSIGNMENT, self.current_line, self.file_name)
            self.throwLexError(INVALID_ASSIGNMENT_ERROR, self.current_line)
            return Token(":", TokenFamily.ERROR, self.current_line, self.file_name)  # Invalid ':'

        # PERASMA ME ANAFORA
        if self.current_char == '%':
            self.next_char()
            return Token("%", TokenFamily.PASSBYREFERENCE, self.current_line, self.file_name)

        # ARITHMITIKA OPS KAI SYMVOLA
        if self.current_char in OPS_AND_SYMBOLS:
            word = self.current_char
            token_type = OPS_AND_SYMBOLS.get(self.current_char)
            self.next_char()
            return Token(word, token_type, self.current_line, self.file_name)

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
        return Token(error_char, TokenFamily.ERROR, self.current_line, self.file_name)

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

# -------------------- NEW CODE -------------------- #

####################
# PINAKAS SYMBOLWN #
####################

class SymbolType(Enum):
    VARIABLE = auto()
    FUNCTION = auto()
    PROCEDURE = auto()
    PARAMETER = auto()
    TEMPORARY = auto()

class Symbol:
    def __init__(self, name, symbol_type, scope="global", offset=0, parameter_mode=None):
        self.name = name
        self.symbol_type = symbol_type
        self.scope = scope
        self.offset = offset  # Memory offset
        self.parameter_mode = parameter_mode  # CV (Call by Value) or REF (Call by Reference)

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.current_scope = "global"
        self.offset = 0
        self.temp_counter = 0

    def enter_scope(self, scope_name):
        self.current_scope = scope_name
        self.offset = 0  # Reset offset for new scope

    def exit_scope(self):
        self.current_scope = "global"

    def add_symbol(self, name, symbol_type, parameter_mode=None):
        key = (name, self.current_scope)
        if key in self.symbols:
            return False  # Symbol already exists in current scope

        self.symbols[key] = Symbol(name, symbol_type, self.current_scope, self.offset, parameter_mode)
        self.offset += 4  # Assuming 4 bytes per variable
        return True

    def lookup(self, name, scope=None):
        if scope is None:
            scope = self.current_scope

        # Check in specified scope
        key = (name, scope)
        if key in self.symbols:
            return self.symbols[key]

        # If not found and we're in a local scope, check global
        if scope != "global":
            key = (name, "global")
            if key in self.symbols:
                return self.symbols[key]

        return None

    def new_temp(self):
        """Create a new temporary variable and return its name"""
        temp_name = f"t@{self.temp_counter}"  # Use lowercase t@
        self.temp_counter += 1
        self.add_symbol(temp_name, SymbolType.TEMPORARY)
        return temp_name

    def print_scope_info(self, output_file=None):
        """Print or save the symbol table scope information"""
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Symbol Table Scope Information\n")
                f.write("=" * 50 + "\n\n")

                # Group symbols by scope
                scopes = {}
                for (name, scope), symbol in self.symbols.items():
                    if scope not in scopes:
                        scopes[scope] = []
                    scopes[scope].append(symbol)

                # Print global scope first
                if "global" in scopes:
                    f.write("Global Scope:\n")
                    f.write("-" * 20 + "\n")
                    for symbol in scopes["global"]:
                        f.write(f"Name: {symbol.name}\n")
                        f.write(f"Type: {symbol.symbol_type.name}\n")
                        f.write(f"Offset: {symbol.offset}\n")
                        if symbol.parameter_mode:
                            f.write(f"Parameter Mode: {symbol.parameter_mode}\n")
                        f.write("\n")
                    del scopes["global"]

                # Print other scopes
                for scope, symbols in scopes.items():
                    f.write(f"Scope: {scope}\n")
                    f.write("-" * 20 + "\n")
                    for symbol in symbols:
                        f.write(f"Name: {symbol.name}\n")
                        f.write(f"Type: {symbol.symbol_type.name}\n")
                        f.write(f"Offset: {symbol.offset}\n")
                        if symbol.parameter_mode:
                            f.write(f"Parameter Mode: {symbol.parameter_mode}\n")
                        f.write("\n")
        else:
            print("\nSymbol Table Scope Information")
            print("=" * 50)

            # Group symbols by scope
            scopes = {}
            for (name, scope), symbol in self.symbols.items():
                if scope not in scopes:
                    scopes[scope] = []
                scopes[scope].append(symbol)

            # Print global scope first
            if "global" in scopes:
                print("\nGlobal Scope:")
                print("-" * 20)
                for symbol in scopes["global"]:
                    print(f"Name: {symbol.name}")
                    print(f"Type: {symbol.symbol_type.name}")
                    print(f"Offset: {symbol.offset}")
                    if symbol.parameter_mode:
                        print(f"Parameter Mode: {symbol.parameter_mode}")
                    print()
                del scopes["global"]

            # Print other scopes
            for scope, symbols in scopes.items():
                print(f"\nScope: {scope}")
                print("-" * 20)
                for symbol in symbols:
                    print(f"Name: {symbol.name}")
                    print(f"Type: {symbol.symbol_type.name}")
                    print(f"Offset: {symbol.offset}")
                    if symbol.parameter_mode:
                        print(f"Parameter Mode: {symbol.parameter_mode}")
                    print()

#########################
# DIAXEIRISTIS TETRADWN # 
#########################

class QuadManager:
    def __init__(self):
        self.quads = []
        self.next_label = 1  # Start from 1 instead of 0
        self.program_name = ""

    def gen_quad(self, op, arg1, arg2, result):
        """Generate a new quad and add it to the list"""
        quad = (self.next_label, op, arg1, arg2, result)  # Use next_label instead of len(quads)
        self.quads.append(quad)
        self.next_label += 1  # Increment next_label
        return self.next_label - 1  # Return the current label

    def next_quad(self):
        """Return the label of the next quad"""
        return self.next_label

    def backpatch(self, list_of_quads, label):
        """Fill in the result field of quads in the list with label"""
        for quad_index in list_of_quads:
            if 0 < quad_index <= len(self.quads):
                quad_num, op, arg1, arg2, _ = self.quads[quad_index - 1]
                if op in {'<', '>', '<=', '>=', '=', '<>'}:
                    # For comparison operators, target is the next quad
                    self.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(label ))
                else:
                    # For jumps, target is the label
                    self.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(label))

    def merge_lists(self, list1, list2):
        """Merge two lists of quad indices"""
        return list1 + list2

    def make_list(self, quad_index):
        """Create a new list containing only quad_index"""
        return [quad_index]

    def print_intermediate_code(self, output_file=None):
        """Print or save the generated intermediate code"""
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Program: {self.program_name}\n")
                f.write("-" * 50 + "\n")
                for quad_num, op, arg1, arg2, result in self.quads:
                    # Format operands to match test1.int style
                    arg1 = arg1 if arg1 != "_" else "_"
                    arg2 = arg2 if arg2 != "_" else "_"
                    result = result if result != "_" else "_"
                    f.write(f"{quad_num} : {op} , {arg1} , {arg2} , {result}\n")
                # Add halt instruction before end_block
                f.write(f"{self.next_label} : halt , _ , _ , _\n")
                # Add end_block instruction only if not already present
                if not any(q[1] == "end_block" for q in self.quads):
                    f.write(f"{self.next_label + 1} : end_block , {self.program_name} , _ , _\n")
        else:
            print("\n-- Intermediate Code --")
            print(f"Program: {self.program_name}")
            print("-" * 50)
            for quad_num, op, arg1, arg2, result in self.quads:
                # Format operands to match test1.int style
                arg1 = arg1 if arg1 != "_" else "_"
                arg2 = arg2 if arg2 != "_" else "_"
                result = result if result != "_" else "_"
                print(f"{quad_num} : {op} , {arg1} , {arg2} , {result}")

########################
# SYNTAKTIKOS ANALYTIS #
########################

class Syntax:
    # constructor
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

        # Store function blocks to be generated after their calls
        self.function_blocks = {}

        print("\n-- Syntax Analyzer --")
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

    def next_token(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None

    def previous_token(self):
        self.token_index -= 1
        self.current_token = self.tokens[self.token_index]
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
            if token.family.name == "ERROR":
                print(f"Syntax Error: Lectical analysis found invalid token '{token.recognized_string}' at line {token.line_number}")
                sys.exit(1)

        self.program()
        print(f"--No errors--")

        # Print intermediate code
        self.quad_manager.print_intermediate_code()

        # Get the input filename from the lexer's file_name attribute
        input_file = self.tokens[0].file_name if hasattr(self.tokens[0], 'file_name') else "output"
        # Get just the filename without path
        input_filename = os.path.basename(input_file)
        # Replace .gr extension with .int
        output_filename = input_filename.replace('.gr', '.int')

        # Save to file with .int extension in current directory
        self.quad_manager.print_intermediate_code(output_filename)
        print(f"\nIntermediate code saved to: {output_filename}")

        # Save symbol table scope information
        scope_filename = input_filename.replace('.gr', '.sym')
        self.symbol_table.print_scope_info(scope_filename)
        print(f"Symbol table scope information saved to: {scope_filename}")

    # --------------------------------------- #
    # Modified methods for intermediate code generation #

    def program(self):
        if self.current_token.recognized_string != "πρόγραμμα":
            self.error_message("Program should start with 'πρόγραμμα'")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'πρόγραμμα' should be followed by <PROGRAM_NAME> of type <IDENTIFIER>")

        # Set program name
        self.quad_manager.program_name = self.current_token.recognized_string

        # Start with program
        self.quad_manager.gen_quad("begin_block", self.current_token.recognized_string, "_", "_")

        self.programblock()

        # End program
        self.quad_manager.gen_quad("halt", "_", "_", "_")
        self.quad_manager.gen_quad("end_block", self.quad_manager.program_name, "_", "_")

    def programblock(self):
        self.declarations()
        if (self.next_token().recognized_string == "συνάρτηση") or (self.next_token().recognized_string == "διαδικασία"):
            self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_προγράμματος":
            self.error_message("'αρχή_προγράμματος' not found")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_προγράμματος":
            self.error_expected("τέλος_προγράμματος")

    def declarations(self):
        if self.next_token().recognized_string != "δήλωση":
            return
        while self.next_token().recognized_string == "δήλωση":
            self.get_token()
            self.varlist()

    def varlist(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'δήλωση' should be of type: δήλωση <IDENTIFIER>, ... ,<IDENTIFIER>")

        # Add variable to symbol table
        var_name = self.current_token.recognized_string
        self.symbol_table.add_symbol(var_name, SymbolType.VARIABLE)

        while self.next_token().recognized_string == ',':
            self.get_token()
            self.varlist()

    def subprograms(self):
        if self.next_token().recognized_string == "συνάρτηση":
            self.func()
            self.subprograms()
            return
        elif self.next_token().recognized_string == "διαδικασία":
            self.proc()
            self.subprograms()
            return

    def func(self):
        self.get_token()
        if self.current_token.recognized_string != "συνάρτηση":
            self.error_expected("συνάρτηση")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'συνάρτηση' should be followed by <FUNCTION_NAME> of type <IDENTIFIER>")

        # Add function to symbol table and set current scope
        func_name = self.current_token.recognized_string
        self.symbol_table.add_symbol(func_name, SymbolType.FUNCTION)
        self.symbol_table.enter_scope(func_name)

        # Store the current quad position for this function
        start_quad = self.quad_manager.next_quad()

        # Generate function begin quad
        self.quad_manager.gen_quad("begin_block", func_name, "_", "_")

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.error_expected("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.error_expected(")")

        # Store the function block instead of generating it immediately
        self.function_blocks[func_name] = {
            'start_quad': start_quad,
            'end_quad': None,  # Will be set when we generate the end block
            'scope': func_name
        }

        self.funcblock()

        # Return to global scope
        self.symbol_table.exit_scope()

    def proc(self):
        self.get_token()
        if self.current_token.recognized_string != "διαδικασία":
            self.error_expected("διαδικασία")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'διαδικασία' should be followed by <PROCESS_NAME> of type <IDENTIFIER>")

        # Add procedure to symbol table and set current scope
        proc_name = self.current_token.recognized_string
        self.symbol_table.add_symbol(proc_name, SymbolType.PROCEDURE)
        self.symbol_table.enter_scope(proc_name)

        # Store the current quad position for this procedure
        start_quad = self.quad_manager.next_quad()

        # Generate procedure begin quad
        self.quad_manager.gen_quad("begin_block", proc_name, "_", "_")

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.error_expected("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.error_expected(")")

        # Store the procedure block instead of generating it immediately
        self.function_blocks[proc_name] = {
            'start_quad': start_quad,
            'end_quad': None,  # Will be set when we generate the end block
            'scope': proc_name
        }

        self.procblock()

        # Return to global scope
        self.symbol_table.exit_scope()

    def formalparlist(self):
        if self.next_token().recognized_string == ")":
            return
        self.varlist()

    def funcblock(self):
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
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.error_expected("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            self.error_expected("αρχή_διαδικασίας")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            self.error_expected("τέλος_διαδικασίας")

    def funcinput(self):
        if self.next_token().recognized_string == "είσοδος":
            self.get_token()
            self.varlist()
        else:
            return

    def funcoutput(self):
        if self.next_token().recognized_string == "έξοδος":
            self.get_token()
            self.varlist()
        else:
            return

    def sequence(self):
        self.statement()
        while self.next_token().recognized_string == ';':
            self.get_token()
            self.statement()

    def statement(self):
        if self.next_token().family == TokenFamily.IDENTIFIER:
            self.assignment_stat()
            return
        elif self.next_token().recognized_string == "εάν":
            self.if_stat()
            return
        elif self.next_token().recognized_string == "όσο":
            self.while_stat()
            return
        elif self.next_token().recognized_string == "επανάλαβε":
            self.do_stat()
            return
        elif self.next_token().recognized_string == "για":
            self.for_stat()
            return
        elif self.next_token().recognized_string == "διάβασε":
            self.input_stat()
            return
        elif self.next_token().recognized_string == "γράψε":
            self.print_stat()
            return
        elif self.next_token().recognized_string == "εκτέλεσε":
            self.call_stat()
            return

        self.get_token()
        self.error_message("No assignment or <εάν, όσο, επανάλαβε, για, διάβασε, γράψε, εκτέλεσε> found.\nCheck for unnecessary extra ';' at end of block")

    def assignment_stat(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        # Store the target variable
        target_var = self.current_token.recognized_string

        # Make sure variable exists in symbol table
        if not self.symbol_table.lookup(target_var):
            self.error_message(f"Undeclared variable '{target_var}'")

        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.error_expected(":=")

        # Get the result of expression
        result = self.expression()

        # Generate assignment quad
        self.quad_manager.gen_quad(":=", result, "_", target_var)

    def if_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "εάν":
            self.error_expected("εάν")

        # Get condition result and true/false jump lists
        true_list, false_list = self.condition()

        self.get_token()
        if self.current_token.recognized_string != "τότε":
            self.error_expected("τότε")

        # Backpatch true list to current quad
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

        self.sequence()

        # Create jump quad for end of if statement
        jump_quad = self.quad_manager.gen_quad("jump", "_", "_", "_")
        end_if_list = self.quad_manager.make_list(jump_quad)

        # Backpatch false list to current quad
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.elsepart()

        # Backpatch end_if_list to current quad
        self.quad_manager.backpatch(end_if_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.recognized_string != "εάν_τέλος":
            self.error_expected("εάν_τέλος")

    def elsepart(self):
        if self.next_token().recognized_string == "αλλιώς":
            self.get_token()
            self.sequence()
        else:
            return

    def while_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "όσο":
            self.error_expected("όσο")

        # Store start of condition for looping back
        while_start = self.quad_manager.next_quad()

        # Get condition result and true/false jump lists
        true_list, false_list = self.condition()

        self.get_token()
        if self.current_token.recognized_string != "επανάλαβε":
            self.error_expected("επανάλαβε")

        # Backpatch true list to current quad (loop body)
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

        self.sequence()

        # Generate jump back to condition
        self.quad_manager.gen_quad("jump", "_", "_", while_start)

        # Backpatch false list to next quad (exit loop)
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.recognized_string != "όσο_τέλος":
            self.error_expected("όσο_τέλος")

    def do_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "επανάλαβε":
            self.error_expected("επανάλαβε")

        # Store start of loop body for looping back
        do_start = self.quad_manager.next_quad()

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "μέχρι":
            self.error_expected("μέχρι")

        # Get condition result and true/false jump lists
        true_list, false_list = self.condition()

        # For do-until, we need to jump back to start if the condition is FALSE
        # So we backpatch the true_list to exit the loop and false_list to loop back
        self.quad_manager.backpatch(false_list, do_start)

        # Backpatch true list to next quad (exit loop)
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

    def for_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "για":
            self.error_expected("για")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        # Store loop counter variable
        counter_var = self.current_token.recognized_string

        # Make sure variable exists in symbol table
        if not self.symbol_table.lookup(counter_var):
            self.error_message(f"Undeclared variable '{counter_var}'")

        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT)

        # Get initial value for counter
        initial_value = self.expression()

        # Generate assignment for initial value
        self.quad_manager.gen_quad(":=", initial_value, "_", counter_var)

        self.get_token()
        if self.current_token.recognized_string != "έως":
            self.error_expected("έως")

        # Get final value for counter
        final_value = self.expression()

        # Create a temporary for the final value
        final_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad(":=", final_value, "_", final_temp)

        # Store step value (default is 1)
        step_value = "1"
        self.step()

        # Check if a custom step was provided
        if hasattr(self, 'custom_step_value'):
            step_value = self.custom_step_value
            delattr(self, 'custom_step_value')

        # Store step in a temporary
        step_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad(":=", step_value, "_", step_temp)

        # Label for the start of the loop
        for_start = self.quad_manager.next_quad()

        # Generate comparison: counter <= final_value (or >= for negative step)
        cond_temp = self.symbol_table.new_temp()
        if step_value.startswith("-"):
            self.quad_manager.gen_quad(">=", counter_var, final_temp, cond_temp)
        else:
            self.quad_manager.gen_quad("<=", counter_var, final_temp, cond_temp)

        # Conditional jump out of loop if condition is false
        cond_quad = self.quad_manager.gen_quad("jumpz", cond_temp, "_", "_")
        false_list = self.quad_manager.make_list(cond_quad)

        self.get_token()
        if self.current_token.recognized_string != "επανάλαβε":
            self.error_expected("επανάλαβε")

        self.sequence()

        # Increment counter: counter := counter + step
        inc_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad("+", counter_var, step_temp, inc_temp)
        self.quad_manager.gen_quad(":=", inc_temp, "_", counter_var)

        # Jump back to condition
        self.quad_manager.gen_quad("jump", "_", "_", for_start)

        # Backpatch the false list to exit the loop
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.recognized_string != "για_τέλος":
            self.error_expected("για_τέλος")

    def step(self):
        if self.next_token().recognized_string == "με_βήμα":
            self.get_token()
            step_result = self.expression()
            self.custom_step_value = step_result
        else:
            return

    def print_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "γράψε":
            self.error_expected("γράψε")

        output_value = self.expression()

        # Generate print quad
        self.quad_manager.gen_quad("out", output_value, "_", "_")

    def input_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "διάβασε":
            self.error_expected("διάβασε")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'διάβασε' should be followed by type <IDENTIFIER>'")

        var_name = self.current_token.recognized_string

        # Make sure variable exists in symbol table
        if not self.symbol_table.lookup(var_name):
            self.error_message(f"Undeclared variable '{var_name}'")

        # Generate input quad
        self.quad_manager.gen_quad("in", var_name,"_", "_")

    def call_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "εκτέλεσε":
            self.error_expected("εκτέλεσε")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_message("'εκτέλεσε' should be followed by type <IDENTIFIER>'")

        proc_name = self.current_token.recognized_string

        # Check if the procedure exists
        proc_symbol = self.symbol_table.lookup(proc_name)
        if not proc_symbol or proc_symbol.symbol_type not in [SymbolType.PROCEDURE, SymbolType.FUNCTION]:
            self.error_message(f"Undefined procedure/function '{proc_name}'")

        # Process parameters if any
        param_list = []

        # Check if there are actual parameters
        if self.next_token().recognized_string == "(":
            self.get_token()  # consume '('

            # Parse actual parameters
            if self.next_token().recognized_string != ")":
                while True:
                    # Handle pass-by-reference parameters
                    if self.next_token().family == TokenFamily.PASSBYREFERENCE:
                        self.get_token()  # consume '%'
                        self.get_token()  # get the parameter name
                        if self.current_token.family != TokenFamily.IDENTIFIER:
                            self.error_message("Expected identifier after '%'")
                        param_list.append(("REF", self.current_token.recognized_string))
                    else:
                        # Handle pass-by-value parameters
                        param_value = self.expression()
                        param_list.append(("CV", param_value))

                    if self.next_token().recognized_string != ",":
                        break
                    self.get_token()  # consume ','

            self.get_token()  # consume ')'

        # Generate parameter passing quads
        for i, (mode, param) in enumerate(param_list):
            self.quad_manager.gen_quad("par", param, mode, str(i+1))

        # Generate call quad
        self.quad_manager.gen_quad("call", proc_name, "_", "_")

        # If it's a function, create a temporary for the result
        if proc_symbol and proc_symbol.symbol_type == SymbolType.FUNCTION:
            result_temp = self.symbol_table.new_temp()
            self.quad_manager.gen_quad("par", result_temp, "RET", "_")
            return result_temp

        # Generate the function/procedure block if it hasn't been generated yet
        if proc_name in self.function_blocks and self.function_blocks[proc_name]['end_quad'] is None:
            # Save current scope
            current_scope = self.symbol_table.current_scope

            # Enter function scope
            self.symbol_table.enter_scope(proc_name)

            # Generate the function block
            if proc_symbol.symbol_type == SymbolType.FUNCTION:
                self.funcblock()
            else:
                self.procblock()

            # Generate end block quad
            self.quad_manager.gen_quad("end_block", proc_name, "_", "_")

            # Update the end quad in the function blocks
            self.function_blocks[proc_name]['end_quad'] = self.quad_manager.next_quad()

            # Restore original scope
            self.symbol_table.enter_scope(current_scope)

    def idtail(self):
        if self.next_token().recognized_string == "(":
            return self.actualpars()
        return None

    def actualpars(self):
        self.get_token()
        if self.current_token.recognized_string != "(":
            self.error_expected("(")

        param_list = self.actualparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.error_expected(")")

        return param_list

    def actualparlist(self):
        param_list = []

        if self.next_token().recognized_string == ")":
            return param_list

        param = self.actualparitem()
        if param:
            param_list.append(param)

        while self.next_token().recognized_string == ",":
            self.get_token()
            param = self.actualparitem()
            if param:
                param_list.append(param)

        return param_list

    def actualparitem(self):
        if self.next_token().family == TokenFamily.PASSBYREFERENCE:
            self.get_token()

            self.get_token()
            if self.current_token.family != TokenFamily.IDENTIFIER:
                self.error_message("'%' should be followed by type <IDENTIFIER>'")

            return ("REF", self.current_token.recognized_string)
        else:
            expr_result = self.expression()
            return ("CV", expr_result)

    def condition(self):
        # Get boolean term result
        true_list, false_list = self.boolterm()

        # Process 'ή' (OR) operators
        while self.next_token().recognized_string == "ή":
            self.get_token()

            # Backpatch the false list of the current term to the next quad
            # This implements short-circuit evaluation
            self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

            # Get the next term's true/false lists
            next_true_list, next_false_list = self.boolterm()

            # Merge the true lists
            true_list = self.quad_manager.merge_lists(true_list, next_true_list)

            # The new false list is just the next term's false list
            false_list = next_false_list

        # Adjust jump targets for comparison quads
        for quad_index in true_list:
            if 0 < quad_index <= len(self.quad_manager.quads):
                quad_num, op, arg1, arg2, _ = self.quad_manager.quads[quad_index - 1]
                if op in {'<', '>', '<=', '>=', '=', '<>'}:
                    # For comparison operators, target is the next quad
                    self.quad_manager.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(self.quad_manager.next_quad()))

        return true_list, false_list

    def boolterm(self):
        # Get boolean factor result
        true_list, false_list = self.boolfactor()

        # Process 'και' (AND) operators
        while self.next_token().recognized_string == "και":
            self.get_token()

            # Backpatch the true list of the current factor to the next quad
            # This implements short-circuit evaluation
            self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

            # Get the next factor's true/false lists
            next_true_list, next_false_list = self.boolfactor()

            # The new true list is just the next factor's true list
            true_list = next_true_list

            # Merge the false lists
            false_list = self.quad_manager.merge_lists(false_list, next_false_list)

        return true_list, false_list

    def boolfactor(self):
        # Check for 'όχι' (NOT) operator
        not_flag = False
        if self.next_token().recognized_string == "όχι":
            self.get_token()
            not_flag = True

        # Handle parenthesized condition
        if self.next_token().recognized_string == "[":
            self.get_token()
            true_list, false_list = self.condition()
            self.get_token()
            if self.current_token.recognized_string != "]":
                self.error_expected("]")

            # If NOT is present, swap the true and false lists
            if not_flag:
                true_list, false_list = false_list, true_list

            return true_list, false_list

        # Handle relational expression
        left_expr = self.expression()
        rel_op = self.relational_oper()
        right_expr = self.expression()

        # Generate comparison quad with target being the next quad
        comp_quad = self.quad_manager.gen_quad(rel_op, left_expr, right_expr, "_")

        # Create lists for true and false cases
        if not_flag:
            # For NOT, swap the true and false lists
            false_list = self.quad_manager.make_list(comp_quad)
            true_list = self.quad_manager.make_list(self.quad_manager.next_quad())
            # Add jump to skip the false case
            self.quad_manager.gen_quad("jump", "_", "_", "_")
        else:
            true_list = self.quad_manager.make_list(comp_quad)
            false_list = self.quad_manager.make_list(self.quad_manager.next_quad())
            # Add jump to skip the true case
            self.quad_manager.gen_quad("jump", "_", "_", "_")

        return true_list, false_list

    def expression(self):
        # Handle optional sign
        sign = None
        if (self.next_token().recognized_string == "+") or (self.next_token().recognized_string == "-"):
            sign = self.add_oper()

        # Get the first term
        term_result = self.term()

        # Apply the sign if present
        if sign == "-":
            # Create a temporary for the negative value
            neg_temp = self.symbol_table.new_temp()
            self.quad_manager.gen_quad("-", "0", term_result, neg_temp)
            term_result = neg_temp

        # Process additional terms
        while (self.next_token().recognized_string == "+") or (self.next_token().recognized_string == "-"):
            op = self.add_oper()
            next_term = self.term()

            # Create a temporary for the result
            result_temp = self.symbol_table.new_temp()

            # Generate quad for the operation
            self.quad_manager.gen_quad(op, term_result, next_term, result_temp)

            # Update the current result
            term_result = result_temp

        return term_result

    def term(self):
        # Get the first factor
        factor_result = self.factor()

        # Process additional factors
        while (self.next_token().recognized_string == "*") or (self.next_token().recognized_string == "/"):
            op = self.mul_oper()
            next_factor = self.factor()

            # Create a temporary for the result
            result_temp = self.symbol_table.new_temp()

            # Generate quad for the operation
            self.quad_manager.gen_quad(op, factor_result, next_factor, result_temp)

            # Update the current result
            factor_result = result_temp

        return factor_result

    def factor(self):
        self.get_token()

        # Handle number
        if self.current_token.family == TokenFamily.NUMBER:
            return self.current_token.recognized_string

        # Handle parenthesized expression
        elif self.current_token.recognized_string == "(":
            expr_result = self.expression()

            self.get_token()
            if self.current_token.recognized_string != ")":
                self.error_expected(")")

            return expr_result

        # Handle identifier (variable or function call)
        elif self.current_token.family == TokenFamily.IDENTIFIER:
            var_name = self.current_token.recognized_string

            # Check for function call
            func_call_result = self.idtail()

            if func_call_result is not None:
                # It's a function call, return the temporary with the result
                return func_call_result
            else:
                # It's a variable reference
                # Make sure variable exists in symbol table
                if not self.symbol_table.lookup(var_name):
                    self.error_message(f"Undeclared variable '{var_name}'")
                return var_name
        else:
            self.error_expected("ID or (Expression) or NUMBER")
            return None

    def relational_oper(self):
        self.get_token()
        if self.current_token.family != TokenFamily.RELATIONAL_OPERATOR:
            self.throwTypeError(TokenFamily.RELATIONAL_OPERATOR)

        return self.current_token.recognized_string

    def add_oper(self):
        self.get_token()
        if (self.current_token.recognized_string != "+") and (self.current_token.recognized_string != "-"):
            self.error_expected("+ or -")

        return self.current_token.recognized_string

    def mul_oper(self):
        self.get_token()
        if (self.current_token.recognized_string != "*") and (self.current_token.recognized_string != "/"):
            self.error_expected("* or /")

        return self.current_token.recognized_string

    def optional_sign(self):
        if (self.next_token().recognized_string == "+") or (self.next_token().recognized_string == "-"):
            return self.add_oper()
        return None


# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Call should look like 'python compiler.py <file_name>'")
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