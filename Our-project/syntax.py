from lex_v2 import Lex, TokenFamily
import sys

class Syntax:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token_index = 0
        self.current_token = self.tokens[self.token_index]
        

    def next_token(self):
        self.token_index += 1
        if self.token_index < len(self.tokens):
            self.current_token = self.tokens[self.token_index]
            return self.current_token
        return None
    
    def error(self, expected):
        print(f"Syntax Error: Expected {expected}, but got '{self.current_token.recognized_string}' at line {self.current_token.line_number}")
        sys.exit(1)

    def error_type(self, expected):
        print(f"Syntax Error: Expected type '{expected.name}', but got type '{self.current_token.family.name}' at line {self.current_token.line_number}")
        sys.exit(1)

    def analyse(self):
        self.program()


    def program(self):
        if self.current_token.recognized_string != "πρόγραμμα":
            self.error("πρόγραμμα")

        self.next_token()
        if self.current_token.family != TokenFamily.IDENTIFIER:
            self.error_type(TokenFamily.IDENTIFIER)

        self.programblock()


# Main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python syntax.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    lexer = Lex(file_name)
    tokens = lexer.analyze()

    syntaxer= Syntax(tokens)
    syntaxer.analyse()
    del lexer # kaloume ton destructor
    del syntaxer 