########################
# SYNTAKTIKOS ANALYTIS #
########################

# A.M 5064 KOUTOULIS CHRISTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11.7

# O lektikos analytis apotelei to prwto stadio
# eksagei ola ta tokens, anti gia ena ena kai sto deftero stadio
# o syntaktikos analytis ta pairnei ws eisodo
# kai kanei tin syntaktiki analysi
# H ylopoihsh mas einai one-way lektiki se syntaktiki analysh
# kai oxi one-by-one gia kathe token, etsi einai pio grigori
from lexer import Lex, TokenFamily
import sys

class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]

    def __del__(self):
        print("\nLectical and syntactical analysis finished successfully!")
        

    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            return self.current_token
        
    
    def error(self, expected):
        print(f"Syntax Error: Expected {expected}, but got '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)

    def error_type(self, expected):
        print(f"Syntax Error: Expected type '{expected.name}', but got type '{self.current_token.family.name}' at line {self.current_token.line_number}")
        sys.exit(1)

    def analyze(self):
        self.program()


    def program(self):
        if self.current_token.recognized_string != "πρόγραμμα":
            self.error("πρόγραμμα")

        self.next_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_type(TokenFamily.IDENTIFIER)
        self.programblock()

    
    def programblock(self):
        self.declarations()
        self.subprograms()
        self.next_token()
        if self.current_token.recognized_string != "αρχή_προγράμματος":
            self.error("αρχή_προγράμματος")
        self.next_token()
        self.sequence()
        self.next_token()
        if self.current_token.recognized_string != "τέλος_προγράμματος":
            self.error("τέλος_προγράμματος")
    
    def declarations(self):
        self.next_token()
        while self.current_token.recognized_string == "δήλωση":
            self.varlist()
            self.next_token()
            
    def varlist(self):
        self.next_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_type(TokenFamily.IDENTIFIER)
        self.next_token()
        while self.current_token.recognized_string == ",":
            self.next_token()
            if self.current_token.family != TokenFamily.IDENTIFIER:
                self.error_type(TokenFamily.IDENTIFIER)
        
    def subprograms(self):
        self.next_token()
        while self.current_token.family == TokenFamily.KEYWORD:
            if self.current_token.recognized_string == "συνάρτηση":
                self.func()
            elif self.current_token.recognized_string == "διαδικασία":
                self.proc()
            else:
                self.error("συνάρτηση or διαδικασία")

    def func(self):
        self.next_token()
        if self.current_token.recognized_string != "συνάρτηση":
            self.error("συνάρτηση")
        self.next_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_type(TokenFamily.IDENTIFIER)
        self.next_token()
        if self.current_token.recognized_string != "(":
            self.error("(")
        self.next_token()
        self.formalparlist()
        self.next_token()
        if self.current_token.recognized_string != ")":
            self.error(")")
        self.next_token()
        self.funcblock()

    def proc(self):

        self.next_token()
        if self.current_token.recognized_string != "διαδικασία":
            self.error("διαδικασία")
        self.next_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_type(TokenFamily.IDENTIFIER)
        self.next_token()
        if self.current_token.recognized_string != "(":
            self.error("(")
        self.next_token()
        self.formalparlist()
        self.next_token()
        if self.current_token.recognized_string != ")":
            self.error(")")
        self.next_token()
        self.procblock()
            
    def formalparlist(self):
        if self.tokens[self.token_index+1].family == TokenFamily.IDENTIFIER:
            self.varlist()
        
    def funcblock(self):
        self.next_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.error("διαπροσωπεία")
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()
        self.next_token()
        if self.current_token.recognized_string != "αρχή_συνάρτησης":
            self.error("αρχή_συνάρτησης")
        self.sequence()
        self.next_token()
        if self.current_token.recognized_string != "τέλος_συνάρτησης":
            self.error("τέλος_συνάρτησης")
    
    def procblock(self):
        self.next_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            self.error("διαπροσωπεία")
        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()
        self.next_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            self.error("αρχή_διαδικασίας")
        self.sequence()
        self.next_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            self.error("τέλος_διαδικασίας")
    
    def funcinput(self):
        if self.tokens[self.token_index+1].recognized_string == "είσοδος":
            self.next_token()
            self.varlist()

    def funcoutput(self):
        if self.tokens[self.token_index+1].recognized_string == "έξοδος":
            self.next_token()
            self.varlist()

# Main
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Call should look like 'python syntaxer.py <file_name>'")
        print("Exiting...")
        sys.exit(1)

    file_name = sys.argv[1] # invoke file name
    
    # Kataskevi antikeimenou tis klasis lexer kai klisi 
    # tis methodou lektikis analysis gia eksagwgi twn tokens
    lexer = Lex(file_name)
    tokens = lexer.analyze()

    # Kataskevi antikeimenou tis klasis syntaxer kai
    # klisi tis methodou syntaktikis analysis
    syntaxer = Syntax(tokens)
    syntaxer.analyze()
    
    # klisi twn destructors
    del lexer
    del syntaxer