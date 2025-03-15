import sys
import os
from lexer import TokenFamily, Lex, Token

class Syntax:
    # constructor
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

        print("-- Syntax Analyzer --")
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
        
    def throwInvalidError(self):
        print(f"Syntax Error: Got invalid phrase '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)
    
    def throwError(self, expected):
        print(f"Syntax Error: Expected {expected}, but got '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)

    def throwTypeError(self, expected):
        print(f"Syntax Error: Expected type '{expected.name}', but got type '{self.current_token.family.name}' at line {self.current_token.line_number}")
        sys.exit(1)

    # methodos analysis pou ksekinaei tin syntaktiki analysi me ti
    # methodo anadromikis katavasis
    def analyze(self):
        
        for token in self.tokens:
            if token.family.name =="ERROR":
                print(f"Syntax Error: Invalid token '{token.recognized_string}' at line {token.line_number}")
                sys.exit(1)

        self.program()

    # --------------------------------------- #
    # 38 private methodoi grammatikis glwssas #

    #SOS#
    # NA PROSTETHOUN OI ; DELIMITERS KAI ERRORS
    def program(self):
        if self.current_token.recognized_string != "πρόγραμμα":
            self.throwError("πρόγραμμα")

        self.get_token() #move to next token: <ID> 

        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.programblock()
    
    def programblock(self):
        self.declarations()
        self.subprograms()
        self.get_token()
        if self.current_token.recognized_string != "αρχή_προγράμματος":
            self.throwError("αρχή_προγράμματος")
        self.get_token()
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != "τέλος_προγράμματος":
            self.throwError("τέλος_προγράμματος")
    
    def declarations(self):
     
        while self.tokens[self.token_index+1].recognized_string =="δήλωση":
            self.get_token()
            self.varlist() 
        self.get_token()
            
            
    def varlist(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        
        while self.tokens[self.token_index+1].recognized_string ==",":
            self.get_token()
            self.get_token()
            if self.current_token.family != TokenFamily.IDENTIFIER:
                self.throwTypeError(TokenFamily.IDENTIFIER)  
        
    def subprograms(self):
       
        while self.current_token.recognized_string == "συνάρτηση" or self.current_token.recognized_string == "διαδικασία":
            if self.current_token.recognized_string == "συνάρτηση":
                self.func()
            elif self.current_token.recognized_string == "διαδικασία":
                self.proc()
            else:
                self.throwError("συνάρτηση or διαδικασία")
        

    def func(self):
        
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwError("(")
            
        self.formalparlist()
        
        
        if self.current_token.recognized_string != ")":
            self.throwError(")")
        
        self.funcblock()

    def proc(self):
        self.get_token()
        if self.current_token.recognized_string != "διαδικασία":
            self.throwError("διαδικασία")
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwError("(")
        self.get_token()
        self.formalparlist()
        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwError(")")
        self.get_token()
        self.procblock()
            
    def formalparlist(self):
        if self.tokens[self.token_index+1].family == TokenFamily.IDENTIFIER:
            self.varlist()
            self.get_token()
        else: self.get_token()
 
        
    def funcblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.throwError("διαπροσωπεία")
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()
        
        if self.current_token.recognized_string != "αρχή_συνάρτησης":
            self.throwError("αρχή_συνάρτησης")
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != "τέλος_συνάρτησης":
            self.throwError("τέλος_συνάρτησης")
    
    def procblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.throwError("διαπροσωπεία")
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()
        self.get_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            self.throwError("αρχή_διαδικασίας")
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            self.throwError("τέλος_διαδικασίας")
    
    def funcinput(self):
        if self.tokens[self.token_index+1].recognized_string == "είσοδος":
            self.get_token()
            self.varlist()

    def funcoutput(self):
        if self.tokens[self.token_index+1].recognized_string == "έξοδος":
            self.get_token()
            self.varlist()
    
    # to do
    #
    def sequence(self):
        self.statement()
        while self.current_token.recognized_string == ";":
            self.statement()
    
    def statement(self):
        # krufokoitazw mprosta
        next_token_string = self.tokens[self.token_index+1].recognized_string
        next_token_family = self.tokens[self.token_index+1].family

        if next_token_family == TokenFamily.IDENTIFIER:
            self.assignment_stat()
        elif next_token_string == 'εάν':
            self.if_stat()
        elif next_token_string == 'όσο':
            self.while_stat()
        elif next_token_string == 'επανάλαβε':
            self.do_stat()
        elif next_token_string == 'για':
            self.for_stat()
        elif next_token_string == 'διάβασε':
            self.input_stat()
        elif next_token_string == 'γράψε':
            self.print_stat()
        elif next_token_string == 'εκτέλεσε':
            self.call_stat()

        self.throwInvalidError()

    def assignment_stat(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT)
        self.expression()

    def if_stat(self):
        self.get_token()
        self.condition()
        self.get_token()
        if self.current_token.recognized_string != 'τότε':
            self.throwError('τότε')
        self.sequence()
        self.elsepart()
        self.get_token()
        if self.current_token.recognized_string != 'εάν_τότε':
            self.throwError('εάν_τότε')

    def elsepart(self):
        if self.tokens[self.token_index+1].recognized_string == 'αλλιώς':
            self.get_token()
            self.sequence()

    def while_stat(self):
        self.get_token()
        self.condition()
        self.get_token()
        if self.current_token.recognized_string != 'επανάλαβε':
            self.throwError('επανάλαβε')
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != 'όσο_τέλος':
            self.throwError('όσο_τέλος')
        
    def do_stat(self):
        self.get_token()
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != 'μέχρι':
            self.throwError('μέχρι')
        self.condition()
    
    def for_stat(self):
        self.get_token()
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.get_token()
        if self.current_token.family != TokenFamily.ASSIGNMENT:
            self.throwTypeError(TokenFamily.ASSIGNMENT)
        self.expression()
        self.get_token()
        if self.current_token.recognized_string != 'έως':
            self.throwError('έως')
        self.expression()
        self.step()
        self.get_token()
        if self.current_token.recognized_string != 'επανάλαβε':
            self.throwError('επανάλαβε')
        self.sequence()
        self.get_token()
        if self.current_token.recognized_string != 'για_τέλος':
            self.throwError('για_τέλος')
    
    def step(self):
        if self.tokens[self.token_index+1].recognized_string == 'με_βήμα':
            self.get_token()
            self.expression()

    def print_stat(self):
        self.get_token()
        if self.current_token.recognized_string != 'γράψε':
            self.throwError('γράψε')
        self.expression()

    def input_stat(self):
        self.get_token()
        if self.current_token.recognized_string != 'διάβασε':
            self.throwError('διάβασε')
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

    def call_stat(self):
        self.get_token()
        if self.current_token.recognized_string != 'εκτέλεσε':
            self.throwError('εκτέλεσε')
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        self.idtail()

    def idtail(self):
        if self.tokens[self.token_index+1].recognized_string == '(':
            self.actualpars()

    def actualpars(self):
        self.get_token()
        self.actualparlist()
        self.get_token()
        if self.current_token.recognized_string != ')':
            self.throwError(')')
    
    
    def actualparlist(self):
        self.actualparitem()
        while self.current_token.recognized_string == ",":
            self.actualparitem()
    
    def actualparitem(self):
        self.get_token()
        self.expression()
        if self.current_token.recognized_string == "με_αναφορά":
            self.get_token()
            if self.current_token.family != TokenFamily.IDENTIFIER:
                self.throwTypeError(TokenFamily.IDENTIFIER)

                
    def condition(self):
        self.boolterm()
        while self.current_token.recognized_string == "ή":
            self.boolterm()
    
    def boolterm(self):
        self.boolfactor()
        while self.current_token.recognized_string == "και":
            self.boolfactor()

    def boolfactor(self):
        self.get_token()
        if self.current_token.recognized_string == "όχι":
            self.get_token()
            if self.current_token.recognized_string == "[":
                self.condition()
                self.get_token()
                if self.current_token.recognized_string != "]":
                    self.throwError("]")
        if self.current_token.recognized_string == "[":
            self.condition()
            self.get_token()
            if self.current_token.recognized_string != "]":
                self.throwError("]")
        else:
            self.expression()
            self.relational_oper()
            self.expression()
        
    def expression(self):
        self.optional_sign()
        self.term()
        while self.current_token.recognized_string == '+' or self.current_token.recognized_string == '-':
            self.term()

    def term(self):
        self.factor()
        while self.current_token.recognized_string == '*' or self.current_token.recognized_string == '/':
            self.factor()
    
    def factor(self):
        self.get_token()
        if self.current_token.family == TokenFamily.NUMBER:
            return
        elif self.current_token.family == TokenFamily.IDENTIFIER:
            self.idtail()
        elif self.current_token.recognized_string == '(':
            self.expression()
            self.get_token()
            if self.current_token.recognized_string != ')':
                self.throwError(')')
        

    def relational_oper(self):
        relational_operators = ['=', '<=', '>=', '<>', '<', '>']
        self.get_token()
        if self.current_token.recognized_string not in relational_operators:
            self.throwTypeError(TokenFamily.RELATIONAL_OPERATOR)
            
    def add_oper(self):
        add_operators = ['+', '-']
        self.get_token()
        if self.current_token.recognized_string not in add_operators:
            self.throwError('ADD_OPERATOR')
        
    def mul_oper(self):
        mul_operators = ['*', '/']
        self.get_token()
        if self.current_token.recognized_string not in mul_operators:
            self.throwError('MUL_OPERATOR')
    
    def optional_sign(self):
        next_token = self.tokens[self.token_index+1].recognized_string
        if next_token == '+' or next_token == '-':
            self.add_oper()

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Call should look like 'python syntaxer.py <file_name>'")
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
