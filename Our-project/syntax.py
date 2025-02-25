########################
# SYNTAKTIKOS ANALYTIS #
########################

# A.M 5064 KOUTOULIS XRHSTOS
# A.M 5108 KOUTSONIKOLIS NIKOLAOS
# PYTHON VERSION: 3.11

import lex_v2 as lex

class Syntax:
    def __init__(self, file_name):
        self.file_name = file_name
        

# Main function
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    syntax_analyzer = Syntax(file_name)
    syntax_analyzer.analyze()