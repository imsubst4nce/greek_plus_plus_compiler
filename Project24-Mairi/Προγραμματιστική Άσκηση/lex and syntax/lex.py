import os
import sys #gia na mporesoume na diavasoume to file apo to command line

#TOKENS
DIGITS='0123456789'
CAP_LETTERS='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LOW_LETTERS='abcdefghijklmnopqrstuvwxyz'
TT_PLUS =100
TT_MINUS =101
TT_MUL=102
TT_DIV=103
TT_MOD=104
TT_LESS_THAN=105
TT_MORE_THAN=106
TT_EQUALS=107
TT_LESS_EQUAL=108
TT_MORE_EQUAL=109
TT_NOT_EQUAL=110
TT_ASSIGN=111
TT_COMMA=112
TT_COLON=113
TT_LPAREN=114
TT_RPAREN=115
TT_LBRACKET=116 
TT_RBRACKET=117
TT_COMMENT=118
TT_MAIN=119
INT_DECLARE=120 #einai to #int
TT_IF=121
TT_WHILE=122
TT_PRINT=123
TT_RETURN=124
TT_INPUT=125
TT_AND=126
TT_DEF=127
TT_GLOBAL=128
TT_ELIF=129
TT_INT=130
TT_OR=131
TT_DEFINE=132 #einai to #def
TT_ELSE=133
TT_NOT=134
TT_ERROR=135
TT_EOF=136
E1=-1 #ANAGNWRISTIKO/DESMEUMEMH LEKSH
E2=-2 #AKERAIA STATHERA
TT_GROUP=139
TT_ID=140


class Token:
#properties : recognized_string , family , line_number
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
        
global lex_out
lex_out=0

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_name>")
        sys.exit(1)

    global file_name
    file_name=sys.argv[1]
    global f1
    f1=open(file_name,'r')
    string=''
    family=''
    token = Token("", "",1)
    lexer = Lex(token, file_name)
    token=lexer.lex()
    #print(lex_out)
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)
    token=lexer.lex()
    print(token)

