import os
import sys

#Tokens
#characters
DIGITS = "0123456789"
SMALL_LAT_LETTERS = "abcdefghijklmnopqrstuvwxyz"
CAP_LAT_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SMALL_GREEK_LETTERS = "αβγδεζηθικλμνξοπρστυφχψωάέήίϊΐόύϋΰώ"
CAP_GREEK_LETTERS = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΪΌΎΫΏ"

#Arithmitikes prakseis
TOK_PLUS = 500
TOK_MINUS = 501
TOK_MUL = 502
TOK_DIV = 503

#Sxesiakoi telestes
TOK_LESS_THAN = 504
TOK_MORE_THAN = 505
TOK_LESS_THAN_EQUAL = 506
TOK_MORE_THAN_EQUAL = 507
TOK_EQUAL = 508
TOK_NOT_EQUAL = 509

#Anathesi
TOK_ASSIGN = 510

#diaxwristes
TOK_SEMICOLON = 511
TOK_COMMA = 512
TOK_COLON = 513

#Omadopoihsh
TOK_OPEN_PAREN = 514
TOK_CLOSE_PAREN = 515
TOK_OPEN_BRACKET = 516
TOK_CLOSE_BRACKET = 517
TOK_DOUBLE_QUOTE = 518

#Sxolia kai anafora
TOK_COMMENT = 519
TOK_REF = 520  #perasma me anafora

#Desmeumenes lejeis
TOK_PROGR = 521  #programma
TOK_DECLARE = 522  # dilwsi
TOK_IF = 523 #ean
TOK_THEN = 524  #tote
TOK_ELSE = 525  #alliws
TOK_ENDIF = 526 #ean_telos
TOK_REPEAT = 527  #epanalabe
TOK_UNTIL = 528  #mexri
TOK_WHILE = 529  #oso
TOK_ENDWHILE = 530  #oso_telos
TOK_FOR = 531  #gia
TOK_TO = 532  #ews
TOK_STEP = 533  #me_bima
TOK_ENDFOR = 534  #gia_telos
TOK_READ = 535  #diavase
TOK_WRITE = 536  #grapse
TOK_FUNCTION = 537  #synartisi
TOK_PROCEDURE = 538  # diadikasia
TOK_INTERFACE = 539  #diaproswpeia
TOK_INPUT = 540  #eisodos
TOK_OUTPUT = 541  #eksodos
TOK_FUNCTION_BEGIN = 542  #arxi_synartisis
TOK_FUNCTION_END = 543  #telos_synartisis
TOK_PROCEDURE_BEGIN = 544  #arxi_diadikasias
TOK_PROCEDURE_END = 545  #telos_diadikasias
TOK_PROG_BEGIN = 546  #arxi_programmatos
TOK_PROG_END = 547  #telos_programmatos
TOK_EXECUTE = 548  #ektelese
#logikoi telestes
TOK_AND = 549  # kai
TOK_OR = 550  # h
TOK_NOT = 551  # oxi
TOK_ERROR = 552 
TOK_EOF=553
TOK_ID=554
TOK_GROUP=555

E1=-1 #RECOGNISE DESMEUMENI LEJI

E2=-2 #AKERAIOS

#END Tokens


class Token:
#pedia : recognized_string , family , line_number
    def __init__(self, recognized_string, family, line_number):
        self.recognized_string = recognized_string
        self.family = family
        self.line_number = line_number

    def __str__(self):
        if self.recognized_string:
            return f'{self.recognized_string} family:"{self.family}", line: {self.line_number}'
        return f'family:"{self.family}", line: {self.line_number}'


class Lex:
    def __init__(self, token ,file_name):
        self.token=token
        self.file_name=file_name
        self.current_char=None
        self.current_line=1
        
    def lex(self):
        recognized_string=''
        token.family=''
        pinakas=[[0,1,2,TT_PLUS,TT_MINUS,TT_MUL,3,TT_MOD,TT_LPAREN,TT_ERROR,TT_RBRACKET,TT_ERROR,TT_COMMA,TT_COLON,4,5,6,7,8,TT_EOF,TT_ERROR],
		         [E2,1,TT_ERROR,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2],
		         [E1,2,2,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1],
		         [TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_DIV,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR],
		         [TT_ERROR,TT_ERROR,2,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_LBRACKET,TT_RBRACKET,TT_ERROR,TT_ERROR,TT_COMMENT,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR],
		         [TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_EQUALS,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN,TT_ASSIGN],
		         [TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_EQUAL,TT_LESS_THAN,TT_LESS_THAN,TT_LESS_THAN],
		         [TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_EQUAL,TT_MORE_THAN,TT_MORE_THAN,TT_MORE_THAN],
		         [TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_NOT_EQUAL,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR,TT_ERROR]]
        putIn=0
        state=0   
        try:                   
            while state>=0 and state<100:
                self.current_char=f1.read(1)
                if self.current_char in ' \t' :
                    putIn=0
                    family='whitespace'
                elif self.current_char=='\n':
                    putIn=0
                    family=''
                elif self.current_char in DIGITS:
                    putIn=1
                    family='number'
                elif self.current_char in CAP_LETTERS:
                    putIn=2
                elif self.current_char in LOW_LETTERS:
                    putIn=2
                elif self.current_char=='+':
                    putIn=3
                    family='addOperator'
                elif self.current_char=='-':
                    putIn=4
                    family='addOperator'
                elif self.current_char=='*':
                    putIn=5
                    family='mulOperator'
                elif self.current_char=='/':
                    putIn=6
                    family='mulOperator'
                elif self.current_char=='%':
                    putIn=7
                    family='mulOperator'
                elif self.current_char=='(':
                    putIn=8
                    family='groupSymbol'
                elif self.current_char==')':
                    putIn=9
                    family='groupSymbol'
                elif self.current_char=='{':
                    putIn=10
                    family='groupSymbol'
                elif self.current_char=='}':
                    putIn=11
                    family='groupSymbol'
                elif self.current_char==',':
                    putIn=12
                    family='delimiter'
                elif self.current_char==':':
                    putIn=13
                    family='delimiter'
                elif self.current_char=='#':
                    putIn=14
                elif self.current_char=='=':
                    putIn=15
                elif self.current_char=='<':
                    putIn=16
                elif self.current_char=='>':
                    putIn=17
                elif self.current_char=='!':
                    putIn=18
                elif not self.current_char:
                    putIn=19
                else:
                    putIn=20

                recognized_string+=self.current_char
                    
                state=pinakas[state][putIn]

            if (state == TT_LESS_THAN or state == TT_MORE_THAN or state == E1 or state == E2 or state == TT_ASSIGN):
                recognized_string=recognized_string[:-1]  # Remove the last character
                current_position=f1.tell()
                if (current_position>1): f1.seek(current_position-1)# Move the file pointer back by one character

            for c in recognized_string:
                if c=='\n':
                    self.current_line+=1
                
            if state>=100:
                if (state==TT_COMMENT):
                    family='comment'
                if (state==TT_ASSIGN):
                    family='assignment'
                if (state==TT_LESS_THAN or state==TT_MORE_THAN or state==TT_EQUALS or state==TT_LESS_EQUAL or state==TT_MORE_EQUAL or state==TT_NOT_EQUAL):
                    family='relOperator'
            elif state==E1:
                if 'main' in recognized_string:
                    recognized_string='main'
                    family='keyword'
                elif 'elif' in recognized_string:
                    recognized_string='elif'
                    family='keyword'
                elif 'while' in recognized_string:
                    recognized_string='while'
                    family='keyword'
                elif 'print' in recognized_string:
                    recognized_string='print'
                    family='keyword'
                elif 'return' in recognized_string:
                    recognized_string='return'
                    family='keyword'
                elif 'input' in recognized_string:
                    recognized_string='input'
                    family='keyword'
                elif 'and' in recognized_string:
                    recognized_string='and'
                    family='keyword'
                elif '#def' in recognized_string:
                    recognized_string='#def'
                    family='keyword'
                elif 'global' in recognized_string:
                    recognized_string='global'
                    family='keyword'
                elif 'if' in recognized_string:
                    recognized_string='if'
                    family='keyword'
                elif '#int' in recognized_string:
                    recognized_string='#int'
                    family='keyword'
                elif 'or' in recognized_string:
                    recognized_string='or'
                    family='keyword'
                elif 'else' in recognized_string:
                    recognized_string='else'
                    family='keyword'
                elif 'not' in recognized_string:
                    recognized_string='not'
                    family='keyword'
                elif 'def' in recognized_string:
                    recognized_string='def'
                    family='keyword'
                elif 'int' in recognized_string:
                    recognized_string='int'
                    family='keyword'
                else:
                    recognized_string = recognized_string.replace(" ", "").replace("\t", "").replace("\n", "")
                    family='identifier'
            elif state==E2:
                family='number'
            return Token(recognized_string,family,self.current_line)

        except FileNotFoundError:
            raise LexicalError(f"File '{self.file_name}' not found")
        except IOError as e:
            raise LexicalError(f"Error reading file: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lex.py <file_name>")
        sys.exit(1)

    file_name = sys.argv[1]
    try:
        with open(file_name, 'r', encoding="utf-8") as f1:
            token = Token("", "", 1)
            lexer = Lex(token, file_name)
            while True:
                token = lexer.lex()
                if token.type == TOK_EOF:
                    break
                print(token)
    except FileNotFoundError:
        print(f"File {file_name} not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)
