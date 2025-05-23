# On/mo: GEORGIOS NTZELVES AM: 5169
# On/mo: ALEXANDROS KOSTOPOULOS AM: 4937
# python version 3.13.3
# ο κώδικας τρέχει με την εντολή "py int_5169_4937.py 'opoiodhpote_arxeio_σε_greek++'"

import sys

# TOKENS #
greeklow = 'αβγδεζηθικλμνξοπρστφχψυως'
greeklowtone = 'άέήίόύώ'
greekcap = 'ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΦΧΨΥΩ'
englow = 'abcdefghijklmnopqrstuvwxyz'
engcap = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
digits = '0123456789'
numops = {'+','-','*','/'}
aops = {'<','>','=','<=','>=','<>'}
asym = {':='}
separators = {';',','}
groupsym = {'(',')','[',']'}
comments = {'{','}'}
whitespaces = {' ','\n','\t','\r'}
reference = {'%'}
keywords = {"πρόγραμμα", "δήλωση", "εάν", "τότε", "αλλιώς", "εάν_τέλος",
    "επανάλαβε", "μέχρι", "όσο", "όσο_τέλος", "για", "έως", "με_βήμα",
    "για_τέλος", "διάβασε", "γράψε", "συνάρτηση", "διαδικασία", "διαπροσωπεία",
    "είσοδος", "έξοδος", "αρχή_συνάρτησης", "τέλος_συνάρτησης", "αρχή_διαδικασίας",
    "τέλος_διαδικασίας", "αρχή_προγράμματος", "τέλος_προγράμματος", "ή", "και", "όχι",
    "εκτέλεσε"} 

############
## Τόκενς ##
############

class Token:
        def __init__(self, recognized_string, family, line_number):
               self.recognized_string = recognized_string
               self.family = family
               self.line_number = line_number

        def __str__(self):
                return f'string: {self.recognized_string} family: "{self.family}", line: {self.line_number}'
        
############
## Έρρορς ##
############

class CompilerError(Exception):
        def __init__(self, message, line = None, kind = "CompilerError"):
                line_info = f" [Line {line}]" if line else ""
                super().__init__(f"[{kind}] {line_info}: {message}")
        
class LexicalError(CompilerError):
        def __init__(self, message, line=None):
                super().__init__(message, line, kind="Lexical Error")

class SyntaxError(CompilerError):
        def __init__(self, message, line=None):
                super().__init__(message, line, kind="Syntax Error")

class SemanticError(CompilerError):
        def __init__(self, message, line=None):
                super().__init__(message, line, kind="Semantic Error")

########################
## Διαχειριστής Έρρορ ##
########################

class ErrorHandler:
    
        def raise_lexical(message, line=None):
                raise LexicalError(message, line)

        def raise_syntax(message, line=None):
                raise SyntaxError(message, line)

        def raise_semantic(message, line=None):
                raise SemanticError(message, line)

#######################
## Λεκτικός Αναλυτής ##
#######################

class Lex:
        def __init__(self, file_name):
                self.file_name = file_name
                self.position = 0
                self.current_line = 1
                self.tokens = []

                print(f"\nTrying to open file: {self.file_name}") 
                try:
                        with open(self.file_name, 'r', encoding='utf-8') as f: # άνοιγμα αρχείου
                                self.source = f.read()
                                print("File content loaded successfully.")
                except FileNotFoundError:
                        print(f'Error: File "{self.file_name}" not found.')
                        sys.exit(1)

                self.current_char = self.source[self.position] if self.source else None
                # print(self.source) # κάνε print στην οθόνη το αρχείο    

        # πήγαινε στην επόμενη θέση στο αρχείο #
        def advance(self):
                self.position += 1
                if self.position < len(self.source):
                        self.current_char = self.source[self.position]
                else:
                        self.current_char = None

        # πήγαινε στην επόμενη γραμμή στο αρχείο #
        def advance_line(self):
                self.current_line += 1

        # προσπέρασε τα κενά (και ειδικούς χαρακτήρες που δεν χρειάζονται) #
        def skip_whitespaces(self):
                while self.current_char and self.current_char in whitespaces:
                        if self.current_char == '\n':
                                self.advance_line()
                        self.advance()
        
        # προσπέρασε τα σχόλια #
        def skip_comment(self):
                if self.current_char == '{':
                        while self.current_char and self.current_char != '}':
                                if self.current_char in whitespaces:
                                        if self.current_char == '\n':
                                                self.advance_line() 
                                self.advance()
                        if self.current_char == '}':
                                self.advance()
                                self.skip_whitespaces()
                        else:
                                ErrorHandler.raise_lexical(f'unclosed comment', self.current_line)
        
        # πάρε και επέστρεψε αναγνωριστικά και δεσμευμένες λέξεις #
        def get_word(self):
                word = ''
                if self.current_char and (self.current_char in englow or self.current_char in engcap or self.current_char in greeklow or self.current_char in greekcap or self.current_char in greeklowtone):
                        word += self.current_char
                        self.advance()
                        while self.current_char and (self.current_char in englow or self.current_char in engcap or self.current_char in greeklow or self.current_char in greekcap or self.current_char in greeklowtone or self.current_char in digits or self.current_char == '_'):
                                if len(word) > 30:
                                        ErrorHandler.raise_lexical(f"Identifier is too long: '{word}'", self.current_line)
                                word += self.current_char
                                self.advance()
                
                        if word in keywords:
                                return Token(word, 'KEYWORD', self.current_line)
                        else:
                                return Token(word, 'IDENTIFIER', self.current_line)
                else:
                        ErrorHandler.raise_lexical('Invalid start of identifier', self.current_line)
        
        # πάρε και επέστρεψε ακέραιες σταθερές και αριθμούς #
        def get_number(self):
                number = ''
                if self.current_char and self.current_char in digits:
                        while self.current_char and self.current_char in digits:
                                if len(number) > 30:
                                        ErrorHandler.raise_lexical(f'Number is too long: {number}', self.current_line)
                                number += self.current_char
                                self.advance()
                        return Token(number, 'NUMBER', self.current_line)
                else:
                        ErrorHandler.raise_lexical(f'Invalid number', self.current_line)
        
        # πάρε και επέστρεψε σύμβολα αριθμητικών πράξεων #
        def get_numop(self):
                nop = ''
                if self.current_char and self.current_char in numops:
                        nop += self.current_char
                        self.advance()
                        return Token(nop, 'NUMERICAL OPERATOR', self.current_line)
        
        # πάρε και επέστρεψε τελεστές συσχέτισης #
        def get_aop(self):
                aop =''
                acheck = ''
                if self.current_char and self.current_char in {'<','>','='}:
                        aop += self.current_char
                        self.advance()
                        acheck = self.current_char
                        if self.current_char and ((aop in {'<','>'} and acheck == '=') or (aop == '<' and acheck == '>')):
                                acheck = aop + acheck
                                self.advance()
                                return Token(acheck, 'ASSOCIATIVE OPERATOR', self.current_line)
                        else:
                                return Token(aop, 'ASSOCIATIVE OPERATOR', self.current_line)

        # πάρε και επέστρεψε σύμβολα ανάθεσης #      
        def get_asym(self):
                assym = ''
                if self.current_char and self.current_char == ':':
                        assym += self.current_char
                        self.advance()
                        if self.current_char and self.current_char == '=':
                                assym += self.current_char
                                self.advance()
                                return Token(assym, 'ASSIGNMENT OPERATOR', self.current_line)
                        else:
                                ErrorHandler.raise_lexical(f'wrong assignment operator', self.current_line)
        
        # πάρε και επέστρεψε διαχωριστές #
        def get_separators(self):
                sep = ''
                if self.current_char and self.current_char in separators:
                        sep += self.current_char
                        self.advance()
                        return Token(sep, 'SEPARATOR', self.current_line)
        
        # πάρε και επέστρεψε σύμβολα ομαδοποίησης #
        def get_groupsym(self):
                gsym = ''
                if self.current_char and self.current_char in groupsym:
                        gsym += self.current_char
                        self.advance()
                        return Token(gsym, 'GROUP SYMBOL', self.current_line)

        # πάρε και επέστρεψε σύμβολα περάσματος παραμέτρων με αναφορά #   
        def get_reference(self):
                ref = ''
                if self.current_char and self.current_char in reference:
                        ref += self.current_char
                        self.advance()
                        return Token(ref, 'REFERENCE', self.current_line)
        
        # πάρε και επέστρεψε token #
        def get_token(self):
                while self.current_char:

                        # προσπερνάμε κενά (και χαρακτήρες που δεν χρειάζονται) και σχόλια
                        self.skip_whitespaces()
                        self.skip_comment()
                        
                        # αν ο χαρακτήρας είναι none τότε έχουμε φτάσει στο τέλος του αρχείου
                        if self.current_char is None:
                                print(f'End of file reached at line {self.current_line}')
                                return None

                        # ελέγχουμε τι χαρακτήρας είναι και τον επιστρέφουμε
                        if self.current_char and (self.current_char in englow or self.current_char in engcap or self.current_char in greeklow or self.current_char in greekcap or self.current_char in greeklowtone):
                                return self.get_word()
                        elif self.current_char and self.current_char in digits:
                                return self.get_number()
                        elif self.current_char and self.current_char in numops:
                                return self.get_numop()
                        elif self.current_char and self.current_char in {'<','>','='}:
                                return self.get_aop()
                        elif self.current_char and self.current_char == ':':
                                return self.get_asym()
                        elif self.current_char and self.current_char in separators:
                                return self.get_separators()
                        elif self.current_char and self.current_char in groupsym:
                                return self.get_groupsym()
                        elif self.current_char and self.current_char in reference:
                                return self.get_reference()
                        else:
                                ErrorHandler.raise_lexical(f"Invalid character: '{self.current_char}'", self.current_line)
        
        # φτιάχνουμε λίστα με τα tokens που βρήκαμε #
        def tokenize(self):
                print('\nStarting lexical analysis...')
                while self.current_char:
                        token = self.get_token()
                        if token:
                                self.tokens.append(token)
                return self.tokens

##########################
## Συντακτικός Αναλυτής ##
##########################

class Syntax:
        def __init__(self, tokens):
                self.tokens = tokens
                self.generated_program = [] # αποθήκευση τετράδων για risc-v
                self.position = 0 
                self.current_token = self.tokens[self.position]
                self.symbol_table = SymbolTable() # δημιουργία πίνακα συμβόλων
                self.quads = QuadList([], 0) # δημιουργία αντικειμένου που διαχειρίζεται τετράδες
                self.current_scope = None
                self.tmpVarCounter = 0 # μετρητής προσωρινών μεταβλητών
                
        
        # δημιούργησε καινούργια προσωρινή μεταβλητή #
        def newTemp(self):

                if not self.symbol_table.scopes:
                        ErrorHandler.raise_semantic("No active scope to insert temporary variable", self.current_token.line_number if self.current_token else None)
                name = f"T_{self.tmpVarCounter}" # όνοματα για προσωρινές μεταβλητές
                if self.symbol_table.search_entity(name):
                        ErrorHandler.raise_semantic(f"Temporary variable name conflict: '{name}' already exists", self.current_token.line_number if self.current_token else None)
                temp = TemporaryVariable(name)
                self.symbol_table.insert_entity(temp)
                self.tmpVarCounter += 1
                ar = self.symbol_table.scopes[-1].activation_record # ανάκτηση του ενεργού activation record
                if ar is None:
                        ErrorHandler.raise_semantic("No activation record found when inserting temporary variable",self.current_token.line_number if self.current_token else None)
                ar.insert('tmpVar', name) # προσθήκη της μεταβλητής στο activation record
                return name

        # πάρε το επόμενο token από τον πίνακα #
        def advance(self):
                self.position += 1
                if self.position < len(self.tokens):
                        self.current_token = self.tokens[self.position]
                else:
                        #self.current_token = None
                        ErrorHandler.raise_semantic("Unexpected end of token stream", None)

        # βοηθητική συνάρτηση που κοιτάει αν το string του token είναι ίδιο με αυτό που περιμένουμε #
        def match_string(self, expected_string):
                if self.current_token is None:
                        ErrorHandler.raise_syntax(f"Expected '{expected_string}' but reached end of input", None)
                if self.current_token and self.current_token.recognized_string == expected_string:
                        return True
                ErrorHandler.raise_syntax(f"Expected {expected_string} but found '{self.current_token.recognized_string}'", self.current_token.line_number)
        
        # βοηθητική συνάρτηση που κοιτάει αν το family του token είναι ίδιο με αυτό που περιμένουμε #
        def match_family(self, expected_family):
                if self.current_token is None:
                        ErrorHandler.raise_syntax(f"Expected token of family '{expected_family}' but reached end of input", None)
                if self.current_token and self.current_token.family == expected_family:
                        return True
                ErrorHandler.raise_syntax(f"Expected {expected_family} but found '{self.current_token.recognized_string}'", self.current_token.line_number)
        
        # ο συντακτικός αναλυτής #
        def syntax_analyzer(self):
                if not self.tokens:
                        ErrorHandler.raise_syntax("Empty token stream — no input to analyze", None)
                self.program()

                                ######
                        ######################
                ######################################
        ######################################################
        # όλες οι συναρτήσεις για την γραμματική της greek++ #
        ######################################################
                ######################################
                        ######################
                                ######

        # συνάρτηση για κύριο πρόγραμμα #
        def program(self):
                self.match_string('πρόγραμμα')
                self.advance()
                prog_name = self.current_token.recognized_string 
                self.match_family('IDENTIFIER')
                self.advance()
                scope = self.symbol_table.create_scope(prog_name) # δημιουργία καινούργιου scope με το όνομα του προγράμματος
                self.current_scope = scope # ορισμός ως τρέχον scope
                ar = ActivationRecord(prog_name, kind="program") # δημιουργία activation record για το κύριο πρόγραμμα
                scope.activation_record = ar # σύνδεση του activation record με το scope του προγράμματος
                self.quads.genQuad('begin_block', prog_name, '_', '_')
                self.programblock() # κλήση για ανάλυση του εσωτερικού του προγράμματος
                self.quads.genQuad('halt', '_', '_', '_')
                self.quads.genQuad('end_block', prog_name, '_', '_')
                self.quads.printQuads('output.int') # τύπωση τετράδων σε αρχείο
                program_entity = Program(prog_name)                    #|
                program_entity.activation_record = ar                  #| για να πάρουμε framelength για τελικό κώδικα
                self.symbol_table.insert_entity(program_entity)        #|
                program_entity.framelength = ar.framelength            #|
        
        # συνάρτηση για εσωτερικό κύριου προγράμματος #
        def programblock(self):
                self.declarations() # κλήση για έλεγχο και επεξεργασία δηλώσεων μεταβλητών
                self.subprograms() # κλήση για έλεγχο και επεξεργασία υποπρογραμμάτων
                self.match_string('αρχή_προγράμματος')
                self.advance()
                self.sequence() # κλήση για επεξεργασία ακολουθίας εντολών προγράμματος
                self.match_string('τέλος_προγράμματος')

        # συνάρτηση για δηλώσεις μεταβλητών # 
        def declarations(self):
                while self.current_token and self.current_token.recognized_string == 'δήλωση':
                        self.advance()
                        self.varlist(None, False, True) # κλήση για καταχώρηση μεταβλητών στον πίνακα συμβόλων

        # συνάρτηση για μεταβλητές και παραμέτρους που δηλώνονται και τι είδους είναι #
        def varlist(self, mode = None, as_parameter = False, from_dec = False): # mode για πέρασμα με τιμή ή αναφορά αν είναι παράμετρος
                                                                                # as_parameter αν είναι παράμετρος
                                                                                # from_dec αν είναι απλή δήλωση μεταβλητής
                if not self.symbol_table.scopes:
                        ErrorHandler.raise_semantic("No active scope to declare variable", self.current_token.line_number if self.current_token else None)

                scope = self.symbol_table.scopes[-1] # ανάκτηση τρέχοντος scope
                ar = scope.activation_record # άνακτηση του activation record του τρέχοντος scope

                if ar is None:
                        ErrorHandler.raise_semantic("Missing activation record for variable declaration", self.current_token.line_number if self.current_token else None)
                
                # βοηθητική συνάρτηση για εισαγωγή μεταβλητής ή παραμέτρου #
                def add_var(name):
                        existing = scope.search_entity(name) # έλεγχος για το αν η μεταβλητή υπάρχει ήδη στο scope
                        if existing: # αν υπάρχει
                                if from_dec: # αν είναι μεταβλητή
                                        ErrorHandler.raise_semantic(f"Redeclaration of variable '{name}'", self.current_token.line_number)
                                elif as_parameter and mode == None: # αν είναι παράμετρος χωρίς καθορισμένο τύπο
                                        ErrorHandler.raise_semantic(f"Redeclaration of parameter '{name}'", self.current_token.line_number)
                                elif as_parameter and (mode == 'ref' or mode == 'cv'): # αν είναι παράμετρος με επερχόμενο μαζί της τύπο για καθορισμό
                                        existing.mode = mode # καθορισμός του τύπου
                                        return # επιστροφή χωρίς προσθήκη εφόσον απλά περνάμε τον τύπο της
                        elif not existing and as_parameter and (mode == 'ref' or mode == 'cv'): # αν προσπαθούμε να καθορίσουμε τύπο σε παράμετρο που δεν είναι δηλωμένη
                                ErrorHandler.raise_semantic(f"Parameter '{name}' does not exist", self.current_token.line_number)
                        else: # αν δεν υπάρχει 
                                if as_parameter:
                                        entity = Parameter(name) # δημιουργία (αντικειμένου) παραμέτρου
                                        entity.mode = mode # καθορισμός τύπου (δεν χρειάζεται γιατί ο τύπος καθορίζεται όταν ο μεταφραστής ξαναδιαβάσει την παράμετρο από "είσοδος/έξοδος")
                                else:
                                        entity = Variable(name) # δημιουργία (αντικειμένου) μεταβλητής
                                self.symbol_table.insert_entity(entity) # εισαγωγή σε πίνακα συμβόλων
                        if ar: # ενημέρωση activation record με βάση τον τύπο (μεταβλητή ή παράμετρος)
                                if as_parameter and name not in ar.formalPar:
                                        ar.insert('formalPar', name)
                                elif from_dec and name not in ar.formalPar and name not in ar.localVar:
                                        ar.insert('localVar', name)
                self.match_family('IDENTIFIER')
                add_var(self.current_token.recognized_string) # κλήση της βοηθητικής
                self.advance()

                while self.current_token and self.current_token.recognized_string == ',': # πρόσθεση και άλλων μεταβλητών/παραμέτρων αν υπάρχουν
                        self.advance()
                        self.match_family('IDENTIFIER')
                        add_var(self.current_token.recognized_string)
                        self.advance()
        
        # συνάρτηση για χειρισμό συναρτήσεων και διαδικασιών #
        def subprograms(self):
                while self.current_token and self.current_token.recognized_string in ['συνάρτηση', 'διαδικασία']:
                        if self.current_token.recognized_string == 'συνάρτηση':
                                self.func() # κλήση για χειρισμό συνάρτησης
                                self.advance()
                        else:
                                self.proc() # κλήση για χειρισμό διαδικασίας
                                self.advance()
                                
        # διαχείριση συνάρτησης #
        def func(self): 
                self.match_string('συνάρτηση')
                self.advance()
                func_name = self.current_token.recognized_string # όνομα της συνάρτησης
                if self.symbol_table.search_entity(func_name):
                        ErrorHandler.raise_semantic(f"Redeclaration of function '{func_name}'", self.current_token.line_number)
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string('(')
                self.advance()
                scope = self.symbol_table.create_scope(func_name) # δημιουργία του scope της συνάρτησης
                self.current_scope = scope # ορισμός ως τρέχον scope
                ar = ActivationRecord(func_name, kind="function") # δημιουργία activation record για συνάρτηση
                if ar is None:
                        ErrorHandler.raise_semantic("Failed to create activation record for function", self.current_token.line_number)
                scope.activation_record = ar # αντιστοιχία activation record στο scope της συνάρτησης
                func_obj = Function(func_name, self.quads.nextQuad()) # δημιουργία αντικειμένου function
                func_obj.activation_record = ar # σύνδεση activation record με το αντικείμενο της συνάρτησης
                self.symbol_table.insert_entity(func_obj) # εισαγωγή της συνάρτησης στον πίνακα συμβόλων
                self.quads.genQuad('begin_block', func_name, '_', '_') 
                self.formalparlist() # κλήση για ανάλυση τυπικών παραμέτρων της συνάρτησης
                self.match_string(')')
                self.advance()
                self.current_function = func_name
                self.funcblock() # κλήση για εσωτερικό συνάρτησης
                func_obj.framelength = ar.framelength # καταγραφή framelength της συνάρτησης
                self.quads.genQuad('end_block', func_name, '_', '_')
                print(ar) # εκτύπωση activation record (για debugging)
                self.symbol_table.print_table(scope) # εκτύπωση πίνακα συμβόλων της συνάρτησης σε αρχείο
                self.symbol_table.delete_scope() # διαγραφή scope από τον πίνακα συμβόλων (πρακτικά κλείσιμο αυτού)
                
        # διαχείριση διαδικασίας (πρακτικά τα ίδια με συναρτήσεις) #
        def proc(self): 
                self.match_string('διαδικασία')
                self.advance()
                proc_name = self.current_token.recognized_string
                if self.symbol_table.search_entity(proc_name):
                        ErrorHandler.raise_semantic(f"Redeclaration of procedure '{proc_name}'", self.current_token.line_number)
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string('(')
                self.advance()
                scope = self.symbol_table.create_scope(proc_name) 
                self.current_scope = scope 
                ar = ActivationRecord(proc_name, kind="procedure")
                if ar is None:
                        ErrorHandler.raise_semantic("Failed to create activation record for procedure", self.current_token.line_number)
                scope.activation_record = ar 
                proc_obj = Procedure(proc_name, self.quads.nextQuad()) 
                proc_obj.activation_record = ar
                self.symbol_table.insert_entity(proc_obj) 
                self.quads.genQuad('begin_block', proc_name, '_', '_') 
                self.formalparlist()
                self.match_string(')')
                self.advance()
                self.procblock()
                proc_obj.framelength = ar.framelength
                self.quads.genQuad('end_block', proc_name, '_', '_')
                print(ar)
                self.symbol_table.print_table(scope)
                self.symbol_table.delete_scope()
                
        # συνάρτηση για τυπικές παραμέτρους #
        def formalparlist(self):
                if not self.symbol_table.scopes:
                        ErrorHandler.raise_semantic("No active scope for parameter declaration", self.current_token.line_number if self.current_token else None)

                if self.current_token and self.current_token.family == "IDENTIFIER":
                        self.varlist(None, True, False)
        
        # σώμα μίας συνάρτησης #
        def funcblock(self):
                self.match_string('διαπροσωπεία')
                self.advance()
                self.funcinput() # κλήση για διαχείριση παραμέτρων εισόδου 
                self.funcoutput() # κλήση για διαχείριση παραμέτρων εξόδου
                self.declarations() # κληση για διαχείρηση τοπικών μεταβλητών 
                self.subprograms() # κλήση για διαχείριση υποπρογραμμάτων (συναρτήσεις/διαδικασίες)
                self.match_string('αρχή_συνάρτησης')
                self.advance()
                self.sequence() # κλήση για διαχείριση σειράς εντολών της συνάρτησης
                self.match_string('τέλος_συνάρτησης')

        # σώμα μίας διαδικασίας (πρακτικά τα ίδια με συναρτήσεις) #
        def procblock(self):
                self.match_string('διαπροσωπεία')
                self.advance()
                self.funcinput()
                self.funcoutput()
                self.declarations()
                self.subprograms()
                self.match_string('αρχή_διαδικασίας')
                self.advance()
                self.sequence()
                self.match_string('τέλος_διαδικασίας')

        # συνάρτηση για διαχείριση δήλωσεων παραμέτρων εισόδου #   
        def funcinput(self):
                if not self.symbol_table.scopes:
                        ErrorHandler.raise_semantic("No active scope when declaring input parameters", self.current_token.line_number if self.current_token else None)

                while self.current_token and self.current_token.recognized_string == 'είσοδος':
                        self.advance()
                        self.varlist('cv', True) # πέρασμα με τιμή

        # συνάρτηση για διαχείριση δήλωσεων παραμέτρων εξόδου #
        def funcoutput(self):
                if not self.symbol_table.scopes:
                        ErrorHandler.raise_semantic("No active scope when declaring output parameters", self.current_token.line_number if self.current_token else None)

                while self.current_token and self.current_token.recognized_string == 'έξοδος':
                        self.advance()
                        self.varlist('ref', True) # πέρασμα με αναφορά

        # συνάρτηση για διαχείριση σειράς εντολών #
        def sequence(self):
                self.statement() # κλήση για διαχείριση πρώτης εντολής
                while self.current_token and self.current_token.recognized_string == ";":
                        self.advance()
                        self.statement() # κλήση για διαχείριση άλλων εντολών αν έχει
        
        # συνάρτηση για επεξεργασία εντολών #
        def statement(self):
                token = self.current_token
                if token:
                        if token.family == 'IDENTIFIER': # αν είναι αναγνωριστικό
                                self.assignment_stat() # κλήση για ανάθεση τιμής σε μεταβλητή
                        elif token.recognized_string == 'εάν':
                                self.if_stat()
                        elif token.recognized_string == 'όσο':
                                self.while_stat()
                        elif token.recognized_string == 'επανάλαβε':
                                self.do_stat()
                        elif token.recognized_string == 'για':
                                self.for_stat()
                        elif token.recognized_string == 'διάβασε':
                                self.input_stat()
                        elif token.recognized_string == 'γράψε':
                                self.print_stat()
                        elif token.recognized_string == 'εκτέλεσε':
                                self.call_stat()
                        else:
                                ErrorHandler.raise_syntax(f"Unexpected token {token.recognized_string}", token.line_number)
                else:
                        ErrorHandler.raise_syntax("Expected statement but found end of input", None)

        # συνάρτηση διαχείρισης εντολών ανάθεσης #
        def assignment_stat(self):
                var_name = self.current_token.recognized_string
                if self.symbol_table.search_entity(var_name) is None:
                        ErrorHandler.raise_semantic(f"Use of undeclared variable '{var_name}'", self.current_token.line_number)
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string(':=')
                self.advance()
                result = self.expression() # ανάλυση δεξιάς πλευράς της έκφρασης και ανάθεση
                if var_name == self.current_function:
                        self.quads.genQuad('ret', '_', '_', result)
                else:
                        self.quads.genQuad(':=', result, '_', var_name)

        # συνάρτηση για διαχείριση της "if" #
        def if_stat(self):
                self.match_string('εάν')
                self.advance()
                true_list, false_list = self.condition() # κλήση για ανάλυση συνθήκης και επιστροφή δύο λιστών
                                                         # true_list: λίστα θέσεων τετράδων που θα μεταπηδήσουν στο "τότε"
                                                         # false_list: λίστα θέσεων τετράδων που θα μεταπηδήσουν στο "αλλιώς" ή μετά από το "εάν_τέλος"
                self.match_string('τότε')
                self.advance()
                self.quads.backpatch(true_list, str(self.quads.nextQuad())) # backpatch της true_list 
                self.sequence()
                ifList = self.quads.makeList(self.quads.nextQuad()) # δημιουργία λίστας με επόμενες τετράδες
                self.quads.genQuad('jump', '_', '_', '_')
                self.quads.backpatch(false_list, str(self.quads.nextQuad())) # backpatch της false_list
                self.elsepart()
                self.quads.backpatch(ifList, str(self.quads.nextQuad())) # backpatch της ifList
                self.match_string('εάν_τέλος')
                self.advance()

        # συνάρτηση για διαχείριση της "else" #
        def elsepart(self):
                if self.current_token and self.current_token.recognized_string == 'αλλιώς':
                        self.advance()
                        self.sequence()

        # συνάρτηση για διαχείριση της "while" #
        def while_stat(self): 
                self.match_string('όσο')
                self.advance()
                start_quad = self.quads.nextQuad() # αποθήκευση αρχικού quad
                true_list, false_list = self.condition()
                self.match_string('επανάλαβε')
                self.advance()
                self.quads.backpatch(true_list, str(self.quads.nextQuad()))
                self.sequence()
                self.quads.genQuad('jump', '_', '_', str(start_quad)) # άλμα για επιστροφή στην αρχή του βρόχου
                self.quads.backpatch(false_list, str(self.quads.nextQuad()))
                self.match_string('όσο_τέλος')
                self.advance()

        # συνάρτηση για διαχείριση της "do" #
        def do_stat(self): 
                self.match_string('επανάλαβε')
                self.advance()
                start_quad = self.quads.nextQuad()
                self.sequence()
                self.match_string('μέχρι')       
                self.advance()
                true_list, false_list = self.condition() # ανάλυση συνθήκης που σταματάει τον βρόχο
                self.quads.backpatch(false_list, str(start_quad)) # αν η συνθήκη είναι false συνεχίζει την επανάληψη
                self.quads.backpatch(true_list, str(self.quads.nextQuad())) # αν η συνθήκη ειναι true προχωράει στην επόμενη εντολή

        # συνάρτηση για διαχείριση της "for" #
        def for_stat(self): 
                self.match_string('για')
                self.advance()
                id_name = self.current_token.recognized_string
                if self.symbol_table.search_entity(id_name) is None:
                        ErrorHandler.raise_semantic(f"Loop variable '{id_name}' is not declared", self.current_token.line_number)
                self.match_family('IDENTIFIER')
                self.advance()
                self.match_string(':=')
                self.advance()
                start_val = self.expression() # αρχική τιμή του μετρητή
                self.quads.genQuad(':=', start_val, '_', id_name)
                self.match_string('έως')
                self.advance()
                end_value = self.expression() # τελική τιμη του μετρητή
                step = '1' # προεπιλεγμένο βήμα
                if self.current_token and self.current_token.recognized_string == 'με_βήμα':
                        step = self.step() # κλήση για βήμα
                cond_quad = self.quads.nextQuad() # καταγραφή της θέσης σύγκρισης
                self.quads.genQuad('<=', id_name, end_value, '_')
                false_list = self.quads.makeList(self.quads.nextQuad()) # δημιουργία λίστας για άλμα αν η συνθήκη είναι false
                self.quads.genQuad('jump', '_', '_', '_')
                self.match_string('επανάλαβε')
                self.advance()
                self.quads.backpatch(self.quads.makeList(cond_quad), str(self.quads.nextQuad())) # backpatch του προηγούμενου jump για να δείχνει στην αρχή του σώματος
                self.sequence()
                temp = self.newTemp() # δημιουργία προσωρινής μεταβλητής για νέο υπολογισμό του μετρητή
                self.quads.genQuad('+', id_name, step, temp)
                self.quads.genQuad(':=', temp, '_', id_name)
                self.quads.genQuad('jump', '_', '_', str(cond_quad))
                self.quads.backpatch(false_list, str(self.quads.nextQuad())) # backpatch για συμπλήρωση τετράδων false_list ώστε να δείχνουν μετά την επανάληψη
                self.match_string('για_τέλος')
                self.advance()

        # συνάρτηση για επεξεργασία του προαιρετικού βήματος #
        def step(self):
                if self.current_token and self.current_token.recognized_string == 'με_βήμα':
                        self.advance()
                        return self.expression() # επιστροφή της αριθμητικής έκφρασης
                return '1'
        
        # συνάρτηση για τύπωση #
        def print_stat(self):
                self.match_string('γράψε')
                self.advance()
                expr_val = self.expression() # ανάθεση της έκφρασης που θα τυπωθεί
                self.quads.genQuad('out', expr_val, '_', '_')

        # συνάρτηση για διάβασμα #
        def input_stat(self):
                self.match_string('διάβασε')
                self.advance()
                self.match_family('IDENTIFIER')
                id_name = self.current_token.recognized_string
                if self.symbol_table.search_entity(id_name) is None:
                        ErrorHandler.raise_semantic(f"Use of undeclared variable '{id_name}' in 'διάβασε'", self.current_token.line_number)
                self.advance()
                self.quads.genQuad('in', id_name, '_', '_')

        # συνάρτηση για εκτέλεση διαδικασιών/συναρτήσεων #
        def call_stat(self):
                self.match_string('εκτέλεσε')
                self.advance()
                name = self.current_token.recognized_string
                entity = self.symbol_table.search_entity(name)
                if entity is None:
                        ErrorHandler.raise_semantic(f"Call to undeclared procedure or function '{name}'", self.current_token.line_number)
                if not isinstance(entity, (Function, Procedure)):
                        ErrorHandler.raise_semantic(f"'{name}' is not a callable procedure or function", self.current_token.line_number)
                self.match_family('IDENTIFIER')
                self.advance()
                self.idtail() # κλήση για ανάλυση παραμέτρων (ορισμάτων)
                self.quads.genQuad('call', name, '_', '_')

        # συνάρτηση για έλεγχο ύπαρξης ορισμάτων #
        def idtail(self):
                if self.current_token and self.current_token.recognized_string == '(':
                        self.actualpars() # κλήση για ανάλυση παραμέτρων (ορισμάτων)

        # συνάρτηση για επεξεργασία ορισμάτων #
        def actualpars(self):
                self.match_string('(')
                self.advance()
                self.actualparlist() # κλήση για ανάλυση παραμέτρων (ορισμάτων)
                self.match_string(')')
                self.advance()

        # συνάρτηση για επεξεργασία λίστας ορισμάτων #
        def actualparlist(self):
                if self.current_token and (self.current_token.recognized_string in {'+','-'} or self.current_token.family in {'NUMBER','IDENTIFIER'} or self.current_token.recognized_string == '(' or self.current_token.recognized_string == '%'):
                        self.actualparitem() # κλήση για ανάλυση πρώτου στοιχείου
                        while self.current_token and self.current_token.recognized_string == ',':
                                self.advance()
                                self.actualparitem() # κλήση για ανάλυση επόμενου στοιχείου

        # συνάρτηση για επεξεργασία ενός ορίσματος #
        def actualparitem(self):
                if self.current_token and (self.current_token.recognized_string in {'+','-'} or self.current_token.family in {'NUMBER','IDENTIFIER'} or self.current_token.recognized_string == '('): # κάλεσμα με τιμή
                        expr_val = self.expression() # αποθήκευση έκφρασης
                        self.quads.genQuad('par', expr_val, 'cv', '_')
                elif self.current_token and self.current_token.recognized_string == '%': # κάλεσμα με αναφορά
                        self.advance()
                        self.match_family('IDENTIFIER')
                        id_name = self.current_token.recognized_string
                        if self.symbol_table.search_entity(id_name) is None:
                                ErrorHandler.raise_semantic(f"Use of undeclared variable '{id_name}' as reference parameter", self.current_token.line_number)
                        self.advance()
                        self.quads.genQuad('par', id_name, 'ref', '_')
                else:
                        ErrorHandler.raise_syntax("Syntax error in actualparitem", self.current_token.line_number if self.current_token else None)

        # συνάρτηση για επεξεργασία λογικών συνθηκών #
        def condition(self):
                true_list, false_list = self.boolterm() # πρώτος λογικός όρος χωρίς "ή"
                while self.current_token and self.current_token.recognized_string == 'ή':
                        self.advance()
                        self.quads.backpatch(false_list, str(self.quads.nextQuad())) # backpatch την false_list για να δείχνει στον επόμενο όρο
                        new_true, new_false = self.boolterm() # ανάλυση επόμενου όρου
                        true_list = true_list.mergeList(new_true) # ενοποίηση true_list ώστε να συνεχίζουν όλοι στο ίδιο "τότε"
                        false_list = new_false # αντικατάσταση με καινούργια false_list
                return true_list, false_list # επιστροφή για backpatching από caller

        # συνάρτηση για επεξεργασία λογικών παραγόντων με το "και" #
        def boolterm(self):
                true_list, false_list = self.boolfactor() # ανάλυση πρώτου λογικού παράγοντα
                while self.current_token and self.current_token.recognized_string == 'και':
                        self.advance()
                        self.quads.backpatch(true_list, str(self.quads.nextQuad())) # αν ο προηγούμενος ήταν true συνέχισε με τον νέο όρο
                        new_true, new_false = self.boolfactor() # ανάλυση επόμενου παράγοντα
                        true_list = new_true # αντικατάσταση με καινούργια true_list
                        false_list = false_list.mergeList(new_false) # ενοποίηση false_list (αν οποιόσδηποτε είναι false τότε όλη η έκφραση είναι false)
                return true_list, false_list

        # συνάρτηση για επεξεργασία λογικών εκφράσεων #
        def boolfactor(self):
                if self.current_token.recognized_string == 'όχι':
                        self.advance()
                        self.match_string('[')
                        self.advance()
                        true_list, false_list = self.condition() # ανάλυση εσωτερικής συνθήκης
                        self.match_string(']')
                        self.advance()
                        return false_list, true_list # αντιστροφή και επιστροφή αφού έχουμε "όχι"
                elif self.current_token.recognized_string == '[':
                        self.advance()
                        true_list, false_list = self.condition()
                        self.match_string(']')
                        self.advance()
                        return true_list, false_list
                else: 
                        e1 = self.expression() # πρώτη έκφραση
                        relop = self.current_token.recognized_string # τελεστής
                        self.relational_oper() # κλήση για έλεγχο αν ο τελεστής είναι αποδεκτός
                        e2 = self.expression() # δεύτερη έκφραση
                        quad_true = self.quads.nextQuad() # true branch της σύγκρισης
                        self.quads.genQuad(f'{relop}', e1, e2, '_')
                        quad_false = self.quads.nextQuad() # false branch της σύγκρισης
                        self.quads.genQuad('jump', '_', '_', '_')
                        return self.quads.makeList(quad_true), self.quads.makeList(quad_false) # επιστροφή για μελλοντικό backpatching

        # συνάρτηση για επεξεργασία αριθμητικών εκφράσεων # 
        def expression(self):
                sign = ''
                if self.current_token.recognized_string in {'+', '-'}:
                        sign = self.current_token.recognized_string # αποθήκευση προσήμου
                        self.optional_sign() # κλήση για έλεγχο προσήμων
                result = self.term() # πρώτος όρος
                if sign: # αν υπάρχει πρόσημο δημιουργία τετράδας
                        temp = self.newTemp()
                        self.quads.genQuad(sign, '0', result, temp)
                        result = temp
                while self.current_token and self.current_token.recognized_string in {'+', '-'}: # όσο βρίσκει τελεστές συνεχίζει
                        op = self.current_token.recognized_string # αποθήκευση τελεστή
                        self.add_oper() # κλήση για έλεγχο τελεστή
                        term_val = self.term() # ανάληση επόμενου όρου
                        temp = self.newTemp()
                        self.quads.genQuad(op, result, term_val, temp)
                        result = temp
                return result
        
        # συνάρτηση για επεξεργασία πολλαπλασιαστικών εκφράσεων #
        def term(self):
                result = self.factor() # ανάλυση πρώτου όρου
                while self.current_token and self.current_token.recognized_string in {'*', '/'}:
                        op = self.current_token.recognized_string 
                        self.mul_oper()
                        factor_val = self.factor() # ανάλυση επόμενου όρου
                        temp = self.newTemp()
                        self.quads.genQuad(op, result, factor_val, temp)
                        result = temp
                return result

        # συνάρτηση για επεξεργασία παραγόντων αριθμητικών/λογικών εκφράσεων #
        def factor(self):
                if self.current_token.family == 'NUMBER':
                        val = self.current_token.recognized_string
                        self.advance()
                        return val
                elif self.current_token.recognized_string == '(':
                        self.advance()
                        val = self.expression() # ανάλυση έκφρασης
                        self.match_string(')')
                        self.advance()
                        return val
                elif self.current_token.family == 'IDENTIFIER':
                        id_name = self.current_token.recognized_string
                        if self.symbol_table.search_entity(id_name) is None:
                                ErrorHandler.raise_semantic(f"Use of undeclared variable or function '{id_name}'", self.current_token.line_number)
                        self.advance()
                        if self.current_token and self.current_token.recognized_string == '(': # αν ακολουθεί παρένθεση πρόκειται για κλήση συνάρτησης
                                self.actualpars() # κλήση για διαχείριση ορισμάτων
                                temp = self.newTemp()
                                self.quads.genQuad('par', temp, 'ret', '_')
                                self.quads.genQuad('call', id_name, '_', '_')
                                return temp # επιστροφή αποτελέσματος συνάρτησης
                        else: # απλή μεταβλητή/παράμετρος/όρισμα
                                self.idtail()
                                return id_name
                else:
                        ErrorHandler.raise_syntax("Syntax error in factor", self.current_token.line_number)

        # συνάρτηση για διαχείριση σχεσιακών τελεστών #
        def relational_oper(self):
                self.match_family('ASSOCIATIVE OPERATOR')
                self.advance()

        # συνάρτηση για διαχείριση προσθαφαιρετικών τελεστών #      
        def add_oper(self):
                if self.current_token.recognized_string in {'+', '-'}:
                        self.advance()
                else:
                        ErrorHandler.raise_syntax("Syntax error in add operator", self.current_token.line_number)
        
        # συνάρτηση για διαχείριση πολλαπλασιαστικών τελεστών #
        def mul_oper(self):
                if self.current_token.recognized_string in {'*', '/'}:
                        self.advance()
                else:
                       ErrorHandler.raise_syntax("Syntax error in mul operator", self.current_token.line_number) 
        
        # συνάρτηση για διαχείριση προσήμων (προαιρετικών) #
        def optional_sign(self):
                if self.current_token and self.current_token.recognized_string in {'+', '-'}:
                        self.add_oper()

########################
## Ενδιάμεσος Κώδικας ##
########################

# τετράδες #
class Quad:
        def __init__(self, label, op, op1, op2, op3):
                self.label = label
                self.op = op
                self.op1 = op1
                self.op2 = op2
                self.op3 = op3
        
        def __str__(self):
                return f"{self.label}: '{self.op},{self.op1},{self.op2},{self.op3}'"

# θέση τετράδας για backpatch #
class QuadPointer:
        def __init__(self, label):
                self.label = label
        
        def __str__(self):
                return f"{self.label}"

# διαχειριστής τετράδων #
class QuadList:
        def __init__(self, programList, quad_counter):
                self.programList = programList # λίστα τετράδων
                self.quad_counter = quad_counter # συνολικός αριθμητής τετράδων
                self.quadLabel = 100 # αριθμητής τετράδων
        
        def __str__(self):
                return f"Quad List: {self.programList} \n Number of quads created: {self.quad_counter}"

        def backpatch(self, quadPointerList, label): # συμπλήρωση τετράδων
                for pointer in quadPointerList.labelList:
                        for quad in self.programList:
                                if quad.label == pointer:
                                        if quad.op3 == '_':
                                                quad.op3 = label

        def genQuad(self, op, op1, op2, op3): # δημιουργία τετράδας
                quad = Quad(self.quadLabel, op, op1, op2, op3)
                self.programList.append(quad)
                self.quadLabel += 1
                self.quad_counter += 1

        def nextQuad(self): # επιστροφή επόμενης τετράδας
                return self.quadLabel
        
        def deleteQuad(self): # διαγραφή τετράδας
                if self.programList:
                        self.programList.pop()
        
        def makeList(self, label): # δημιουργία QuadPointerList
                return QuadPointerList([label])
        
        def emptyList(self): # δημιουργία άδειας λίστας
                return QuadPointerList([])
        
        def printQuads(self, filename): # τύπωση τετράδων σε αρχείο
                with open(filename, 'w', encoding = 'utf-8') as f:
                        for q in self.programList:
                                f.write(str(q) + '\n')

# λίστα από δείκτες σε τετράδες #
class QuadPointerList:
        def __init__(self, labelList):
                self.labelList = labelList
        
        def __str__(self):
                return f"{self.labelList}"

        def mergeList(self, otherList): # ενοποίηση λιστών
                return QuadPointerList(self.labelList + otherList.labelList)
        
        def append(self, label): # προσθήκη label στη λίστα
                self.labelList.append(label)

######################
## Πίνακας Συμβόλων ##
######################

# βασική κλάση entity που κληρονομούν όλα τα υπόλοιπα entities #
class Entity:
        def __init__(self, name):
                self.name = name

# πρόγραμμα (χρησιμοποιείται μόνο για να πάρουμε το offset για να κάνουμε χώρο στην στοίβα στον τελικό κώδικα)
class Program(Entity):
        def __init__(self,name):
                super().__init__(name)
                self.offset = 0
                self.activation_record = None
                self.framelength = 0

# μεταβλητές #
class Variable(Entity):
        def __init__(self, name):
                super().__init__(name)
                self.datatype = "INTEGER"
                self.offset = 0
                self.nestinglevel = 0

# παράμετροι #
class Parameter(Entity):
        def __init__(self, name):
                super().__init__(name)
                self.datatype = "INTEGER"
                self.mode = "cv" 
                self.offset = 0
                self.nestinglevel = 0

# συναρτήσεις #
class Function(Entity):
        def __init__(self, name, startingQuad):
                super().__init__(name)
                self.datatype = "INTEGER"
                self.startingQuad = startingQuad
                self.framelength = 0 
                self.formalParameters = []
                self.nestinglevel = 0
                self.activation_record = None
                self.returnValueAddress = 0

# διαδικασίες #
class Procedure(Entity):
        def __init__(self, name, startingQuad):
                super().__init__(name)
                self.startingQuad = startingQuad
                self.framelength = 0 
                self.formalParameters = []
                self.nestinglevel = 0
                self.activation_record = None

# για ορίσματα εν τέλη δεν χρειάστηκε γίνονται όλα μέσω της "Parameter" #
class FormalParameters(Entity):
    def __init__(self, name, datatype="INTEGER", mode="cv"):
        super().__init__(name)
        self.datatype = datatype
        self.mode = mode
        self.offset = 0
        self.nestinglevel = 0

# προσωρινές μεταβλητές #
class TemporaryVariable(Entity):
        def __init__(self, name):
                super().__init__(name)
                self.datatype = "INTEGER"
                self.offset = 0

# δεν χρειάστηκε είναι από το βιβλίο αλλά δεν χρησιμοποιείται σε greek++ #
class SymbolicConstant(Entity):
        def __init__(self, name, value):
                super().__init__(name)
                self.datatype = "INTEGER"
                self.value = value

# Scopes #
class Scope:
        def __init__(self, name):
                self.name = name
                self.entities = []
                self.nestinglevel = 0
                self.activation_record = None

        def insert_entity(self, entity): # προσθήκη entity
                last_offset = 12
                for i in reversed(self.entities):
                        if isinstance(i, (Variable, Parameter, TemporaryVariable)):
                                last_offset = i.offset + 4
                                break
                entity.offset = last_offset  
                entity.nestinglevel = self.nestinglevel
                self.entities.append(entity)

        def search_entity(self,name): # αναζήτηση entity
                for entity in self.entities:
                        if entity.name == name:
                                return entity
                return None

# πίνακας συμβόλων #
class SymbolTable:
        def __init__(self):
                self.scopes = []
                self.closed_scopes = []

        def create_scope(self, name): # δημιουργία scope
                scope = Scope(name)
                if self.scopes:
                        scope.nestinglevel = self.scopes[-1].nestinglevel + 1
                else:
                        scope.nestinglevel = 0
                self.scopes.append(scope)
                return scope

        def delete_scope(self): # διαγραφή scope
                if self.scopes:
                        closed = self.scopes.pop()
                        self.closed_scopes.append(closed)

        def insert_entity(self, entity): # προσθήκη entity
                if self.scopes:
                        last_scope = self.scopes[-1]
                        last_scope.insert_entity(entity)
                else:
                        raise Exception("No scope created yet")

        def search_entity(self, name): # αναζήτηση entity
                for i in reversed(self.closed_scopes + self.scopes):
                        result = i.search_entity(name)
                        if result:
                                return result
                return None

        def print_table(self, scope): # τύπωση πίνακα συμβόλων σε αρχείο
                with open("output.sym", 'a', encoding = 'utf-8') as f:
                        f.write(f"Scope: {scope.name} (Nesting Level: {scope.nestinglevel})\n")

                        if not scope.entities:
                                f.write("  [Empty scope]\n\n")
                                return

                        for entity in scope.entities:
                                if isinstance(entity, Variable):
                                        f.write(f"  - Variable '{entity.name}', Offset: {entity.offset}, Type: {entity.datatype}\n")

                                elif isinstance(entity, Parameter):
                                        f.write(f"  - Parameter '{entity.name}', Mode: {entity.mode}, Offset: {entity.offset}, Type: {entity.datatype}\n")

                                elif isinstance(entity, Function):
                                        f.write(f"  - Function '{entity.name}', StartingQuad: {entity.startingQuad}, Framelength: {entity.framelength}, Type: {entity.datatype}\n")

                                elif isinstance(entity, Procedure):
                                        f.write(f"  - Procedure '{entity.name}', StartingQuad: {entity.startingQuad}, Framelength: {entity.framelength}\n")

                                elif isinstance(entity, TemporaryVariable):
                                        f.write(f"  - TempVar '{entity.name}', Offset: {entity.offset}, Type: {entity.datatype}\n")

                                elif isinstance(entity, SymbolicConstant):
                                        f.write(f"  - Constant '{entity.name}', Value: {entity.value}, Type: {entity.datatype}\n")

                        f.write("\n")

# Activation Record # 
class ActivationRecord:
        def __init__(self, name, kind=None):
                self.name = name # όνομα του scope
                self.kind = kind # συνάρτηση/διαδικασία/πρόγραμμα
                self.returnAddress = 0 # διεύθυνση επιστροφής 
                self.sp = 0 # δεν χρησιμοποιείται εν τέλη (stack pointer)
                self.returnValueAddress = 0 # διεύθυνση αποθήκευσης τιμής επιστροφής
                self.formalPar = [] # λίστα ονομάτων παραμέτρων
                self.localVar = [] # λίστα τοπικών μεταβλητών
                self.tmpVars = [] # λίστα προσωρινών μεταβλητών
                self.framelength = 12 # αρχικό μέγεθος activation record

        def insert(self, category, name): # προσθήκη παραμέτρων/μεταβλητών(τοπικών/προσωρινών) στο activation record και στις λίστες
                if category == 'formalPar':
                        self.formalPar.append(name)
                        self.framelength += 4
                elif category == 'localVar':
                        self.localVar.append(name)
                        self.framelength += 4
                elif category == 'tmpVar':
                        self.tmpVars.append(name)
                        self.framelength += 4
            
        def __str__(self): # εκτύπωση activation record (στην οθόνη για debugging)
                return f'\nActivation Record for {self.kind} {self.name}:\nFormal parameters list: {self.formalPar}\nLocal variables list: {self.localVar}\nTemporary variables list: {self.tmpVars}\nFramelength: {self.framelength} bytes'

#####################
## ΤΕΛΙΚΟΣ ΚΩΔΙΚΑΣ ##
#####################

# πρόσθεση γραμμής risc-v σε αρχείο #
def produce(line):
        with open("final.asm", "a", encoding="utf-8") as f:
                f.write(line + "\n")

# εύρεση διεύθυνσης μεταβλητής που βρίσκεται σε πρόγονο scope #
def gnlvcode(id, symbol_table):
        if isinstance(id, TemporaryVariable):
                return
        
        if isinstance(id, (Parameter,Variable)): # μπορει να θελει και function,procedure
                entity = None
                level_diff = 0

                for scope in reversed(symbol_table.scopes): # reversed επειδή είναι στοίβα
                        level_diff += 1
                        entity = scope.search_entity(id)

                if entity is None:
                        raise Exception(f"Identifier '{id}' not found for gnlvcode.")

                produce("lw t0, -4(sp)") # -4 γιάτι εκεί είναι ο σύνδεσμος προσπέλασης
                for i in range(level_diff - 1):
                        produce("lw t0, -4(t0)") # για κάθε επίπεδο που ανεβαίνει (αν χρειάζεται)
                produce(f"addi t0, t0, -{entity.offset}") # πραγματική διεύθυνση της μεταβλητής 

# φόρτωση της μεταβλητής v στον καταχωρητή r από το σωστό scope #
def loadvr(v, r, symbol_table):
        if v.isdigit():
                produce(f"li {r}, {v}")
                return

        for scope in reversed(symbol_table.scopes):
                entity = scope.search_entity(v)
                if entity:
                        curr_scope = symbol_table.scopes[-1]
                        if scope.nestinglevel == 0:
                                produce(f"lw {r}, -{entity.offset}(gp)")
                        elif scope == curr_scope:
                                if (isinstance(entity, Parameter) and entity.mode == 'cv') or isinstance(entity, (Variable,TemporaryVariable)):
                                        produce(f"lw {r}, -{entity.offset}(sp)")
                                elif isinstance(entity, Parameter) and entity.mode == 'ref':
                                        produce(f"lw t0, -{entity.offset}(sp)")
                                        produce(f"lw {r}, (t0)")
                        else:
                                if (isinstance(entity, Parameter) and entity.mode == 'cv') or isinstance(entity, Variable):
                                        gnlvcode(v, symbol_table)
                                        produce(f"lw {r}, (t0)")
                                elif isinstance(entity, Parameter) and entity.mode == 'ref':
                                        gnlvcode(v, symbol_table)
                                        produce("lw t0, (t0)")
                                        produce(f"lw {r}, (t0)")

# γράψιμο τιμής του καταχωρητή r στην μεταβλητή v από το σωστό scope #
def storerv(r, v, symbol_table): # παρόμοια πράγματα με την loadvr για σχόλια :)
        if r.isdigit():
                loadvr(r, "t0", symbol_table)
                r = "t0"

        for scope in reversed(symbol_table.scopes):
                entity = scope.search_entity(v)
                if entity:
                        curr_scope = symbol_table.scopes[-1]
                        if scope.nestinglevel == 0:
                                produce(f"sw {r}, -{entity.offset}(gp)")
                        elif scope == curr_scope:
                                if (isinstance(entity, Parameter) and entity.mode == 'cv') or isinstance(entity, (Variable,TemporaryVariable)):
                                        produce(f"sw {r}, -{entity.offset}(sp)")
                                elif isinstance(entity, Parameter) and entity.mode == 'ref':
                                        produce(f"lw t0, -{entity.offset}(sp)")
                                        produce(f"sw {r}, (t0)")
                        else:
                                if (isinstance(entity, Parameter) and entity.mode == 'cv') or isinstance(entity, Variable):
                                        gnlvcode(v, symbol_table)
                                        produce(f"sw {r}, (t0)")
                                elif isinstance(entity, Parameter) and entity.mode == 'ref':
                                        gnlvcode(v, symbol_table)
                                        produce("lw t0, (t0)")
                                        produce(f"sw {r}, (t0)")

# παραγωγή τελικού κώδικα μηχανής #
def generate_final_code(quad_list, symbol_table):
        last_called_function = None
        par_index = 0
        first_par = True
        function_labels = {}

        with open("final.asm", "w", encoding="utf-8") as f:
                f.write(".data\nstr_nl: .asciz \"\\n\"\n.text\n") # δήλωση string για αλλαγή γραμμής

        produce("L0:")
        produce("j main")

        for quad in quad_list.programList: 
                label = f"L{quad.label - 99}"
                op, x, y, z = quad.op, quad.op1, quad.op2, quad.op3
                produce(f"{label}:")
                
                if op == ":=":
                        loadvr(x, "t0", symbol_table)
                        storerv("t0", z, symbol_table)

                elif op in ['+', '-', '*', '/']:
                        loadvr(x, "t1", symbol_table)
                        loadvr(y, "t2", symbol_table)
                        numops_map = {'+': 'add', '-': 'sub', '*': 'mul', '/': 'div'}
                        produce(f"{numops_map[op]} t1, t2, t1") 
                        storerv("t1", z, symbol_table)

                elif op in ['<', '<=', '>', '>=', '=', '<>']:
                        relop_map = {'=': 'beq', '<>': 'bne', '<': 'blt', '>': 'bgt', '<=': 'ble', '>=': 'bge'}
                        loadvr(x, "t1", symbol_table)
                        loadvr(y, "t2", symbol_table)
                        produce(f"{relop_map[op]} t1, t2, L{int(z) - 99}")

                elif op == "jump":
                        produce(f"j L{int(z) - 99}")

                elif op == "out":
                        loadvr(x, "a0", symbol_table)
                        produce("li a7, 1") # syscall για print_int
                        produce("ecall")
                        produce("la a0, str_nl") # αλλαγή γραμμής
                        produce("li a7, 4") # syscall για print_string
                        produce("ecall")

                elif op == "in":
                        produce("li a7, 5") # syscall για read_int
                        produce("ecall")
                        storerv("a0", x, symbol_table)

                elif op == "halt":
                        produce("li a0, 0") # exit code 0
                        produce("li a7, 93") # syscall για terminate
                        produce("ecall")

                elif op == "begin_block":
                        function_labels[x] = quad.label # για να βρούμε το label για jal στην call
                        for scope in symbol_table.scopes:                                             
                                for entity in scope.entities:                                          
                                        if isinstance(entity, Program):                                 
                                                frame_len = entity.activation_record.framelength       
                                                prog_name = entity.activation_record.name              
                        if x == prog_name: # αν είναι το main πρόγραμμα
                                produce("main:") 
                                produce(f"addi sp, sp, -{frame_len}") # κράτηση χώρου στη στοίβα
                                produce("mv gp, sp")
                                last_called_function = x
                        else: # αν είναι συνάρτηση
                                produce("sw ra, 0(sp)") # αποθήκευση διεύθυνσης επιστροφής
                                last_called_function = x

                elif op == "end_block":
                        produce("lw ra, 0(sp)") # επαναφορά διεύθυνσης επιστροφής
                        produce("jr ra") # επιστροφή στη καλούσα

                elif op == "ret":
                        for scope in reversed(symbol_table.closed_scopes + symbol_table.scopes):
                                entity = scope.search_entity(z)
                                if entity:
                                        offset = entity.offset
                                        break
                        produce(f"lw t0, -8(sp)")
                        produce(f"lw t1, -{offset}(sp)")
                        produce("sw t1, (t0)")
                
                elif op == "par" and y != "ret":
                        if first_par == True:
                                caller = symbol_table.search_entity(last_called_function)
                                frame_length = caller.activation_record.framelength
                                produce(f"addi fp, sp, -{frame_length}")
                                first_par = False
                        par_index += 1
                        if y == "cv":
                                loadvr(x, "t0", symbol_table)
                                d = 12 + (par_index - 1) * 4 # offset i-οστής παραμέτρου συνάρτησης (i == par_index)
                                produce(f"sw t0, -{d}(fp)")
                        elif y == "ref":
                                d = 12 + (par_index - 1) * 4
                                caller_entity = symbol_table.search_entity(last_called_function)
                                caller_level = caller_entity.nestinglevel
                                
                                entity = None
                                entity_scope = None
                                for scope in reversed(symbol_table.scopes):
                                                entity = scope.search_entity(x)
                                                if entity:
                                                        entity_scope = scope
                                                        break

                                if entity:
                                        var_level = entity_scope.nestinglevel
                                        # α)
                                        if var_level == caller_level: # αν το entity βρίσκεται στην καλούσα
                                                # i) τοπική μεταβλητή ή προσωρινή μεταβλητή ή παράμετρος που έχει περαστεί με τιμή στη συνάρτηση
                                                if isinstance(entity, (Variable,TemporaryVariable)) or (isinstance(entity, Parameter) and entity.mode == 'cv'):
                                                        produce(f"addi t0, sp, -{entity.offset}")
                                                        produce(f"sw t0, -{d}(fp)")
                                                # ii) παράμετρος που έχει περαστεί με αναφορά στην καλούσα συνάρτηση ή διαδικασία
                                                elif isinstance(entity, Parameter) and entity.mode == 'ref':
                                                        produce(f"lw t0, -{entity.offset}(sp)")
                                                        produce(f"sw t0, -{d}(fp)")
                                        # β)
                                        if var_level < caller_level and var_level != 0: # αν το entity βρίσκεται σε πρόγονο
                                                # i) τοπική μεταβλητή ή παράμετρος που έχει περαστεί με τιμή σε συνάρτηση πρόγονο στην οποία ανήκει
                                                if isinstance(entity, Variable) or (isinstance(entity, Parameter) and entity.mode == 'cv'):
                                                        gnlvcode(x, symbol_table)
                                                        produce(f"sw t0, -{d}(fp)")
                                                # ii) παράμετρος που έχει περαστεί με αναφορά σε συνάρτηση ή διαδικασία πρόγονο
                                                elif isinstance(entity, Parameter) and entity.mode == 'ref':
                                                        gnlvcode(x, symbol_table)
                                                        produce(f"lw t0, (t0)")
                                                        produce(f"sw t0, -{d}(fp)")
                                        # γ)
                                        elif var_level == 0: # αν το entity είναι καθολική μεταβλητή
                                                produce(f"addi t0, gp, -{entity.offset}")
                                                produce(f"sw t0, -{d}(fp)")

                elif op == "par" and y == "ret":
                        for scope in reversed(symbol_table.closed_scopes + symbol_table.scopes):
                                entity = scope.search_entity(x)
                                if entity:
                                        offset = entity.offset
                                        break
                        produce(f"addi t0, sp, -{offset}")
                        produce("sw t0, -8(fp)")
                
                elif op == "call":
                        if first_par == True:
                                caller = symbol_table.search_entity(last_called_function)
                                frame_length = caller.activation_record.framelength
                                produce(f"addi fp, sp, -{frame_length}")
                        else:
                                caller = symbol_table.search_entity(last_called_function)
                                caller_level = caller.nestinglevel
                                callee = symbol_table.search_entity(x)
                                callee_frame_len = callee.activation_record.framelength
                                callee_level = callee.nestinglevel
                                if callee_level == caller_level - 1:
                                        produce("sw sp, -4(fp)")
                                elif callee_level == caller_level:
                                        produce("lw t0, -4(sp)")
                                        produce("sw t0, -4(fp)")
                                labell = function_labels.get(x)
                                produce(f"addi sp, sp, {callee_frame_len}")
                                produce(f"jal L{labell - 99}")
                                produce(f"addi sp, sp, -{callee_frame_len}")
                                first_par = True


        # na tsekarw quads
        # na diavasw thewria na kanw anafora
        # na valw ta ypoloipa sxolia
           

if __name__ == "__main__":
        if len(sys.argv) != 2:
                print("Code runs with 'py' followed by 'int_5169_4937.py' and 'opoiodhpote_arxeio_σε_greek++'")
                print("Please try again!")
                sys.exit(1)

        file_name = sys.argv[1]

        try:
                tokens = Lex(file_name).tokenize() # κλήση του λεκτικού αναλυτή
                print('Generating tokens...')
                print('Lexical analysis succesfully completed!')
                print('Tokens generated!')
                #for token in tokens:
                        #print(token) # τύπωσε τα tokens που βρήκε ο λεκτικός αναλυτής
                
                parser = Syntax(tokens) # δημιουργία του συντακτικού αναλυτή
                print('\nStarting syntax analysis...')

                parser.program() # έναρξη της συντακτικής ανάλυσης
                print('Syntax analysis succesfully completed!')

                parser.quads.printQuads("output.int")
                print("\nIntermediate code written to 'output.int'")

                with open("output.sym", 'w', encoding = 'utf-8') as f:
                        f.write("Symbol Table:\n\n")

                for scope in parser.symbol_table.closed_scopes: # τύπωση κλειστών scopes
                        parser.symbol_table.print_table(scope)
                for scope in parser.symbol_table.scopes: # τύπωση τελευταίου ενεργού scope
                        parser.symbol_table.print_table(scope)
                print("Symbol table written to 'output.sym'")

                generate_final_code(parser.quads, parser.symbol_table) # έναρξη δημιουργίας τελικού κώδικα
                print("Final code written to 'final.asm'\n")

        except CompilerError as e:
                print(f"\n Compilation Error:\n{e}")
                sys.exit(1)
        except Exception as e:
                print(f"\n Unexpected Error:\n{e}")
                sys.exit(1)

