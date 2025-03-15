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

            #to ebala gia na testarw pio token diabazw 
            print(self.current_token)
            return self.current_token
        
    def next_token(self):
        if self.token_index + 1 < len(self.tokens):
            return self.tokens[self.token_index + 1]
        return None

    def previous_token(self):
        self.token_index -= 1
        self.current_token = self.tokens[self.token_index]
        print(self.current_token)
        return self.current_token

    def throwInvalidError(self):
        print(f"Syntax Error: Got invalid phrase '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)
    
    def throwError(self, expected):
        print(f"Syntax Error: Expected '{expected}', but got '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
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

    def program(self):
        print(self.current_token)
        if self.current_token.recognized_string != "πρόγραμμα":
            self.throwError("πρόγραμμα")
        
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        self.programblock()
        
    def programblock(self):
        self.declarations()
        self.subprograms()
        ### continue with arxi programmatos

    def declarations(self):
        
        if self.next_token().recognized_string != "δήλωση":
            return
        while self.next_token().recognized_string == "δήλωση":
            self.get_token()
            self.varlist()

    def varlist(self):

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)
        while self.next_token().recognized_string == ',':
            self.get_token()

            self.varlist()
       
        
    def subprograms(self):
        while self.next_token().recognized_string == "συνάρτηση":
            self.func()
        while self.next_token().recognized_string == "διαδικασία":
            self.proc()

    def func(self):
        self.get_token()
        if self.current_token.recognized_string != "συνάρτηση":
            throwError("συνάρτηση")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwError("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwError(")")

        self.funcblock()


    def proc(self):
        self.get_token()
        if self.current_token.recognized_string != "διαδικασία":
            throwError("διαδικασία")

        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        self.get_token()
        if self.current_token.recognized_string != "(":
            self.throwError("(")

        self.formalparlist()

        self.get_token()
        if self.current_token.recognized_string != ")":
            self.throwError(")")

        self.procblock()

    def formalparlist(self):
        if self.next_token().recognized_string == ")":
            return
        self.varlist()

    def funcblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            throwError("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_συνάρτησης":
            throwError("αρχή_συνάρτησης")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_συνάρτησης":
            throwError("τέλος_συνάρτησης")


        
    def procblock(self):
        self.get_token()
        if self.current_token.recognized_string != "διαπροσωπεία":
            throwError("διαπροσωπεία")

        self.funcinput()
        self.funcoutput()
        self.declarations()
        self.subprograms()

        self.get_token()
        if self.current_token.recognized_string != "αρχή_διαδικασίας":
            throwError("αρχή_διαδικασίας")

        self.sequence()

        self.get_token()
        if self.current_token.recognized_string != "τέλος_διαδικασίας":
            throwError("τέλος_διαδικασίας")

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
        
        if self.next_token().family==TokenFamily.IDENTIFIER:
            self.assignment_stat()
        
        if self.next_token().recognized_string=="εάν":
            self.if_stat()
        elif self.next_token().recognized_string=="όσο":
            self.while_stat()
        elif self.next_token().recognized_string=="επανάλαβε":
            self.do_stat()
        elif self.next_token().recognized_string=="για":
            self.for_stat()
        elif self.next_token().recognized_string=="διάβασε":
            self.input_stat()
        elif self.next_token().recognized_string=="γράψε":
            self.print_stat()
        elif self.next_token().recognized_string=="εκτέλεσε":
            self.call_stat()
        else:
            self.get_token()
            self.throwInvalidError()


    def assignment_stat(self):
        self.get_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.throwTypeError(TokenFamily.IDENTIFIER)

        self.get_token()
        if self.current_token.family!= TokenFamily.ASSIGNMENT:
            self.throwError(":=")

        self.expression()

    def if_stat(self):
        self.get_token()
        if self.current_token.recognized_string!="εάν":
            self.throwError("εάν")

        self.condition()
        ##continue


    def idtail(self):
        if self.next_token().recognized_string == "(":
            self.actualpars()

    def actualpars(self):
        self.get_token()
        if self.current_token.recognized_string!="(":
            self.throwError("(")
        self.actualparlist()
        self.get_token()
        if self.current_token.recognized_string!=")":
            self.throwError(")")


    def actualparlist(self):
        if self.next_token().recognized_string==")":
            return
        self.actualparitem()
        while self.next_token().recognized_string==",":
            self.get_token()
            self.actualparitem()

    def actualparitem(self):
        if self.next_token().family==TokenFamily.PASSBYREFERENCE:
            self.get_token()

            self.get_token()
            if self.current_token.family!=TokenFamily.NUMBER:
                throwTypeError(TokenFamily.NUMBER)
            return
        else: self.expression()


    def condition(self):
        self.boolterm()
        while self.next_token().recognized_string=="ή":
            self.get_token()
            self.boolterm()

    def boolterm(self):
        self.boolfactor()
        while self.next_token().recognized_string=="και":
            self.get_token()
            self.boolfactor()

    def boolfactor(self):
        if (self.next_token().recognized_string != "όχι") and (self.next_token().recognized_string != "["):
            self.expression()
            self.relational_oper()
            self.expression()

        elif self.next_token().recognized_string == "όχι":
            self.get_token()

        self.get_token()
        if self.next_token().recognized_string=="[":
            self.condition()



    def expression(self):
        self.optional_sign()
        self.term()
        while (self.next_token().recognized_string=="+") or (self.next_token().recognized_string=="-"):
            self.add_oper()
            self.term()

    def term(self):
        self.factor()
        while (self.next_token().recognized_string=="*") or (self.next_token().recognized_string=="/"):
            self.mul_oper()
            self.factor()

    def factor(self):
        self.get_token()
        if self.current_token.family == TokenFamily.NUMBER:
            return
        elif self.current_token.recognized_string=="(":
            self.expression()
            self.get_token()
            if self.current_token.recognized_string!=")":
                self.throwError(")")  
        elif self.current_token.family==TokenFamily.IDENTIFIER:
            self.get_token()
            self.idtail()
        else:
            self.throwInvalidError("ID or (Expression) or NUMBER")

    def relational_oper():
        self.get_token()
        if self.current_token.family!=TokenFamily.RELATIONAL_OPERATOR:
            throwTypeError(TokenFamily.RELATIONAL_OPERATOR)


    def add_oper(self):
        self.get_token()
        if (self.next_token().recognized_string!="+") and (self.next_token().recognized_string!="-"):
            throwError("+ or -")

    def mul_oper(self):
        self.get_token()
        if (self.next_token().recognized_string!="*") and (self.next_token().recognized_string!="/"):
            throwError("* or /")

    def optional_sign(self):
        if (self.next_token().recognized_string=="+") or (self.next_token().recognized_string=="-"):
            self.add_oper()
        else: print("no sign")


        






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
