import os
import sys

#Tokens
#characters
DIGITS = "0123456789"
SMALL_LAT_LETTERS = "abcdefghijklmnopqrstuvwxyz"
CAP_LAT_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
SMALL_GREEK_LETTERS = "αβγδεζηθικλμνξοπρσςτυφχψωάέήίϊΐόύϋΰώ"
CAP_GREEK_LETTERS = "ΑΒΓΔΕΖΗΘΙΚΛΜΝΞΟΠΡΣΤΥΦΧΨΩΆΈΉΊΪΌΎΫΏ_"

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
        trans_diagram= [ [0, 1, 2, TOK_PLUS, TOK_MINUS, TOK_MUL, TOK_DIV, TOK_EQUAL, 3, 4, 5, 6, TOK_ERROR, TOK_SEMICOLON, TOK_COMMA, TOK_OPEN_PAREN, TOK_CLOSE_PAREN, TOK_OPEN_BRACKET, TOK_CLOSE_BRACKET, TOK_DOUBLE_QUOTE, TOK_REF, TOK_EOF, TOK_ERROR]
                        ,[E1, 1, 1, E1, E1 , E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1, E1]
                        ,[E2, TOK_ERROR, 2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2, E2]
                        ,[ TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN_EQUAL,TOK_LESS_THAN, TOK_NOT_EQUAL, TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN,TOK_LESS_THAN]
                        ,[ TOK_MORE_THAN,  TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN_EQUAL, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN, TOK_MORE_THAN]
                        ,[TOK_ERROR, TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ASSIGN, TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR,TOK_ERROR]
                        ,[6,6,6,6,6,6,6,6,6,6,6,6,0,6,6,6,6,6,6,6,6,TOK_ERROR,6] 
        ]
        state=0 
        input_cat=0
        try:                   
            while state>=0 and state<500:
                self.current_char=f1.read(1)
                if self.current_char in ' \t' :
                    input_cat=0
                    family='whitespace'
                elif self.current_char=='\n':
                    input_cat=0
                    family=''
                elif self.current_char in SMALL_LAT_LETTERS:
                    input_cat=1
                elif self.current_char in SMALL_GREEK_LETTERS:
                    input_cat=1
                elif self.current_char in CAP_GREEK_LETTERS:
                    input_cat=1
                elif self.current_char in CAP_LAT_LETTERS:
                    input_cat=1
                elif self.current_char in DIGITS:
                    input_cat=2
                    family='number'
                elif self.current_char=='+':
                    input_cat=3
                    family='arithmeticOperator'
                elif self.current_char=='-':
                    input_cat=4
                    family='arithmeticOperator'
                elif self.current_char=='*':
                    input_cat=5
                    family='arithmeticOperator'
                elif self.current_char=='/':
                    input_cat=6
                    family='arithmeticOperator'
                elif self.current_char=='=':
                    input_cat=7
                    family='comparisonOperator'
                elif self.current_char=='<':
                    input_cat=8
                elif self.current_char=='>':
                    input_cat=9
                elif self.current_char==':':
                    input_cat=10
                elif self.current_char=='{':
                    input_cat=11
                elif self.current_char=='}':
                    input_cat=12
                elif self.current_char==';':
                    input_cat=13
                    family='delimiter'
                elif self.current_char==',':
                    input_cat=14
                    family='delimiter'
                elif self.current_char=='(':
                    input_cat=15
                    family='groupSymbol'
                elif self.current_char==')':
                    input_cat=16
                    family='groupSymbol'
                elif self.current_char=='[':
                    input_cat=17
                    family='groupSymbol'
                elif self.current_char==']':
                    input_cat=18
                    family='groupSymbol'
                elif self.current_char=='"':
                    input_cat=19
                    family='quote'
                elif self.current_char=='%':
                    input_cat=20
                    family='passbyReference'
                elif not self.current_char:
                    input_cat=21
                else:
                    input_cat=22

                recognized_string+=self.current_char
                    
                state=trans_diagram[state][input_cat]

            if (state == TOK_LESS_THAN or state == TOK_MORE_THAN or state == E1 or state == E2 or state == TOK_ASSIGN):
                recognized_string=recognized_string[:-1]  # Remove the last character
                current_position=f1.tell()
                if (current_position>1): f1.seek(current_position-1)# Move the file pointer back by one character

            for c in recognized_string:
                if c=='\n':
                    self.current_line+=1
                
            if state>=500:
                if (state==TOK_ASSIGN):
                    family='assignment'
                if (state==TOK_LESS_THAN or state==TOK_MORE_THAN or state==TOK_EQUAL or state==TOK_LESS_THAN_EQUAL or state==TOK_MORE_THAN_EQUAL or state==TOK_NOT_EQUAL):
                    family='relOperator'
            elif state==E1:
                if 'πρόγραμμα' in recognized_string:
                    recognized_string='πρόγραμμα'
                    family='keyword'
                elif 'δήλωση' in recognized_string:
                    recognized_string='δήλωση'
                    family='keyword'
                elif 'εάν' in recognized_string:
                    recognized_string='εάν'
                    family='keyword'
                elif 'τότε' in recognized_string:
                    recognized_string='τότε'
                    family='keyword'
                elif 'αλλιώς' in recognized_string:
                    recognized_string='αλλιώς'
                    family='keyword'
                elif 'εάν_τέλος' in recognized_string:
                    recognized_string='εάν_τέλος'
                    family='keyword'
                elif 'επανάλαβε' in recognized_string:
                    recognized_string='επανάλαβε'
                    family='keyword'
                elif 'μέχρι' in recognized_string:
                    recognized_string='μέχρι'
                    family='keyword'
                elif 'όσο' in recognized_string:
                    recognized_string='όσο'
                    family='keyword'
                elif 'όσο_τέλος' in recognized_string:
                    recognized_string='όσο_τέλος'
                    family='keyword'
                elif 'για' in recognized_string:
                    recognized_string='για'
                    family='keyword'
                elif 'εώς' in recognized_string:
                    recognized_string='εώς'
                    family='keyword'
                elif 'με_βήμα' in recognized_string:
                    recognized_string='με_βήμα'
                    family='keyword'
                elif 'για_τέλος' in recognized_string:
                    recognized_string='για_τέλος'
                    family='keyword'
                elif 'διάβασε' in recognized_string:
                    recognized_string='διάβασε'
                    family='keyword'
                elif 'γράψε' in recognized_string:
                    recognized_string='γράψε'
                    family='keyword'
                elif 'συνάρτηση' in recognized_string:
                    recognized_string='συνάρτηση'
                    family='keyword'
                elif 'διαδικασία' in recognized_string:
                    recognized_string='διαδικασία'
                    family='keyword'
                elif 'διαπροσωπεία' in recognized_string:
                    recognized_string='διαπροσωπεία'
                    family='keyword'
                elif 'είσοδος' in recognized_string:
                    recognized_string='είσοδος'
                    family='keyword'    
                elif 'έξοδος' in recognized_string:
                    recognized_string='έξοδος'
                    family='keyword'
                elif 'αρχή_συνάρτησης' in recognized_string:
                    recognized_string='αρχή_συνάρτησης'
                    family='keyword'
                elif 'τέλος_συνάρτησης' in recognized_string:
                    recognized_string='τέλος_συνάρτησης'
                    family='keyword'
                elif 'αρχή_διαδικασίας' in recognized_string:
                    recognized_string='αρχή_διαδικασίας'
                    family='keyword'
                elif 'τέλος_διαδικασίας' in recognized_string:
                    recognized_string='τέλος_διαδικασίας'
                    family='keyword'
                elif 'ή' in recognized_string:
                    recognized_string='ή'
                    family='keyword'
                elif 'και' in recognized_string:
                    recognized_string='και'
                    family='keyword'
                elif 'όχι' in recognized_string:
                    recognized_string='όχι'
                    family='keyword'
                elif 'in' in recognized_string:
                    recognized_string='in'
                    family='keyword'
                elif 'inout' in recognized_string:
                    recognized_string='inout'
                    family='keyword'
                elif 'αρχή_προγράμματος' in recognized_string:
                    recognized_string='αρχή_προγράμματος'
                    family='keyword'
                elif 'τέλος_προγράμματος' in recognized_string:
                    recognized_string='τέλος_προγράμματος'
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
        with open(file_name, 'r', encoding='utf-8') as f1:
            token = Token("", "", 1)
            lexer = Lex(token, file_name)
            while True:
                
                token = lexer.lex()
                if token.family == 'n':
                    break
                print(token)
    except FileNotFoundError:
                    print(f"File '{file_name}' not found")
    except IOError as e:
        print(f"Error reading file: {e}")
