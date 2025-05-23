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
    NUMBER = 0  # ksekinaem enumaration apo to miden
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

#oi xaraktires pou uposthrizei h greek++
ALLOWED_CHARS = "αβγδεζηθικλμνξοπρσςτυφχψωΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩάέήίόύώΐΰϊϋabcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_0123456789"

#keywords 
KEYWORDS = {
    "πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος",
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "έως", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία",
    "είσοδος", "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας",
    "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", "και", "όχι",
    "εκτέλεσε"
}


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
ACCEPTED_NUMBER_RANGE = [-32768, 32767]

# ERRORS
INVALID_TOKEN_ERROR = 'InvalidTokenError'
INVALID_ASSIGNMENT_ERROR = 'InvalidAssignmentError'

# ---------------- KLASEIS ---------------- #

#####################
# LEKTIKOS ANALYTIS #
#####################

# KLASI TOKEN
class Token:
    def __init__(self, string, type, line_number, file_name=None):
        self.string = string
        self.type = type
        self.line_number = line_number
        self.file_name = file_name

    def __str__(self):
        return f'{self.string}\ttype:"{self.type.name}",\tline: {self.line_number}'

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
            print(f"Beginning lexical analysis...\n")
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
            if self.current_char and (self.current_char in ALLOWED_CHARS): #.isalpha() or self.current_char == '_'):
                word += self.current_char
                self.next_char()
                while self.current_char and (self.current_char in ALLOWED_CHARS): #.isalnum() or self.current_char == '_'):
                    word += self.current_char
                    self.next_char()
                self.throwLexError(INVALID_TOKEN_ERROR, self.current_line, word)
                return Token(word, TokenFamily.ERROR, self.current_line, self.file_name)
            return Token(word, TokenFamily.NUMBER, self.current_line, self.file_name)

        # IDENTIFIERS KAI KEYWORDS
        if self.current_char in ALLOWED_CHARS and self.current_char != '_': # Prevent identifiers from starting with underscore
            word = self.current_char
            self.next_char()
            while self.current_char and (self.current_char in ALLOWED_CHARS): #.isalnum() or self.current_char == '_'):
                word += self.current_char
                self.next_char()
                if(len(word) >= MAX_WORD_SIZE):
                    break
            token_type = TokenFamily.KEYWORD if word in KEYWORDS else TokenFamily.IDENTIFIER
            return Token(word, token_type, self.current_line, self.file_name)

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

            if token.type == TokenFamily.EOF:
                print("-- Reached EOF --")
                break

            tokens.append(token) # DEN THELOUME TO EOF
            print(token)

        self.file.close()
        return tokens


####################
# PINAKAS SYMBOLWN #
####################

class SymbolType(Enum):
    VARIABLE = 0
    FUNCTION = auto()
    PROCEDURE = auto()
    PARAMETER = auto()
    TEMPORARY = auto()

class Symbol:
    def __init__(self, name, symbol_type, scope="global", offset=0, parameter_mode=None):
        self.name = name                      # Onoma tou symbolou
        self.symbol_type = symbol_type        #  (metavliti, synartisi, diadikasia,  temp)
        self.scope = scope                    # Emveleia  (global or onoma synartisis/diadikasias)
        self.offset = offset                  # Thesi tou symbolou sto activation record
        self.parameter_mode = parameter_mode   # cv or ref
        self.parameters = []                  # Lista parametrwn (gia synartiseis/diadikasies)
        self.nesting_level = 0                # nesting level
        self.entry_label = 0                  # entry label
        self.frame_length = 0                 # frame length

class SymbolTable:
    def __init__(self):
        self.symbols = {}
        self.scope_stack = ["global"]
        self.scope_offsets = {"global": 12}  # ksekinaei apo 12 bytes
        self.temp_counter = 0
        self.scope_nesting = {"global": 0}
        self.activation_records = {
            "global": {
                'parent': None,
                'frame_length': 12,
                'parameters': [],
                'local_vars': [],
                'temp_vars': []
            }
        }

    def enter_scope(self, scope_name):
        parent_scope = self.current_scope
        self.scope_stack.append(scope_name)
        parent_nesting = self.scope_nesting.get(parent_scope, 0)
        self.scope_nesting[scope_name] = parent_nesting + 1
        self.scope_offsets[scope_name] = 12
        
        # create activation record for this scope
        self.activation_records[scope_name] = {
            'parent': parent_scope,
            'frame_length': 12,
            'parameters': [],
            'local_vars': [],
            'temp_vars': []
        }

    def exit_scope(self):
        if len(self.scope_stack) > 1:
            return self.scope_stack.pop()
        return "global"

    
    def current_scope(self):
        return self.scope_stack[-1]

    
    def current_nesting_level(self):
        return self.scope_nesting.get(self.current_scope, 0)

    def add_symbol(self, name, symbol_type, parameter_mode=None):
        current_scope = self.current_scope()
        key = (name, current_scope)

        
        if key in self.symbols:
            return False

        current_offset = self.scope_offsets.get(current_scope, 12)
        symbol = Symbol(name, symbol_type, current_scope, current_offset, parameter_mode)
        symbol.nesting_level = self.current_nesting_level()
        
        self.symbols[key] = symbol
        self.scope_offsets[current_scope] = current_offset + 4  # kathe symbol  4 bytes
        
        #enimerosi activation record
        if current_scope in self.activation_records:
            ar = self.activation_records[current_scope]
            ar['frame_length'] += 4
            
            
            if symbol_type == SymbolType.PARAMETER:
                ar['parameters'].append(name)
            elif symbol_type == SymbolType.TEMPORARY:
                ar['temp_vars'].append(name)
            elif symbol_type == SymbolType.VARIABLE:
                ar['local_vars'].append(name)
        
        if symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
            symbol.frame_length = 12  
        
        return True

    def add_parameter(self, func_name, param_name, param_mode="CV"):
        func_symbol = self.lookup_in_all_scopes(func_name)
        if func_symbol and func_symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
            func_symbol.parameters.append((param_name, param_mode))
            return True
        return False

    def lookup_in_all_scopes(self, name):
       
        for (sym_name, sym_scope), symbol in self.symbols.items():
            if sym_name == name:
                return symbol
        return None

    def lookup(self, name, scope=None):
        if scope is not None:
            key = (name, scope)
            return self.symbols.get(key)
        
        # psakse pano apo to current scope
        for scope_name in reversed(self.scope_stack):
            key = (name, scope_name)
            if key in self.symbols:
                return self.symbols[key]
        return None

    def lookup_with_nesting(self, name):
        current_nesting = self.current_nesting_level()
        symbol = self.lookup(name)
        if symbol:
            return symbol
            
        # psakse pano apo to current scope
        for (sym_name, sym_scope), symbol in self.symbols.items():
            if (sym_name == name and 
                self.scope_nesting.get(sym_scope, 0) < current_nesting):
                return symbol
        return None

    def new_temp(self):
        temp_name = f"T@{self.temp_counter}"  
        self.temp_counter += 1
        self.add_symbol(temp_name, SymbolType.TEMPORARY)
        return temp_name

    def get_frame_length(self, scope_name=None):
        if scope_name is None:
            scope_name = self.current_scope()
        if scope_name in self.activation_records:
            return self.activation_records[scope_name]['frame_length']
        return 12  # default  12 bytes

    def get_activation_record(self, scope_name=None):
        if scope_name is None:
            scope_name = self.current_scope()
        return self.activation_records.get(scope_name, {})

    def finalize_scope(self, scope_name=None):
        if scope_name is None:
            scope_name = self.current_scope()
            
        func_symbol = self.lookup_in_all_scopes(scope_name)
        if func_symbol and func_symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
            func_symbol.frame_length = self.get_frame_length(scope_name)

    def print_scope_info(self, output_file=None):
        def write_output(content):
            if output_file:
                output_file.write(content)
            else:
                print(content, end='')

        if output_file:
            output_file = open(output_file, 'w', encoding='utf-8')

        write_output("Symbol Table \n")
        write_output("=" * 50 + "\n\n")


        scopes = {}
        for (name, scope), symbol in self.symbols.items():
            if scope not in scopes:
                scopes[scope] = []
            scopes[scope].append(symbol)

        def print_scope_details(scope_name, symbols):
            write_output(f"\n{scope_name.title()} Scope:\n")
            write_output("-" * 20 + "\n")
            ar_info = self.activation_records.get(scope_name, {})
            write_output(f"Frame Length: {ar_info.get('frame_length', 12)}\n")
            write_output(f"Nesting Level: {self.scope_nesting.get(scope_name, 0)}\n")
            if scope_name != "global":
                write_output(f"Parent Scope: {ar_info.get('parent', 'N/A')}\n")
            write_output("\n")
            
            for symbol in symbols:
                write_output(f"Name: {symbol.name}\n")
                write_output(f"Type: {symbol.symbol_type.name}\n")
                write_output(f"Offset: {symbol.offset}\n")
                if symbol.parameter_mode:
                    write_output(f"Parameter Mode: {symbol.parameter_mode}\n")
                if symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
                    write_output(f"Parameters: {symbol.parameters}\n")
                    write_output(f"Frame Length: {symbol.frame_length}\n")
                    write_output(f"Entry Label: {symbol.entry_label}\n")
                write_output("\n")

        # print global scope first
        if "global" in scopes:
            print_scope_details("global", scopes["global"])
            del scopes["global"]

        # print remaining scopes
        for scope, symbols in scopes.items():
            print_scope_details(scope, symbols)

        if output_file and hasattr(output_file, 'close'):
            output_file.close()

#########################
# DIAXEIRISTIS TETRADWN # 
#########################

class QuadManager:
    def __init__(self):
        self.quads = []
        self.next_label = 1  
        self.program_name = "" 
        self.temp_counter = 0

    def gen_quad(self, op, arg1, arg2, result):
        #generate tetrada
        quad = (self.next_label, op, arg1, arg2, result)
        self.quads.append(quad)
        self.next_label += 1
        return self.next_label - 1  

    def next_quad(self):
        #epistrofi etiketas tis epomenis tetradas
        return self.next_label

    def backpatch(self, list_of_quads, label):
        
        for quad_index in list_of_quads:
            if 0 < quad_index <= len(self.quads):
                quad_num, op, arg1, arg2, _ = self.quads[quad_index - 1]
                self.quads[quad_index - 1] = (quad_num, op, arg1, arg2, str(label))

    def merge_lists(self, list1, list2):
       
        return list1 + list2

    def make_list(self, quad_index):
        
        return [quad_index]

    def print_intermediate_code(self, output_file=None):
       
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                for quad_num, op, arg1, arg2, result in self.quads:
                    # format arguments
                    arg1 = arg1 if arg1 != "_" else "_"
                    arg2 = arg2 if arg2 != "_" else "_"
                    result = result if result != "_" else "_"
                    f.write(f"{quad_num} : {op} , {arg1} , {arg2} , {result}\n")
                
                # add halt if not present
                if not any(q[1] == "halt" for q in self.quads):
                    f.write(f"{self.next_label} : halt , _ , _ , _\n")
                # add end_block if not present
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

#########################
# RISC-V CODE GENERATOR # 
#########################

class RISCVGenerator:
    def __init__(self, quad_manager, symbol_table):
        self.quad_manager = quad_manager
        self.symbol_table = symbol_table
        self.assembly_file = None
        self.current_scope = "global"
        self.param_counter = -1  
        self.scope_stack = ["global"]  
        self.current_called_function = None  
        self.call_setups = {}

    def open_file(self, filename):
        
        self.assembly_file = open(filename, 'w', encoding='utf-8')
        
    def close_file(self):
        self.assembly_file.close()

    def generate_code(self, output_file):
        
        self.open_file(output_file)
        
        
        
        self.assembly_file.write('  # Initialize \n')
        self.assembly_file.write('  mv fp, sp\n\n')
        
        # write initial jump to main program
        main_entry_label = None
        for i, quad in enumerate(self.quad_manager.quads):
            if quad[1] == "begin_block" and quad[2] == self.quad_manager.program_name:
                main_entry_label = quad[0]
                break
        
        if main_entry_label:
            self.assembly_file.write(f'# jump stin main  \n')
            self.assembly_file.write(f'j L{main_entry_label}\n\n')
        
        
        for quad in self.quad_manager.quads:
            quad_num, op, arg1, arg2, result = quad
            
            
            self.assembly_file.write(f'L{quad_num}: \n')
            
            
            if op == "jump":
                self.assembly_file.write(f'  b L{result}\n')
            elif op in ["=", "<>", "<", ">", "<=", ">="]:
                self.create_comparison(op, arg1, arg2, result)
            elif op == ":=":
                self.create_assignment(arg1, result)
            elif op in ["+", "-", "*", "/"]:
                self.create_arithmetic(op, arg1, arg2, result)
            elif op == "out":
                self.create_output(arg1)
            elif op == "in":
                self.create_input(arg1)
            elif op == "par":
                self.create_parameter(arg1, arg2)
            elif op == "call":
                self.create_call(arg1)
            elif op == "begin_block":
                self.create_begin_block(arg1)
            elif op == "end_block":
                self.create_end_block(arg1)
            elif op == "halt":
                self.create_halt()
            else:
                self.assembly_file.write(f'  # Unhandled operation: {op}\n')
        
      
        
        
        self.close_file()
        
  

    def load_value(self, value, register):
        
        if value.isdigit() or (value[0] == '-' and value[1:].isdigit()):
            # arithmos
            self.assembly_file.write(f'  li t{register}, {value}\n')
        elif value.startswith("T@"):
            # gia temp
            self.assembly_file.write(f'  lw t{register}, -{int(value[2:])*4+40}(gp)\n')
        else:
            
            symbol = self.symbol_table.lookup(value, self.current_scope)
            if not symbol:
                
                symbol = self.symbol_table.lookup(value)
            if not symbol:
               
                symbol = self.symbol_table.lookup_with_nesting(value)
                if not symbol:
                    func_symbol = self.symbol_table.lookup_in_all_scopes(self.current_scope)
                    if func_symbol and func_symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
                        for i, (param_name, param_mode) in enumerate(func_symbol.parameters):
                            if param_name == value:
                                if param_mode == "CV":  
                                    self.assembly_file.write(f'  # fortosi {value} me timi\n')
                                    self.assembly_file.write(f'  lw t{register}, -{12+4*i}(sp)\n')
                                    return
                                elif param_mode == "REF":  
                                    self.assembly_file.write(f'  # fortosi {value} me anafora\n')
                                    self.load_value_reference(f"-{12+4*i}", register)
                                    return
                    
                    
                    return
            
            if symbol.scope == "global":
                
                self.assembly_file.write(f'  lw t{register}, -{symbol.offset}(gp)\n')
            elif symbol.scope == self.current_scope:
               
                if symbol.symbol_type == SymbolType.PARAMETER:
                   
                    if symbol.parameter_mode == "CV":  
                        self.assembly_file.write(f'  lw t{register}, -{symbol.offset}(sp)\n')
                    elif symbol.parameter_mode == "REF":  
                        self.assembly_file.write(f'  # Loading parameter {value} in current scope by reference\n')
                        self.load_value_reference(f"-{symbol.offset}", register)
                    else:
                        self.assembly_file.write(f'  lw t{register}, -{symbol.offset}(sp)\n')
                else:
                   
                    self.assembly_file.write(f'  lw t{register}, -{symbol.offset}(sp)\n')
            elif symbol.parameter_mode == "CV":  
                self.assembly_file.write(f'  lw t{register}, -{symbol.offset}(sp)\n')
            elif symbol.parameter_mode == "REF": 
                
                self.load_value_reference(f"-{symbol.offset}", register)
            else:
                
                self.gnlvcode(value, register)

    def store_value(self, register, target):
        
        
        if target.startswith("T@"):
            self.assembly_file.write(f'  sw t{register}, -{int(target[2:])*4+40}(gp)\n')
            return
            
        symbol = self.symbol_table.lookup(target)
        if not symbol:
            
            symbol = self.symbol_table.lookup_with_nesting(target)
            if not symbol:
                
                func_symbol = self.symbol_table.lookup_in_all_scopes(self.current_scope)
                if func_symbol and func_symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]:
                    for i, (param_name, param_mode) in enumerate(func_symbol.parameters):
                        if param_name == target:
                            if param_mode == "CV":  
                                self.assembly_file.write(f'  sw t{register}, -{12+4*i}(sp)\n')
                                return
                            elif param_mode == "REF":  
                                
                                self.store_value_reference(register, f"-{12+4*i}")
                                return
                
                self.assembly_file.write(f'  # Warning: Symbol {target} not found in symbol table (current scope: {self.current_scope})\n')
                return
                
        if symbol.scope == "global":
            
            self.assembly_file.write(f'  sw t{register}, -{symbol.offset}(gp)\n')
        elif symbol.scope == self.current_scope:
            
            if symbol.symbol_type == SymbolType.PARAMETER:
                
                if symbol.parameter_mode == "CV":  
                    self.assembly_file.write(f'  sw t{register}, -{symbol.offset}(sp)\n')
                elif symbol.parameter_mode == "REF":  
                    
                    self.store_value_reference(register, f"-{symbol.offset}")
                else:
                    self.assembly_file.write(f'  sw t{register}, -{symbol.offset}(sp)\n')
            else:
                
                self.assembly_file.write(f'  sw t{register}, -{symbol.offset}(sp)\n')
        elif symbol.parameter_mode == "CV":  
            self.assembly_file.write(f'  sw t{register}, -{symbol.offset}(sp)\n')
        elif symbol.parameter_mode == "REF":  
            
            self.store_value_reference(register, f"-{symbol.offset}")
        else:
            
            self.gnlvcode(target, 0)
            self.assembly_file.write(f'  sw t{register}, 0(t0)\n')

    def gnlvcode(self, name, register):
        
        symbol = self.symbol_table.lookup_with_nesting(name)
        if not symbol:
            self.assembly_file.write(f'  # Warning: Symbol {name} not found in symbol table\n')
            return
            
        
        self.assembly_file.write(f'  lw t0, -4(sp)\n')  
        
        
        current_level = self.symbol_table.current_nesting_level()
        target_level = symbol.nesting_level
        
       
        level_diff = current_level - target_level - 1
        for i in range(level_diff):
            self.assembly_file.write(f'  lw t0, -4(t0)\n')
        
        
        if register != 0:  
            self.assembly_file.write(f'  lw t{register}, -{symbol.offset}(t0)\n')
        else: 
            self.assembly_file.write(f'  addi t0, t0, -{symbol.offset}\n')

    def create_comparison(self, op, arg1, arg2, result):
       
        self.load_value(arg1, 1)
        self.load_value(arg2, 2)
        
        if op == "=":
            self.assembly_file.write(f'  beq t1, t2, L{result}\n')
        elif op == "<>":
            self.assembly_file.write(f'  bne t1, t2, L{result}\n')
        elif op == "<":
            self.assembly_file.write(f'  blt t1, t2, L{result}\n')
        elif op == ">":
            self.assembly_file.write(f'  bgt t1, t2, L{result}\n')
        elif op == "<=":
            self.assembly_file.write(f'  ble t1, t2, L{result}\n')
        elif op == ">=":
            self.assembly_file.write(f'  bge t1, t2, L{result}\n')

    def create_assignment(self, source, target):
        
        self.load_value(source, 1)
        
        
        if target == "@RET":
            
            self.assembly_file.write('  lw t0, -8(sp)\n')  # Load address of return value
            self.assembly_file.write('  sw t1, 0(t0)\n')   # Store the value at that address
        else:
            
            func_symbol = self.symbol_table.lookup_in_all_scopes(self.current_scope)
            if (func_symbol and 
                func_symbol.symbol_type == SymbolType.FUNCTION and 
                target == self.current_scope):
                
                self.assembly_file.write('  lw t0, -8(sp)\n')  # Load address of return value
                self.assembly_file.write('  sw t1, 0(t0)\n')   # Store the value at that address
            elif (func_symbol and 
                  func_symbol.symbol_type in [SymbolType.FUNCTION, SymbolType.PROCEDURE]):
                # Check if target is a parameter
                for i, (param_name, param_mode) in enumerate(func_symbol.parameters):
                    if param_name == target:
                        if param_mode == "REF":
                            # Parameter is passed by reference
                            self.assembly_file.write(f'  # Parameter {target} passed by reference\n')
                            self.store_value_reference(1, f"-{12+4*i}")
                            return
                self.store_value(1, target)
            else:
                self.store_value(1, target)

    def create_arithmetic(self, op, arg1, arg2, result):
        
        self.load_value(arg1, 1)
        self.load_value(arg2, 2)
        
        if op == "+":
            self.assembly_file.write(f'  add t1, t1, t2\n')
        elif op == "-":
            self.assembly_file.write(f'  sub t1, t1, t2\n')
        elif op == "*":
            self.assembly_file.write(f'  mul t1, t1, t2\n')
        elif op == "/":
            self.assembly_file.write(f'  div t1, t1, t2\n')
            
        self.store_value(1, result)

    def create_output(self, arg):
        
        
        self.load_value(arg, 1)
        self.assembly_file.write('  mv a0, t1\n')
        self.assembly_file.write('  li a7, 1\n')  #  print integer
        self.assembly_file.write('  ecall\n')
        
        self.assembly_file.write('  li a0, 10\n')  # ASCII cde for newline
        self.assembly_file.write('  li a7, 11\n')  #   print character
        self.assembly_file.write('  ecall\n')

    def create_input(self, arg):
        
        self.assembly_file.write('  li a7, 5\n')  #   read integer
        self.assembly_file.write('  ecall\n')
        self.assembly_file.write('  mv t1, a0\n')
        self.store_value(1, arg)

    def create_parameter(self, arg1, arg2):
        
        if self.param_counter == -1:
            
            self.param_counter = 0
            
            
            func_name = None
            current_quad_index = None
            next_call_label = None
            
            
            for i, quad in enumerate(self.quad_manager.quads):
                if quad[1] == "par" and quad[2] == arg1 and quad[3] == arg2:
                    current_quad_index = i
                    break
            
            
            if current_quad_index is not None:
                for i in range(current_quad_index, len(self.quad_manager.quads)):
                    if self.quad_manager.quads[i][1] == "call":
                        func_name = self.quad_manager.quads[i][2]
                        next_call_label = self.quad_manager.quads[i][0]
                        break
            
            if func_name:
                
                self.current_called_function = func_name
                if next_call_label is not None:
                    self.call_setups[next_call_label] = func_name
                
                
                func_symbol = self.symbol_table.lookup(func_name, self.current_scope)
                if not func_symbol:
                    func_symbol = self.symbol_table.lookup(func_name) or self.symbol_table.lookup_with_nesting(func_name)
                
                if func_symbol:
                    
                    self.assembly_file.write(f'  # Setting up frame pointer for {func_name}\n')
                    self.assembly_file.write(f'  addi fp, sp, {func_symbol.frame_length}\n')
        
        if arg2 == "CV":  
           
            self.load_value(arg1, 0)
            self.assembly_file.write(f'  sw t0, -{12+4*self.param_counter}(fp)\n')
            self.param_counter += 1
        elif arg2 == "REF":  
            
            
            symbol = self.symbol_table.lookup(arg1, self.current_scope)
            if not symbol:
                symbol = self.symbol_table.lookup(arg1)
            if not symbol:
                symbol = self.symbol_table.lookup_with_nesting(arg1)
            
            if symbol:
                if symbol.scope == self.current_scope:
                    
                    self.assembly_file.write(f'  addi t0, sp, -{symbol.offset}\n')
                    self.assembly_file.write(f'  sw t0, -{12+4*self.param_counter}(fp)\n')
                elif symbol.scope == "global":
                    
                    self.assembly_file.write(f'  addi t0, gp, -{symbol.offset}\n')
                    self.assembly_file.write(f'  sw t0, -{12+4*self.param_counter}(fp)\n')
                else:
                   
                    self.gnlvcode(arg1, 0)
                    self.assembly_file.write(f'  sw t0, -{12+4*self.param_counter}(fp)\n')
                self.param_counter += 1
            else:
                if arg1.startswith("T@"):
                    
                    self.assembly_file.write(f'  addi t0, gp, -{int(arg1[2:])*4+40}\n')
                    self.assembly_file.write(f'  sw t0, -{12+4*self.param_counter}(fp)\n')
                    self.param_counter += 1
                else:
                    self.assembly_file.write(f'  # Warning: Symbol {arg1} not found in symbol table (current scope: {self.current_scope})\n')
                    self.param_counter += 1
        elif arg2 == "RET":  
            
            
            if arg1.startswith("T@"):
                self.assembly_file.write(f'  addi t0, gp, -{int(arg1[2:])*4+40}\n')
                self.assembly_file.write('  sw t0, -8(fp)\n')
            else:
                symbol = self.symbol_table.lookup(arg1)
                if not symbol:
                    symbol = self.symbol_table.lookup_with_nesting(arg1)
                
                if symbol:
                    if symbol.scope == "global":
                        self.assembly_file.write(f'  addi t0, gp, -{symbol.offset}\n')
                    else:
                        self.assembly_file.write(f'  addi t0, sp, -{symbol.offset}\n')
                    self.assembly_file.write('  sw t0, -8(fp)\n')
                else:
                    self.assembly_file.write(f'  # Warning: Symbol {arg1} not found in symbol table\n')
                    
    def load_value_reference(self, offset, register):
        
        # Load the address stored at offset(sp)
        self.assembly_file.write(f'  lw t0, {offset}(sp)\n')
        # Load the value from that address into the target register
        self.assembly_file.write(f'  lw t{register}, 0(t0)\n')
        
    def store_value_reference(self, register, offset):
       
        # Load the address stored at offset(sp)
        self.assembly_file.write(f'  lw t0, {offset}(sp)\n')
        # Store the value from register to that address
        self.assembly_file.write(f'  sw t{register}, 0(t0)\n')

    def create_call(self, func_name):
        
        func_symbol = self.symbol_table.lookup(func_name, self.current_scope)
        if not func_symbol:
            func_symbol = self.symbol_table.lookup(func_name) or self.symbol_table.lookup_with_nesting(func_name)
        if not func_symbol:
            self.assembly_file.write(f'  # Warning: Function {func_name} not found in symbol table (current scope: {self.current_scope})\n')
            return
            
        
        current_quad_label = None
        for i, quad in enumerate(self.quad_manager.quads):
            if quad[1] == "call" and quad[2] == func_name:
                current_quad_label = quad[0]
                break
        
        
        expected_func = None
        if current_quad_label in self.call_setups:
            expected_func = self.call_setups[current_quad_label]
            
        if expected_func and expected_func != func_name:
            self.assembly_file.write(f'  # Warning: Calling {func_name} but parameters were set up for {expected_func}\n')
            
            self.assembly_file.write(f'  # Fixing frame pointer setup for {func_name}\n')
            self.assembly_file.write(f'  addi fp, sp, {func_symbol.frame_length}\n')
        
        
        self.assembly_file.write(f'  # Setting up static link for {func_name}\n')
        if self.symbol_table.current_nesting_level() == func_symbol.nesting_level:
            
            self.assembly_file.write('  lw t0, -4(sp)\n')
            self.assembly_file.write('  sw t0, -4(fp)\n')
        else:
            
            self.assembly_file.write('  sw sp, -4(fp)\n')
            
        
        func_type = "function" if func_symbol.symbol_type == SymbolType.FUNCTION else "procedure"
        self.assembly_file.write(f'  # Calling {func_type} {func_name}\n')
        self.assembly_file.write(f'  addi sp, sp, {func_symbol.frame_length}\n')
        self.assembly_file.write(f'  jal L{func_symbol.entry_label}\n')
        
        
        if func_symbol.symbol_type == SymbolType.FUNCTION:
            self.assembly_file.write(f'  # Getting return value from function {func_name}\n')
            
            self.assembly_file.write('  lw t0, -8(sp)\n')
            
            self.assembly_file.write('  lw t1, 0(t0)\n')
            
            self.assembly_file.write('  sw t1, 0(t0)\n')
            
        
        self.assembly_file.write(f'  addi sp, sp, -{func_symbol.frame_length}\n')
        
        
        self.param_counter = -1
        if current_quad_label in self.call_setups:
            del self.call_setups[current_quad_label]

    def create_begin_block(self, block_name):
        
        self.current_scope = block_name
        self.scope_stack.append(block_name)  # Push new scope onto stack
        
        if block_name == self.quad_manager.program_name:
            
            
            frame_length = self.symbol_table.get_frame_length("global")
            self.assembly_file.write(f'  addi sp, sp, {frame_length}\n')  # Allocate space for main AR
            self.assembly_file.write('  mv gp, sp\n')  # Set global pointer
        else:
            
            self.assembly_file.write('  sw ra, 0(sp)\n')  # Save return address at offset 0
            
            
            func_symbol = self.symbol_table.lookup_in_all_scopes(block_name)
            if func_symbol and func_symbol.frame_length > 12:  
                self.assembly_file.write(f'  # Frame length: {func_symbol.frame_length}\n')
                self.assembly_file.write(f'  # Initializing local variables space\n')

    def create_end_block(self, block_name):
        
        if block_name != self.quad_manager.program_name:
            
            self.assembly_file.write('  lw ra, 0(sp)\n')  # Restore return address
            self.assembly_file.write('  jr ra\n')  # Return
        
        # Pop  scope 
        if len(self.scope_stack) > 1:
            self.scope_stack.pop()
            self.current_scope = self.scope_stack[-1]  # Set to parent scope
        else:
            self.current_scope = "global"

    def create_halt(self):
        
        self.assembly_file.write('  li a0, 0\n')  # Exit code 0
        self.assembly_file.write('  li a7, 93\n')  # System call for exit
        self.assembly_file.write('  ecall\n')

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


# Main 
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Usage: 'python compiler.py <file_name>.gr'")
        print("Exiting...")
        sys.exit(1)

    if not sys.argv[1].endswith('.gr'):
        print("Error: File must be of .gr type")
        print("Exiting...")
        sys.exit(1)

    filename = sys.argv[1]

    
    lexer = Lex(filename)
    token_list = lexer.analyze()
    del lexer

    
    parser = Syntax(token_list)
    parser.analyze()

    
    if hasattr(token_list[0], 'file_name') and token_list[0].file_name:
        input_file_path = token_list[0].file_name
    else:
        input_file_path = "output"
    
    original_file = os.path.basename(input_file_path)
    
    
    intermediate_file = original_file.replace('.gr', '.int')
    assembly_file = original_file.replace('.gr', '.s')
    symbol_file = original_file.replace('.gr', '.sym')

    
    parser.quad_manager.print_intermediate_code(intermediate_file)
    print(f"\nIntermediate code saved in: {intermediate_file}")

    
    parser.symbol_table.print_scope_info(symbol_file)
    print(f"Symbol table scope information saved in: {symbol_file}")
    
    
    riscv_gen = RISCVGenerator(parser.quad_manager, parser.symbol_table)
    riscv_gen.generate_code(assembly_file)
    print(f"RISC-V assembly  saved in: {assembly_file}")
    
    del parser 
