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

##____________TOKEN____________
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

##____________LEX____________
class Lex:
    def __init__(self, token ,file_name):
        self.token=token
        self.file_name=file_name
        self.current_char=None
        self.current_line=1
        
    def lex(self):
        recognized_string=''
        family=''
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
        times=0                  
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
                family='delimiters'
            elif self.current_char==':':
                putIn=13
                family='delimiters'
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
                family='Error:EOF'
            else:
                putIn=20
                family='Error:Invalid Char'
            recognized_string+=self.current_char
                
            state=pinakas[state][putIn]
            

        recognized_string=recognized_string[0:31] ##only take into consideration the first 30 letters
            

        if (state == TT_LESS_THAN or state == TT_MORE_THAN or state == E1 or state == E2 or state == TT_ASSIGN):
            recognized_string=recognized_string[:-1]  
            current_position=f1.tell()
            if (current_position>1): f1.seek(current_position-1)
            
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
            if state==TT_ERROR:
                family='Error'
        elif state==E1:
            recognized_string=recognized_string.strip()
            if recognized_string in ('main','if','while','print','return','input','and','#def','global','elif','#int','or','else','not','def','int'):
                family='keyword'
            else:
                recognized_string = recognized_string.replace(" ", "").replace("\t", "").replace("\n", "")
                family='identifier'
        elif state==E2:
            if int(recognized_string)<-32767 or int(recognized_string)>32767:
                family='Error: invalid number'
            else:
                family='number'
        
        
        return Token(recognized_string,family,self.current_line)

##____________SYNTAX____________
class Syntax:
    def __init__(self, lexer, token):
        self.lexer=Lex(token,file_name)
        self.current_token=token

    def get_token(self):
        self.current_token=self.lexer.lex()

    def syntax_analyzer(self):
        global token
        self.current_token=self.get_token()
        self.startRule()
        print("No errors found; successful compilation")

    def error(message):
        global token
        print(message + " on line: " + self.current_token.line_number)

    def startRule(self):
        self.def_main_part()
        self.call_main_part()

    def def_main_part(self):
        result=self.def_main_function()
        if not result:
            self.error('Error: def_main_function not found on structure')

    def def_main_function(self):
        self.declarations()
        result=self.def_function()
        while result:
            result=self.def_function()
        self.statements() 
        
    def def_function(self):
        #global token
        if self.current_token.recognized_string=='def':
            self.current_token=self.get_token()
            if self.current_token.family=='identifier':
                self.current_token=self.get_token()
                if self.current_token.recognized_string=='(':
                    self.current_token=self.get_token()
                    self.id_list()
                    if self.current_token.recognized_string==')':
                        self.current_token=self.get_token()
                        if self.current_token.recognized_string==':':
                            self.current_token=self.get_token()
                            if self.current_token.recognized_string=='#{':
                                self.declarations()
                                result=self.def_function()
                                while result:
                                    result=self.def_function()
                                self.statements()
                                if self.current_token.recognized_string=='#}':
                                    self.current_token=self.get_token()
                                else:
                                    self.error("Error: missing '#}', function never closes")
                            else:
                                self.error("Error: missing '#{', function never opens")
                        else:
                            self.error("Error: missing ':' after function's ID")
                    else:
                        self.error("Error: missing ')', ID list never closes")
                else:
                    self.error("Error: missing '(' after ID")
            else:
                self.error("Error: function misses ID")   
            
    def declarations(self):
        result=self.declaration_line()
        while result:
            result=self.declaration_line()

    def declaration_line(self):
        #global token
        self.current_token=self.get_token()
        if self.current_token.recognized_string=='#int' or self.current_token.recognized_string=='global':
            self.current_token=self.get_token()
            self.id_list()
        else:
            self.error("Error: missing '#int' before declarations")

    def statement(self):
        #global token
        if (self.current_token.family=='identifier') or (self.current_token.recognized_string=='print') or (self.current_token.recognized_string=='return'):
            self.simple_statement()
        elif (self.current_token.recognized_string=='if') or (self.current_token.recognized_string=='while'):
            self.structured_statement()
        else:
            self.error("Error: unrecognized type of statement")
            
    def statements(self):
        result=self.statement()
        if not statement:
            self.error("Error: no statements found")

    def simple_statement(self):
        #global token
        if self.current_token.family=='identifier':
            self.current_token=self.get_token()
            self.assignment_stat()
        elif self.current_token.recognized_string=='print':
            self.current_token=self.get_token()
            self.print_stat()
        elif self.current_token.recognized_string=='return':
            self.return_stat()
        else:
            self.error("Error: no known keywords found for simple statements")

    def structured_statement(self):
        #global token
        if self.current_token.family=='if':
            token=self.get_token()
            self.if_stat()
        elif self.current_token.recognized_string=='while':
            self.current_token=self.get_token()
            self.while_stat()

    def assignment_stat(self):
        #global token
        if self.current_token.recognized_string=='=':
            self.current_token=self.get_token()
            if (self.current_token.recognized_string=='int'):
                self.current_token=self.get_token()
                if (self.current_token.recognized_string=='('):
                    self.current_token=self.get_token()
                    if (self.current_token.recognized_string=='input'):
                        self.current_token=self.get_token()
                        if (self.current_token.recognized_string=='('):
                            self.current_token=self.get_token()
                            if (self.current_token.recognized_string==')'):
                                self.current_token=self.get_token()
                                if self.current_token.recognized_string==')':
                                    self.current_token=self.get_token()
                                else:
                                    self.error("Error: ')' not found when closing int()")
                            else:
                                self.error("Error: ')' not found when closing input()")
                        else:
                            self.error("Error: '(' not found when opening input()")
                    else:
                        self.error("Error: 'input()' not found when using int()")
                else:
                    self.error("Error: '(' when opening int()")
            else:
                self.expression()
        else:
            self.error("Error: '=' not found on ID assignment")
        
    def print_stat(self):
        #global token
        if self.current_token.recognized_string=='(':
            self.current_token=self.get_token()
            self.expression()
            if self.current_token.recognized_string==')':
                self.current_token=self.get_token()
            else:
                self.error("Error: ')' not found when closing the print()")
        else:
            self.error("Error: ')' not found when closing the print()")

    def return_stat(self):
        #global token
        self.current_token=self.get_token()
        self.expression()

    def if_stat(self):
        #global token
        if self.current_token.recognized_string=='if':
            self.current_token=self.get_token()
            self.condition()
            if self.current_token.recognized_string==':':
                self.current_token=self.get_token()
                self.statements()
                if self.current_token.recognized_string=='elif':
                    self.current_token=self.get_token()
                    if self.current_token.recognized_string==':':
                        self.current_token=self.get_token()
                        self.statements()
                        if self.current_token.recognized_string=='else':
                            self.current_token=self.get_token()
                            if self.current_token.recognized_string==':':
                                self.current_token=self.get_token()
                                self.statements()
                            else:
                                self.error("Error: ':' not found when opening else statement")
                    else:
                        self.error("Error: ':' not found when opening elif statement")
            else:
                self.error("Error: ':' not found when opening if statement")

                    
    def while_stat(self):
        #global token
        if self.current_token.recognized_string=='while':
            self.current_token=self.get_token()
            self.condition()
            if self.current_token.recognized_string==':':
                self.current_token=self.get_token()
                self.statements()
            else:
                self.error("Error: ':' not found when opening while statement")

    def id_list(self):
        #global token
        if self.current_token.family=='identifier':
            self.current_token=self.get_token()
            while self.current_token.recognized_string==',':
                self.current_token=self.get_token()
                if self.current_token.family=='identifier':
                    self.current_token=self.get_token()
                else:
                    self.error("Error: no ID found after ','")

    def expression(self):
        #global token
        self.term()
        while (self.current_token.family=='addOperator'):
            self.term()
                
    def term(self):
        global token
        if self.current_token.family=='number' or self.current_token.recognized_string=='(' or self.current_token.family=='identifier':
            self.factor()
            while self.current_token.family=='mulOperator':
                self.factor()

    def factor(self):
        #global token
        if self.current_token.family=='number':
            self.current_token=self.get_token()
        if self.current_token.recognized_string=='(':
            self.current_token=self.get_token()
            self.expression()
            if self.current_token.recognized_string==')':
                self.current_token=self.get_token()
            else:
                self.error("Error: ')' not found when closing the expression")
        elif self.current_token.family=='identifier':
            self.idtail()
        else:
            self.error("Error: unrecognized factor")

    def idtail(self):
        #global token
        if (self.current_token.recognized_string=='('):
            self.actual_par_list()
            if (self.current_token.recognized_string==')'):
                self.current_token=self.get_token()
            else:
                self.error("Error: ')' not found when closing the id tail")
        else:
            self.get_token()

    def actual_par_list(self):
        #global token
        self.expression()
        while self.current_token.recognized_string==',':
            self.expression()

    def condition(self):
        #global token
        self.bool_term()
        while self.current_token.recognized_string=='or':
            self.current_token=self.get_token()
            self.bool_term()

    def bool_term(self):
        #global token
        self.bool_factor()
        while self.current_token.recognized_string=='and':
            self.current_token=self.get_token()
            self.bool_factor()

    def bool_factor(self):
        #global token
        if self.current_token.recognized_string=='not':
            self.current_token=self.get_token()
            self.condition()
        elif self.current_token.family=='addOperator' or self.current_token.family=='number' or self.current_token.recognized_string=='(' or self.current_token.family=='identifier':
            self.expression()
            if self.current_token.family=='relOperator':
                self.current_token=self.get_token()
                self.expression()
        else:
            self.condition()
            
        
    def call_main_part(self):
        main_function_call()

    def main_function_call(self):
        #global token
        if self.current_token.recognized_string=='#def':
            self.current_token=self.get_token()
            if self.current_token.recognized=='main':
                self.current_token=self.get_token()

## AYTH EINAI H MAIN MAS!!!! ##

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_name>")
        sys.exit(1)

    global file_name
    file_name=sys.argv[1]
    global f1
    f1=open(file_name,'r')
    token = Token("", "",1)
    lexer = Lex(token, file_name)
    parser = Syntax(lexer,token)
    parser.syntax_analyzer()

## EDW TELEIWNEI H MAIN MAS :( ##

    
