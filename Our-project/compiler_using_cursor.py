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
                print(f"### Lexer error at line '{line}' => Bad use of ':' operator. Received: '{invalid_token}'. Typically only '=' can follow. ###")

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

        # FTASAME SE EOF
        if not self.current_char:
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
            word = self.current_char
            next_word = self.next_char()
            if next_word == '=':
                assignment = word + next_word
                self.next_char()
                return Token(assignment, TokenFamily.ASSIGNMENT, self.current_line, self.file_name)
            self.throwLexError(INVALID_ASSIGNMENT_ERROR, self.current_line, word+next_word)
            return Token(word+next_word, TokenFamily.ERROR, self.current_line, self.file_name)  # Invalid ':'

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
        self.next_char()
        self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, error_char)
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
        self.offset = offset  # Offset mnimis
        self.parameter_mode = parameter_mode  # CV (Call by Value) alliws REF (Call by Reference)

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.current_scope = "global"
        self.offset = 0
        self.temp_counter = 0  # Metritis gia tis temporary metavlites

    # Eisodos se neo code block
    def enter_scope(self, scope_name):
        self.current_scope = scope_name
        self.offset = 0  # Epanafora tou offset

    # Eksodos apo code block
    def exit_scope(self):
        self.current_scope = "global"

    # Prosthiki symbolou ston pinaka
    def add_symbol(self, name, symbol_type, parameter_mode=None):
        key = (name, self.current_scope)

        # Elegxos an to symbolo yparxei hdh
        if key in self.symbols:
            return False

        self.symbols[key] = Symbol(name, symbol_type, self.current_scope, self.offset, parameter_mode)
        self.offset += 4  # Ypothetoume 4 bytes gia kathe metavliti
        return True

    # Anazhthsh symbolou ston pinaka
    def lookup(self, name, scope=None):
        # An den dinetai to scope, thewroume to trexon
        if scope is None:
            scope = self.current_scope

        # Elegxos an to symbolo yparxei
        key = (name, scope)
        if key in self.symbols:
            return self.symbols[key]

        # An den exei akoma vrethei, anazhthsh sto global scope
        if scope != "global":
            key = (name, "global")
            if key in self.symbols:
                return self.symbols[key]

        # An den vrethei kai sto global scope
        return None

    # Dhmiourgia neas temporary metavlitis kai epistrofi tou onomatos tis
    def new_temp(self):
        temp_name = f"t@{self.temp_counter}"  # Xrisi lowercase t@
        self.temp_counter += 1
        self.add_symbol(temp_name, SymbolType.TEMPORARY)  # Eisagogi ston pinaka symbolon
        return temp_name

    # Ektypwsi h apothikefsi twn pliroforiwn tou pinaka symbolon gia ta scopes
    def print_scope_info(self, output_file=None):
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write("Symbol Table Scope Information\n")
                f.write("=" * 50 + "\n\n")

                # Omadopoihsh symbolwn ana scope
                scopes = {}
                for (name, scope), symbol in self.symbols.items():
                    if scope not in scopes:
                        scopes[scope] = []
                    scopes[scope].append(symbol)

                # Arxika katagrafh tou global scope
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

                # Katagrafh twn allown scopes
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

            # Omadopoihsh symbolwn ana scope
            scopes = {}
            for (name, scope), symbol in self.symbols.items():
                if scope not in scopes:
                    scopes[scope] = []
                scopes[scope].append(symbol)

            # Arxika ektypwsi tou global scope
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

            # Ektypwsh twn allown scopes
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
        self.next_label = 1  # Arxh apo to 1
        self.program_name = "" 

    # Paragwgh neas tetradas kai prosthikh ths sthn lista
    def gen_quad(self, op, arg1, arg2, result):
        quad = (self.next_label, op, arg1, arg2, result)  # Xrisi tou next_label anti gia len(self.quads)
        self.quads.append(quad)
        self.next_label += 1  # Afksisi tou next_label
        return self.next_label - 1  # Epistrofi tou trexontos label

    # Epistrofi tou label tis epomenis tetradas
    def next_quad(self):
        return self.next_label

    # Gemisma tou pediou result twn tetradwn me label
    def backpatch(self, list_of_quads, label):
        for quad_index in list_of_quads:
            if 0 < quad_index <= len(self.quads):
                quad_num, op, arg1, arg2, _ = self.quads[quad_index - 1]
                if op in {'<', '>', '<=', '>=', '=', '<>'}:
                    # For comparison operators, target is the next quad
                    self.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(label + 1))
                else:
                    # For jumps, target is the label
                    self.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(label))

    # Sinenwsi listwn
    def merge_lists(self, list1, list2):
        return list1 + list2

    # Kataskevi neas listas pou periexei mono to quad_index
    def make_list(self, quad_index):
        return [quad_index]

    # Ektypwsi h apothikefsi tou paraxthein endiamesou kwdika
    def print_intermediate_code(self, output_file=None):
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"Program: {self.program_name}\n")
                f.write("-" * 50 + "\n")
                for quad_num, op, arg1, arg2, result in self.quads:
                    # Morfopoihsh
                    arg1 = arg1 if arg1 != "_" else "_"
                    arg2 = arg2 if arg2 != "_" else "_"
                    result = result if result != "_" else "_"
                    f.write(f"{quad_num} : {op} , {arg1} , {arg2} , {result}\n")
                # Prosthiki tou halt instruction prin to telos
                f.write(f"{self.next_label} : halt , _ , _ , _\n")
                # Prosthiki tou end_block instruction mono ean den uparxei hdh
                if not any(q[1] == "end_block" for q in self.quads):
                    f.write(f"{self.next_label + 1} : end_block , {self.program_name} , _ , _\n")
        else:
            print("\n-- Intermediate Code --")
            print(f"Program: {self.program_name}")
            print("-" * 50)
            for quad_num, op, arg1, arg2, result in self.quads:
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

        # Gia aksiologisi ekfrasewn
        self.place_stack = []

        # Gia elegxo rois
        self.if_list = []
        self.while_list = []
        self.for_list = []

        # Kataxwrisi twn function blocks gia na paraxthoun meta apo tin klisi
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

    def throwInvalidError(self, token):
        print(f"Syntax Error at line {token.line_number}: Got invalid phrase '{token.recognized_string}'.")
        sys.exit(1)

    def throwExpectedAnotherTokenError(self, expected):
        print(f"Syntax Error at line {self.current_token.line_number}: Expected '{expected}', but got '{self.current_token.recognized_string}'.")
        sys.exit(1)

    def throwTypeError(self, type):
        print(f"Syntax Error at line {self.current_token.line_number}: Expected type '{type}', but got type '{self.current_token.family.name}'.")
        sys.exit(1)

    def throwCustomError(self, message):
        print(f"Syntax Error at line {self.current_token.line_number}: {message}.")
        sys.exit(1)

    # Methodos analysis pou ksekinaei tin syntaktiki analysi me ti
    # methodo anadromikis katavasis
    def analyze(self):
        for token in self.tokens:
            if token.family.name == "ERROR":
                self.throwInvalidError(token)

        self.program()
        print("--No errors--")

        # Klisi ektipwsis endiamesou kwdika
        self.quad_manager.print_intermediate_code()

        # --------------------------- #
        #  Kataskevi arxeiwn eksodou  #
        # --------------------------- #

        # Pare to input filename apo to pedio file_name tou token
        input_file_path = self.tokens[0].file_name if hasattr(self.tokens[0], 'file_name') else "output"
        # Theloume mono to onoma tou arxeiou
        input_filename = os.path.basename(input_file_path)
        # Allagi kataliksis arxeiou se .int gia to arxeio eksodou tou endiamesou
        int_output_filename = input_filename.replace('.gr', '.int')

        # Apothikefsi tou arxeiou eksodou sto trexonta katalogo
        self.quad_manager.print_intermediate_code(int_output_filename)
        print(f"\nIntermediate code saved to: {int_output_filename}")

        # Apothikefsi tou arxeiou eksodou tou pinaka symbolon sto trexonta katalogo
        sym_scope_output_filename = input_filename.replace('.gr', '.sym')
        self.symbol_table.print_scope_info(sym_scope_output_filename)
        print(f"Symbol table scope information saved to: {sym_scope_output_filename}")

    # ---------------------------------------------------- #
    #  Allagmenes methodoi gia paragwgi endiamesou kwdika  #
    # ---------------------------------------------------- #

    def program(self):
        if self.current_token.recognized_string != "πρόγραμμα":
            self.throwCustomError("Program should start with 'πρόγραμμα'")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwCustomError("'πρόγραμμα' should be followed by <PROGRAM_NAME> of type <IDENTIFIER>")

        # Perasma tou program name
        self.quad_manager.program_name = self.current_token.recognized_string

        # Ekkinisi me to program
        self.quad_manager.gen_quad("begin_block", self.current_token.recognized_string, "_", "_")

        self.programblock()

        # Telos programmatos
        self.quad_manager.gen_quad("halt", "_", "_", "_")
        self.quad_manager.gen_quad("end_block", self.quad_manager.program_name, "_", "_")

    def programblock(self):
        self.declarations()
        if (self.next_token().recognized_string == "συνάρτηση") or (self.next_token().recognized_string == "διαδικασία"):
            self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_προγράμματος":
            self.throwCustomError("'αρχή_προγράμματος' not found")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_προγράμματος":
            self.throwExpectedAnotherTokenError("τέλος_προγράμματος")

    def declarations(self):
        if self.next_token().recognized_string != "δήλωση":
            return
        while self.next_token().recognized_string == "δήλωση":
            self.get_token()
            self.varlist()

    def varlist(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwCustomError("'δήλωση' should be of type: δήλωση <IDENTIFIER>, ... ,<IDENTIFIER>")

        # Prosthiki metavlitis ston pinaka symbolwn
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
            self.throwExpectedAnotherTokenError("συνάρτηση")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwCustomError("'συνάρτηση' should be followed by <FUNCTION_NAME> of type <IDENTIFIER>")

        # Prosthiki synartisis ston pinaka symbolwn kai allagi tou scope
        func_name = self.current_token.recognized_string
        self.symbol_table.add_symbol(func_name, SymbolType.FUNCTION)
        self.symbol_table.enter_scope(func_name)

        # Kataxwrisi tis thesis tis trexousas tetradas gia afti tin synartisi
        start_quad = self.quad_manager.next_quad()

        # Paragwgh tis tetradas begin_block gia tin sinartisi
        self.quad_manager.gen_quad("begin_block", func_name, "_", "_")

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwExpectedAnotherTokenError("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwExpectedAnotherTokenError(")")

        # Kataxwrisi tou block tis sinartisis anti na to paragoume apeftheias
        self.function_blocks[func_name] = {
            'start_quad': start_quad,
            'end_quad': None,  # Tha allaksei molis paraxthei to end block
            'scope': func_name
        }

        self.funcblock()

        # Epistrofi sto global scope
        self.symbol_table.exit_scope()

    def proc(self):
        self.get_token()
        if self.current_token.recognized_string != "διαδικασία":
            self.throwExpectedAnotherTokenError("διαδικασία")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwCustomError("'διαδικασία' should be followed by <PROCESS_NAME> of type <IDENTIFIER>")

        # Prosthiki diadikasias ston pinaka symvolwn kai allagi tou scope
        proc_name = self.current_token.recognized_string
        self.symbol_table.add_symbol(proc_name, SymbolType.PROCEDURE)
        self.symbol_table.enter_scope(proc_name)

        # Kataxwrisi tis thesis tis trexousas tetradas gia afti ti diadikasia
        start_quad = self.quad_manager.next_quad()

        # Paragwgh tis tetradas begin_block gia ti diadikasia
        self.quad_manager.gen_quad("begin_block", proc_name, "_", "_")

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwExpectedAnotherTokenError("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwExpectedAnotherTokenError(")")

        # Kataxwrisi tou block tis diadikasias anti na to paragoume apeftheias
        self.function_blocks[proc_name] = {
            'start_quad': start_quad,
            'end_quad': None,  # Tha allaksei molis paraxthei to end block
            'scope': proc_name
        }

        self.procblock()

        # Epistrofi sto global scope
        self.symbol_table.exit_scope()

    def formalparlist(self):
        if self.next_token().recognized_string == ")":
            return
        self.varlist()

    def funcblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.throwExpectedAnotherTokenError("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_συνάρτησης":
            self.throwExpectedAnotherTokenError("αρχή_συνάρτησης")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_συνάρτησης":
            self.throwExpectedAnotherTokenError("τέλος_συνάρτησης")

    def procblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.throwExpectedAnotherTokenError("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            self.throwExpectedAnotherTokenError("αρχή_διαδικασίας")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            self.throwExpectedAnotherTokenError("τέλος_διαδικασίας")

    def funcinput(self):
        if self.next_token().recognized_string == "είσοδος":
            self.get_token()
            self.varlist()

    def funcoutput(self):
        if self.next_token().recognized_string == "έξοδος":
            self.get_token()
            self.varlist()

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
        self.throwCustomError("No assignment or <εάν, όσο, επανάλαβε, για, διάβασε, γράψε, εκτέλεσε> found. Check for unnecessary extra ';' at end of block")

    def assignment_stat(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER.name)

        # Krataw to onoma tis metavlitis ekxwrhshs
        target_var = self.current_token.recognized_string

        # Elegxos an h metavliti ekxwrhshs uparxei ston pinaka symbolwn
        # An den yparxei, tote shmainei oti den exei dhlwthei kai petame error
        if not self.symbol_table.lookup(target_var):
            self.throwCustomError(f"Undeclared variable '{target_var}'")

        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwExpectedAnotherTokenError(":=")

        # Krataw to apotelesma tis ekfrasis
        result = self.expression()

        # Paragwgh tetradas
        self.quad_manager.gen_quad(":=", result, "_", target_var)

    def if_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "εάν":
            self.throwExpectedAnotherTokenError("εάν")

        # Krataw apotelesmata sinthikwn kai true/false jump listes
        true_list, false_list = self.condition()

        self.get_token()
        if self.current_token.recognized_string != "τότε":
            self.throwExpectedAnotherTokenError("τότε")

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
        if self.current_token.recognized_string != "εάν_τέλος":
            self.throwExpectedAnotherTokenError("εάν_τέλος")

    def elsepart(self):
        if self.next_token().recognized_string == "αλλιώς":
            self.get_token()
            self.sequence()

    def while_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "όσο":
            self.throwExpectedAnotherTokenError("όσο")

        # Krataw arxi sinthikwn gia na epistrepsei stin epanalipsi
        while_start = self.quad_manager.next_quad()

        # Krataw apotelesmata sinthikwn kai true/false jump listes
        true_list, false_list = self.condition()

        self.get_token()
        if self.current_token.recognized_string != "επανάλαβε":
            self.throwExpectedAnotherTokenError("επανάλαβε")

        # Ektelw backpatch tis true list stin trexousa tetrada (loop body)
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

        self.sequence()

        # Paragwgh jump tetradas gia na epistrepsei stin sinthiki
        self.quad_manager.gen_quad("jump", "_", "_", while_start)

        # Ektelw backpatch tis false list stin epomeni tetrada (exit loop)
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.recognized_string != "όσο_τέλος":
            self.throwExpectedAnotherTokenError("όσο_τέλος")

    def do_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "επανάλαβε":
            self.throwExpectedAnotherTokenError("επανάλαβε")

        # Krataw arxi loop body gia na epistrepsei stin epanalipsi
        do_start = self.quad_manager.next_quad()

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "μέχρι":
            self.throwExpectedAnotherTokenError("μέχρι")

        # Krataw apotelesmata sinthikwn kai true/false jump listes
        true_list, false_list = self.condition()

        # Sto do-until prepei na kanoume jump back stin arxi an h synthiki apotimatai se FALSE
        # Ektelw backpatch tis false list stin arxi
        self.quad_manager.backpatch(false_list, do_start)

        # Ektelw backpatch tis true list stin eksodo (exit loop)
        self.quad_manager.backpatch(true_list, self.quad_manager.next_quad())

    def for_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "για":
            self.throwExpectedAnotherTokenError("για")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER.name)

        # Krataw to onoma tis metavlitis tou metriti tou for-loop
        counter_var = self.current_token.recognized_string

        # Elegxos an h metavliti uparxei ston pinaka symbolwn
        if not self.symbol_table.lookup(counter_var):
            self.throwCustomError(f"Undeclared variable '{counter_var}'")

        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT.name)

        # Krataw arxikh timh tou metriti
        initial_value = self.expression()

        # Paragwgh tetradas ekxwrhshs gia arxikh timh tou metriti
        self.quad_manager.gen_quad(":=", initial_value, "_", counter_var)

        self.get_token()
        if self.current_token.recognized_string != "έως":
            self.throwExpectedAnotherTokenError("έως")

        # Krataw teliki timh tou metriti
        final_value = self.expression()

        # Dimiourgia enos temp var gia thn teliki timh
        final_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad(":=", final_value, "_", final_temp)

        # Krataw timh step (default timh einai 1)
        step_value = "1"
        self.step()

        # Elegxos an exei dwthei custom step
        if hasattr(self, 'custom_step_value'):
            step_value = self.custom_step_value
            delattr(self, 'custom_step_value')

        # Krataw timh step sto temp var
        step_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad(":=", step_value, "_", step_temp)

        # Label gia tin arxi tou for-loop
        for_start = self.quad_manager.next_quad()

        # Paragwgi sygkrisis: counter <= final_value (or >= for negative step)
        cond_temp = self.symbol_table.new_temp()
        if step_value.startswith("-"):
            self.quad_manager.gen_quad(">=", counter_var, final_temp, cond_temp)
        else:
            self.quad_manager.gen_quad("<=", counter_var, final_temp, cond_temp)

        # Conditional jump out of loop if condition is false (jumpz)
        cond_quad = self.quad_manager.gen_quad("jumpz", cond_temp, "_", "_")
        false_list = self.quad_manager.make_list(cond_quad)

        self.get_token()
        if self.current_token.recognized_string != "επανάλαβε":
            self.throwExpectedAnotherTokenError("επανάλαβε")

        self.sequence()

        # Afksish tou metriti: counter := counter + step
        inc_temp = self.symbol_table.new_temp()
        self.quad_manager.gen_quad("+", counter_var, step_temp, inc_temp)
        self.quad_manager.gen_quad(":=", inc_temp, "_", counter_var)

        # Epistrofi sti sinthiki
        self.quad_manager.gen_quad("jump", "_", "_", for_start)

        # Ektelw backpatch tou false list gia na vgei apo to loop
        self.quad_manager.backpatch(false_list, self.quad_manager.next_quad())

        self.get_token()
        if self.current_token.recognized_string != "για_τέλος":
            self.throwExpectedAnotherTokenError("για_τέλος")

    def step(self):
        if self.next_token().recognized_string == "με_βήμα":
            self.get_token()
            step_result = self.expression()
            self.custom_step_value = step_result

    def print_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "γράψε":
            self.throwExpectedAnotherTokenError("γράψε")

        output_value = self.expression()

        # Paragwgh tetradas ektypwshs
        self.quad_manager.gen_quad("out", output_value, "_", "_")

    def input_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "διάβασε":
            self.throwExpectedAnotherTokenError("διάβασε")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwCustomError("'διάβασε' should be followed by type <IDENTIFIER>'")

        var_name = self.current_token.recognized_string

        # Elegxos an h metavliti uparxei ston pinaka symbolwn
        if not self.symbol_table.lookup(var_name):
            self.throwCustomError(f"Undeclared variable '{var_name}'")

        # Paragwgh tetradas eisodou
        self.quad_manager.gen_quad("in", var_name,"_", "_")

    def call_stat(self):
        self.get_token()
        if self.current_token.recognized_string != "εκτέλεσε":
            self.throwExpectedAnotherTokenError("εκτέλεσε")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwCustomError("'εκτέλεσε' should be followed by type <IDENTIFIER>'")

        proc_name = self.current_token.recognized_string

        # Elegxos an h diadikasia uparxei ston pinaka symbolwn
        proc_symbol = self.symbol_table.lookup(proc_name)
        if not proc_symbol or proc_symbol.symbol_type not in [SymbolType.PROCEDURE, SymbolType.FUNCTION]:
            self.throwCustomError(f"Undefined procedure/function '{proc_name}'")

        # Lista parametrwn
        param_list = []

        # Elegxos an yparxoun parametroi
        if self.next_token().recognized_string == "(":
            self.get_token() # katanalwsh '('

            # Analisi parametrwn
            if self.next_token().recognized_string != ")":
                while True:
                    # Xeirismos parametrwn me anafora
                    if self.next_token().family == TokenFamily.PASSBYREFERENCE:
                        self.get_token()  # katanalwsh '%'
                        self.get_token()  # lipsi onomatos parametrou
                        if self.current_token.family != TokenFamily.IDENTIFIER:
                            self.throwCustomError("Expected identifier after '%'")
                        param_list.append(("REF", self.current_token.recognized_string))
                    else:
                        # Xeirismos parametrwn me timh
                        param_value = self.expression()
                        param_list.append(("CV", param_value))

                    if self.next_token().recognized_string != ",":
                        break
                    self.get_token()  # katanalwsh ','

            self.get_token() # katanalwsh ')'

        # Paragwgi tetradwn parametrwn
        for i, (mode, param) in enumerate(param_list):
            self.quad_manager.gen_quad("par", param, mode, str(i+1))

        # Paragwgh tetradas klhshs
        self.quad_manager.gen_quad("call", proc_name, "_", "_")

        # Ean einai synartisi dimiourgia temp gia to apotelesma
        if proc_symbol and proc_symbol.symbol_type == SymbolType.FUNCTION:
            result_temp = self.symbol_table.new_temp()
            self.quad_manager.gen_quad("par", result_temp, "RET", "_")
            return result_temp

        # Dhmiourgia tou function/proc block an den exei ginei hdh
        if proc_name in self.function_blocks and self.function_blocks[proc_name]['end_quad'] is None:
            # Krataw to trexon scope
            current_scope = self.symbol_table.current_scope

            # Eisodos sto scope tis sinartisis
            self.symbol_table.enter_scope(proc_name)

            # Dhmiourgia block sinartisis
            if proc_symbol.symbol_type == SymbolType.FUNCTION:
                self.funcblock()
            else:
                self.procblock()

            # Paragwgh tetradas end block
            self.quad_manager.gen_quad("end_block", proc_name, "_", "_")

            # Ananewsi tis end tetradas sta function blocks
            self.function_blocks[proc_name]['end_quad'] = self.quad_manager.next_quad()

            # Epistrofi sto trexon scope
            self.symbol_table.enter_scope(current_scope)

    def idtail(self):
        if self.next_token().recognized_string == "(":
            return self.actualpars()
        return None

    def actualpars(self):
        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwExpectedAnotherTokenError("(")

        param_list = self.actualparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwExpectedAnotherTokenError(")")

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
                self.throwCustomError("'%' should be followed by type <IDENTIFIER>'")

            return ("REF", self.current_token.recognized_string)
        else:
            expr_result = self.expression()
            return ("CV", expr_result)

    def condition(self):
        # Krataw boolterm apotelesma kai true/false jump listes
        true_list, false_list = self.boolterm()

        # Epeksergasia OR operator
        while self.next_token().recognized_string == "ή":
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
        while self.next_token().recognized_string == "και":
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
        if self.next_token().recognized_string == "όχι":
            self.get_token()
            not_flag = True

        # Xeirismos sinthikis se parenthesi
        if self.next_token().recognized_string == "[":
            self.get_token()
            true_list, false_list = self.condition()
            self.get_token()
            if self.current_token.recognized_string != "]":
                self.throwExpectedAnotherTokenError("]")

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
        if (self.next_token().recognized_string == "+") or (self.next_token().recognized_string == "-"):
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
        while (self.next_token().recognized_string == "+") or (self.next_token().recognized_string == "-"):
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
        while (self.next_token().recognized_string == "*") or (self.next_token().recognized_string == "/"):
            op = self.mul_oper()
            next_factor = self.factor()

            # Dhmiourgia temp gia to apotelesma
            result_temp = self.symbol_table.new_temp()

            # Dhmiourgia tetradas
            self.quad_manager.gen_quad(op, factor_result, next_factor, result_temp)

            # Ananewsi tou trexontos apotelesmatos
            factor_result = result_temp

        return factor_result

    def factor(self):
        self.get_token()

        # Xeirismos arithmou
        if self.current_token.family == TokenFamily.NUMBER:
            return self.current_token.recognized_string

        # Xeirismos ekfrasis se parenthesi
        elif self.current_token.recognized_string == "(":
            expr_result = self.expression()

            self.get_token()
            if self.current_token.recognized_string != ")":
                self.throwExpectedAnotherTokenError(")")

            return expr_result

        # Xeirismos identifier (metavliti h klisi sinartisis)
        elif self.current_token.family == TokenFamily.IDENTIFIER:
            var_name = self.current_token.recognized_string

            # Elegxos gia klisi sinartisis
            func_call_result = self.idtail()

            if func_call_result is not None:
                # Einai klisi sinartisis epistrofi tou temp me to apotelesma
                return func_call_result
            else:
                # Einai metavliti, elegxos an yparxei ston pinaka symbolwn
                if not self.symbol_table.lookup(var_name):
                    self.throwCustomError(f"Undeclared variable '{var_name}'")
                return var_name
        else:
            self.throwExpectedAnotherTokenError("ID or (Expression) or NUMBER")
            return None

    def relational_oper(self):
        self.get_token()
        if self.current_token.family != TokenFamily.RELATIONAL_OPERATOR:
            self.throwTypeError(TokenFamily.RELATIONAL_OPERATOR.name)

        return self.current_token.recognized_string

    def add_oper(self):
        self.get_token()
        if (self.current_token.recognized_string != "+") and (self.current_token.recognized_string != "-"):
            self.throwExpectedAnotherTokenError("+ or -")

        return self.current_token.recognized_string

    def mul_oper(self):
        self.get_token()
        if (self.current_token.recognized_string != "*") and (self.current_token.recognized_string != "/"):
            self.throwExpectedAnotherTokenError("* or /")

        return self.current_token.recognized_string

    def optional_sign(self):
        if (self.next_token().recognized_string == "+") or (self.next_token().recognized_string == "-"):
            return self.add_oper()
        return None


# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Usage: 'python compiler_using_cursor.py <file_name>'")
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