##ZACHRA ELISAVET ALLA GKAMPOU, 5052
##MARIA KATOLI, 5083

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
        in_comment=False
        pinakas=[[0,1,2,TT_PLUS,TT_MINUS,TT_MUL,3,TT_MOD,TT_LPAREN,TT_RPAREN,TT_LBRACKET,TT_RBRACKET,TT_COMMA,TT_COLON,4,5,6,7,8,TT_EOF,TT_ERROR],
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
        while state>=0 and state<100 and file_name:
            self.current_char=f1.read(1)

            if self.current_char=='#' and not in_comment:
                next_char=f1.read(1)
                if next_char=='#':
                    in_comment=True
                    recognized_string=''
                    continue
                else:
                    f1.seek(f1.tell()-1)


            if in_comment:
                if self.current_char=='#':
                    next_char=f1.read(1)
                    if next_char=='#':
                        in_comment=False
                    continue
                else:
                    continue
                
            if not self.current_char:
                f1.close()
                break
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
            if (current_position>1):
                f1.seek(current_position-1)
                current_position=f1.tell()
            
        for c in recognized_string:
            if c=='\n':
                self.current_line+=1
                
        recognized_string=recognized_string.strip()
        
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
            if recognized_string in ('main','if','while','print','return','input','and','#def','global','elif','#int','or','else','not','def','int'):
                family='keyword'
            else:
                family='identifier'
        elif state==E2:
            if int(recognized_string)<-32767 or int(recognized_string)>32767:
                family='Error: invalid number'
            else:
                family='number'
        
        
        return Token(recognized_string,family,self.current_line)

##____________SYNTAX____________

global tmpVarCount ##na krataei poses proswrines metavlhtes exoume
tmpVarCount=0
global tmpVarList
tmpVarList=[]

class cond: ##na krataei tis listes twn labels gia true/false otan elegxoume ta conditions sta while kai if 
    def __init__(self, true, false):
        self.true=true
        self.false=false

    def __str__(self):
        return f'{self.true},{self.false}'

class Syntax:
    def __init__(self, lexer, generated_program, symbolTable):
        self.lexer=Lex(token,file_name)
        self.generated_program=generated_program
        self.symbolTable=symbolTable
        self.current_token=None

    def newTemp(self):
        global tmpVarCount,tmpVarList
        s="T_" + str(tmpVarCount)
        tmpVarCount=tmpVarCount+1
        tmpVarList.append(s)
        return s
        
    def get_token(self):
        self.current_token=self.lexer.lex()
        return self.current_token

    def syntax_analyzer(self):
        global token
        token=self.get_token()
        self.program()
        print("No errors found; successful compilation")

    def error(self,message):
        global token
        print(message + " on line: " + str(token.line_number))

    def program(self):
        self.generated_program.genQuad('begin_block','program','_','_')
        scope=self.symbolTable.create_scope("program")
        actRec=ActivationRecord('main')
        func=Function('main',self.generated_program.nextQuad(),actRec)
        self.declarations("localVar", func)
        self.functions()
        self.main(func)
        self.symbolTable.print_table(scope)
        self.symbolTable.delete_scope()
        self.generated_program.genQuad('end_block','program','_','_')

    def declarations(self, k, func):
        global token
        while token.recognized_string=='#int':
            token=self.get_token()
            self.id_list("variable", k, func)

    def id_list(self, t, k, func):
        global token
        if token.family=='identifier':
            if t=="variable":
                var=Variable(token.recognized_string)
                self.symbolTable.insert_entity(var)
                func.activationRecord.insert(k)
            else:
                par=Parameter(token.recognized_string)
                self.symbolTable.insert_entity(par)
                func.activationRecord.insert(k)
            token=self.get_token()
            while token.recognized_string==',':
                token=self.get_token()
                if token.family=='identifier':
                    if t=="variable":
                        var=Variable(token.recognized_string)
                        self.symbolTable.insert_entity(var)
                        func.activationRecord.insert(k)
                    else:
                        par=Parameter(token.recognized_string)
                        self.symbolTable.insert_entity(par)
                        func.activationRecord.insert(k)
                    token=self.get_token()
                else:
                    self.error("Error: no ID found after ','")

    def glob_decl(self, k, func):
        global token
        while token.recognized_string=='global':
            token=self.get_token()
            self.id_list("variable", k, func)
            self.symbolTable.scopes[-1].entities.pop(-1) ##AYTO DIAGRAFEI TIS GLOBAL METAVLHTES APO TO SCOPE (PREPEI NA GINETAI AYTO?????)

    def functions(self):
        global token
        while token.recognized_string=='def':
            self.function()

    def nested_functions(self):
        global token
        global quadLabel
        while token.recognized_string=='def':
            q=Quad(0,"","","","")
            q=self.generated_program.deleteLastQuad()
            quadLabel=quadLabel-1
            self.functions()
            self.generated_program.genQuad(q.op,q.op1,q.op2,q.op3)
            
    def function(self):
        global token
        global tmpVarList
        nestedFunctions=[]
        if token.recognized_string=='def':
            token=self.get_token()
            if token.family=='identifier':
                ID=token.recognized_string
                actRec=ActivationRecord(ID)
                func=Function(ID,self.generated_program.nextQuad(),actRec)
                self.symbolTable.scopes[-1].insert_entity(func)
                self.generated_program.genQuad("begin_block", ID,"_","_")
                scope=self.symbolTable.create_scope(ID)
                token=self.get_token()
                if token.recognized_string=='(':
                    token=self.get_token()
                    self.id_list("parameter", "formalPar", func)
                    if token.recognized_string==')':
                        token=self.get_token()
                        if token.recognized_string==':':
                            token=self.get_token()
                            if token.recognized_string=='#{':
                                token=self.get_token()
                                self.declarations("localVar",func)
                                self.nested_functions()
                                self.glob_decl("globalVar",func)
                                while token.family=='identifier' or token.family=='keyword':
                                    self.code_block()
                                if token.recognized_string=='#}':
                                    self.generated_program.genQuad("end_block",ID,"_","_")
                                    func.activationRecord.tmpVars=tmpVarList
                                    for v in func.activationRecord.tmpVars:
                                        func.activationRecord.framelength+=4
                                    tmpVarList=[]
                                    self.symbolTable.print_table(scope)
                                    self.symbolTable.delete_scope()
                                    token=self.get_token()
                                else:
                                    self.error("Error: opened the function but never closed it, missing '#}'")
                            else:
                                self.error("Error: never opened function, missing '#{'")
                        else:
                            self.error("Error: empty function after ':'")
                    else:
                        self.error("Error: never closed ID_LIST, missing ')'")
                else:
                    self.error("Error: parentheses missing from function declaration")
            else:
                self.error("Error: missing function identifier")

    def main(self, func):
        global token
        if token.recognized_string=='#def':
            token=self.get_token()
            if token.recognized_string=='main':
                self.generated_program.genQuad("begin_block","main","_","_")
                token=self.get_token()
                self.declarations("localVar",func)
                self.code_block()
                self.generated_program.genQuad("halt","_","_","_")
                self.generated_program.genQuad("end_block","main","_","_")

    def code_block(self):
        global token
        while token.family=='keyword' or token.family=='identifier':
            self.statement()

    def statement(self):
        self.simple_statement()
        self.structured_statement()

    def simple_statement(self):
        self.assignment_stat()
        self.print_stat()
        self.return_stat()

    def structured_statement(self):
        self.if_stat()
        self.while_stat()

    def assignment_stat(self):
        global token
        expr_place=''
        ID=''
        if token.family=='identifier':
            ID=token.recognized_string
            token=self.get_token()
            if token.recognized_string=='=':
                token=self.get_token()
                if token.recognized_string=='int':
                    token=self.get_token()
                    if token.recognized_string=='(':
                        token=self.get_token()
                        if token.recognized_string=='input':
                            token=self.get_token()
                            self.generated_program.genQuad("in","_","_","_")
                            if token.recognized_string=='(':
                                token=self.get_token()
                                if token.recognized_string==')':
                                    token=self.get_token()
                                    if token.recognized_string==')':
                                        token=self.get_token()
                                    else:
                                        self.error("Error: never closed int(input()), missing ')'")

                                else:
                                    self.error("Error: never closed input, missing ')'")
                            else:
                                self.error("Error: INPUT function missing parentheses")
                    else:
                        self.error("Error: INT missing INPUT function")
                else:
                    expr_place=self.expression()
                    self.generated_program.genQuad('=',expr_place,'_',ID)
            else:
                self.error("Error: ASSIGNMENT missing")

    def print_stat(self):
        global token
        if token.recognized_string=='print':
            self.generated_program.genQuad("out","_","_","_")
            token=self.get_token()
            if token.recognized_string=='(':
                token=self.get_token()
                self.expression()
                if token.recognized_string==')':
                    token=self.get_token()
                else:
                    self.error("Error: PRINT function never closes, missing ')'")
            else:
                self.error("Error: PRINT function missing parentheses")

    def return_stat(self):
        global token
        expr_place=''
        if token.recognized_string=='return':
            token=self.get_token()
            self.generated_program.genQuad("ret",token.recognized_string,"_","_")
            expr_place=self.expression()

    def statement_or_block(self):
        global token
        self.statement()
        if token.recognized_string=='#{':
            token=self.get_token()
            while token.family=='identifier' or token.family=='keyword':
                self.statement()
            if token.recognized_string=='#}':
                token=self.get_token()
            else:
                self.error("Error: STATEMENT BLOCK never closes, missing '#}'")

    def if_stat(self):
        global token
        c=cond([],[])
        l=[]
        if token.recognized_string=='if':
            token=self.get_token()
            c=self.condition()
            if token.recognized_string==':':
                token=self.get_token()
                self.generated_program.backpatch(c.true,self.generated_program.nextQuad())
                self.statement_or_block()
                l=self.generated_program.makeList(self.generated_program.nextQuad())
                self.generated_program.genQuad('jump','_','_','_')
                self.generated_program.backpatch(c.false,self.generated_program.nextQuad())
                while token.recognized_string=='elif':
                    token=self.get_token()
                    c=self.condition()
                    if token.recognized_string==':':
                        token=self.get_token()
                        self.generated_program.backpatch(c.true,self.generated_program.nextQuad())
                        self.statement_or_block()
                        l=self.generated_program.makeList(self.generated_program.nextQuad())
                        self.generated_program.genQuad('jump','_','_','_')
                        self.generated_program.backpatch(c.false,self.generated_program.nextQuad())
                    else:
                        self.error("Error: ELIF missing ':'")
                if token.recognized_string=='else':
                    token=self.get_token()
                    if token.recognized_string==':':
                        token=self.get_token()
                        self.statement_or_block()
                    else:
                        self.error("Error: ELSE missing ':'")
            else:
                self.error("Error: IF missing ':'")

    def while_stat(self):
        global token
        c=cond([],[])
        quad=0
        temp=''
        if token.recognized_string=='while':
            token=self.get_token()
            quad=self.generated_program.nextQuad()
            c=self.condition()
            if token.recognized_string==':':
                token=self.get_token()
                self.generated_program.backpatch(c.true,self.generated_program.nextQuad())
                self.statement_or_block()
                temp=str(quad)
                self.generated_program.genQuad('jump','_','_',temp)
                self.generated_program.backpatch(c.false,self.generated_program.nextQuad())
            else:
                self.error("Error: WHILE missing ':'")

    def expression(self):
        expr_place=''
        term1_place=''
        term2_place=''
        temp=''
        addOp_string=''
        self.optional_sign()
        term1_place=self.term()
        while token.family=="addOperator":
            addOp_string=self.add_oper()
            term2_place=self.term()
            temp=self.newTemp()
            self.generated_program.genQuad(addOp_string,term1_place,term2_place,temp)
            term1_place=temp
        expr_place=term1_place
        return expr_place
            
    def term(self):
        t_place=''
        fact1_place=''
        fact2_place=''
        temp=''
        mulOp_string=''
        fact1_place=self.factor()
        while token.family=="mulOperator":
            mulOp_string=self.mul_oper()
            fact2_place=self.factor()
            temp=self.newTemp()
            self.generated_program.genQuad(mulOp_string,fact1_place,fact2_place,temp)
            fact1_place=temp
        t_place=fact1_place
        return t_place

    def factor(self):
        global token
        f_place=''
        expr_place=''
        if token.family=='number':
            f_place=token.recognized_string
            token=self.get_token()
        elif token.recognized_string=='(':
            token=self.get_token()
            expr_place=self.expression()
            f_place=expr_place
            if token.recognized_string==')':
                token=self.get_token()
            else:
                self.error("Error: FACTOR EXPRESSION never closes, missing ')'")
        elif token.family=='identifier':
            ID=token.recognized_string
            f_place=token.recognized_string
            token=self.get_token()
            self.idtail(ID)
        return f_place

    def idtail(self, ID):
        global token
        if token.recognized_string=='(':
            self.generated_program.genQuad('call',ID,'_','_')
            token=self.get_token()
            self.actual_par_list()
            if token.recognized_string==')':
                token=self.get_token()
            else:
                self.error("Error: IDTAIL never closes, missing ')'")

    def actual_par_list(self):
        global token
        expr1_place=''
        expr2_place=''
        expr1_place=self.expression()
        self.generated_program.genQuad('par',expr1_place,'_','_')
        while token.recognized_string==',':
            token=self.get_token()
            expr2_place=self.expression()
            self.generated_program.genQuad('par',expr2_place,'_','_')

    def condition(self):
        global token
        c=cond([],[])
        c1=cond([],[])
        c2=cond([],[])
        c1=self.bool_term()
        c.true=c1.true
        c.false=c2.false
        while token.recognized_string=='or':
            token=self.get_token()
            self.generated_program.backpatch(c.false,self.generated_program.nextQuad())
            c2=self.bool_term()
            c.false=c2.false
            c.true=self.generated_program.quadPointers.mergeList(c.true,c2.true)
        return c

    def bool_term(self):
        global token
        c=cond([],[])
        c1=cond([],[])
        c2=cond([],[])
        c1=self.bool_factor()
        c.true=c1.true
        c.false=c1.false
        while token.recognized_string=='and':
            token=self.get_token()
            self.generated_program.backpatch(c.true,self.generated_program.nextQuad())
            c2=self.bool_factor()
            c.true=c1.true
            c.false=self.generated_program.quadPointers.mergeList(c.false,c2.false)
        return c

    def bool_factor(self):
        global token
        c=cond([],[])
        c1=cond([],[])
        expr1_place=""
        expr2_place=""
        relOp_string=""
        if token.recognized_string=='not':
            token=self.get_token()
##            expr1_place=self.expression()
##            relOp_string=self.rel_oper()
##            expr2_place=self.expression()
            c1=self.bool_factor()
            c.true=c1.false
            c.false=c1.true
        else:
            expr1_place=self.expression()
            relOp_string=self.rel_oper()
            expr2_place=self.expression()
            c.true=self.generated_program.makeList(self.generated_program.nextQuad())
            self.generated_program.genQuad(relOp_string, expr1_place, expr2_place, '_')
            c.false=self.generated_program.makeList(self.generated_program.nextQuad())
            self.generated_program.genQuad('jump','_','_','_')
        return c

    def optional_sign(self):
        global token
        addOp_string=''
        if token.family=='addOperator':
            self.add_oper()

    def add_oper(self):
        global token
        string=token.recognized_string
        if token.family=='addOperator':
            token=self.get_token()
        return string

    def mul_oper(self):
        global token
        string=token.recognized_string
        if token.family=='mulOperator':
            token=self.get_token()
        return string
        
    def rel_oper(self):
        global token
        string=token.recognized_string
        if token.family=='relOperator':
            token=self.get_token()
        return string

####___________________ENDIAMESOS KWDIKAS___________________
                
global quadLabel
quadLabel=100 #as poume to prwto label

class Quad:
    def __init__(self, label, op, op1, op2, op3):
        self.label=QuadPointer(label)
        self.op=op
        self.op1=op1
        self.op2=op2
        self.op3=op3

    def __str__(self):
        return f'{self.label.label}: "{self.op},{self.op1},{self.op2},{self.op3}"'

class QuadList:
    def __init__(self, programList, quadPointers, quad_counter):
        self.programList=programList
        self.quadPointers=QuadPointerList([])
        self.quad_counter=quad_counter

    def __str__(self):
        return f'QuadList(Quads: {self.programList}\nNumber of quads: {self.quad_counter}\n")'

    def backpatch(self, labelList, quadLabel):
        for l in labelList:
            for q in self.programList: 
                if l==q.label: 
                    q.op3=quadLabel
                    
    def genQuad(self, operator, operand1, operand2, operand3):
        global quadLabel
        newQuadPointer=QuadPointer(quadLabel)
        newQuad=Quad(newQuadPointer,operator,operand1,operand2,operand3)
        self.programList.append(newQuad)
        self.quadPointers.append(newQuadPointer)
        self.quad_counter+=1
        quadLabel+=1

    def deleteLastQuad(self):
        return self.programList.pop(-1)

    def makeList(self, label):
        return [label]

    def emptyList(self):
        return []

    def nextQuad(self):
        return quadLabel

    def printQuads(self, filename):
        with open(filename, 'w') as f:
            for q in self.programList:
                f.write(str(q) + '\n')

class QuadPointer:
    def __init__(self, label):
        self.label=label

    def __str__(self):
        return f'{self.label}'

class QuadPointerList:
    def __init__(self, labelList):
        self.labelList=labelList

    def __str__(self):
        return f'QuadPointerList(List of the labels: {self.labelList})'

    def mergeList(self, l1, l2):
        l=list(set(l1+l2))
        return l

    def append(self, label):
        self.labelList.append(label)

##__________________SYMBOL TABLE________________________

class Entity:
    def __init__(self, name):
        self.name = name

class Variable(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.datatype = "INTEGER"
        self.offset = 0
        self.nestinglevel = 0

class Parameter(Entity):
    def __init__(self, name):
        super().__init__(name)
        self.datatype = "INTEGER"
        self.mode = "cv"
        self.offset = 0
        self.nestinglevel = 0

class Function(Entity):
    def __init__(self, name, startingQuad, activationRecord):
        super().__init__(name)
        self.datatype = "INTEGER"
        self.startingQuad = startingQuad
        self.nestinglevel = 0
        self.offset=0
        self.activationRecord=activationRecord

class TemporaryVariable(Entity):
    def __init__(self,name,datatype,offset):
        super().__init__(name)
        self.datatype="INTEGER"
        self.offset=0

class FormalParameters(Entity):
    def __init__(self,datatype,mode):
        super().__init__(name)
        self.datatype="INTEGER"
        self.mode="cv"
        self.nestinglevel=0
        self.offset=0
        
class Scope:
    def __init__(self, name):
        self.name = name
        self.entities = []
        self.nestinglevel = 0

    def insert_entity(self, entity):
        if isinstance(entity, Variable) or isinstance(entity, Parameter) or isinstance(entity, TemporaryVariable) or isinstance(entity, Function):
            if self.entities:
                last_offset = self.entities[-1].offset
                entity.offset = last_offset + 4  
            else:
                entity.offset = 12  
            entity.nestinglevel = self.nestinglevel
        elif isinstance(entity,Function):
            return
        self.entities.append(entity)

    def search_entity(self,name):
        for entity in self.entities:
            if entity.name==name:
                return entity
        return None

class SymbolTable:
    def __init__(self):
        self.scopes = []

    def create_scope(self, name):
        scope = Scope(name)
        if self.scopes:
            scope.nestinglevel=self.scopes[-1].nestinglevel +1
        else:
            scope.nestinglevel=0
        self.scopes.append(scope)
        return scope

    def delete_scope(self):
        if self.scopes:
            self.scopes.pop()

    def insert_entity(self, entity):
        if self.scopes:
            current_scope = self.scopes[-1]
            current_scope.insert_entity(entity)
        else:
            raise Exception("No scope created yet")

    def print_table(self, scope):
        with open("scopes.int", 'a') as f:
            f.write(scope.name + " ::: ")
            for entity in scope.entities[0:-1]:
                f.write("{}({}, Nesting Level: {}), ".format(entity.name, entity.offset, entity.nestinglevel))
            f.write("{}({}, Nesting Level: {}) ".format(scope.entities[-1].name, scope.entities[-1].offset, scope.entities[-1].nestinglevel))
            f.write("\n")


class ActivationRecord:
    def __init__(self,function):
        self.function=function
        self.returnAddress=0
        self.sp=0
        self.returnValueAddress=0
        self.formalPar=[]
        self.localVar=[]
        self.tmpVars=[]
        self.framelength=0

    def insert(self,t):
        global token
        if t=='formalPar':
            self.formalPar.append(token.recognized_string)
            self.framelength=self.framelength+4
        elif t=='localVar':
            self.localVar.append(token.recognized_string)
            self.framelength=self.framelength+4
            
    def __str__(self):
        return f'Activation Record for func {self.function}:\nFormal parameters list: {self.formalPar}\nLocal variables list: {self.localVar}\nTemporary variables list: {self.tmpVars}\nFramelength: {self.framelength} bytes'

##AYTH EINAI H MAIN MAS ##

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python lexer.py <file_name>")
        sys.exit(1)

    with open("scopes.int", "w"):
            pass ##apla gia na to kanoume clear
        
    global file_name
    file_name=sys.argv[1]
    global f1
    f1=open(file_name,'r')
    global token
    token = Token("", "",1)
    lexer = Lex(token, file_name)
    quadList=QuadList([],[],0)
    symbolTable=SymbolTable()
    parser = Syntax(lexer,quadList,symbolTable)
    parser.syntax_analyzer()
    quadList.printQuads("quads.sym")

## EDW TELEIWNEI H MAIN MAS ##
