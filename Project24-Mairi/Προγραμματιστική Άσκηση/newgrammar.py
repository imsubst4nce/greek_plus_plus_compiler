def program(self):
    self.declarations()
    self.functions()
    self.main()

def declarations(self):
    global token
    while token.recognized_string=='#int':
        token=self.get_token()
        self.id_list()

def id_list(self):
    global token
    if token.family=='identifier':
        token=self.get_token()
        while token.recognized_string==',':
            token=self.get_token()
            if token.family=='identifier':
                token=self.get_token()
            else:
                self.error("Error: no ID found after ','")

def glob_decl(self):
    global token
    while token.recognized_string=='global':
        token=self.get_token()
        self.id_list()

def functions():
    global token
    while token.recognized_string=='def':
        self.function()

def function():
    global token
    if token.recognized_string=='def':
        token=self.get_token()
        if token.family=='identifier':
            token=self.get_token()
            if token.recognized_string=='(':
                token=self.get_token()
                self.id_list()
                if token.recognized_string==')':
                    token=self.get_token()
                    if token.recognized_string==':':
                        token=self.get_token()
                        if token.recognized_string=='#{':
                            self.declarations()
                            self.functions()
                            self.glob_decl()
                            self.code_block()
                            if self.recognized_string=='#}':
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

def main(self):
    global token
    if token.recognized_string=='#def':
        token=self.get_token()
        if token.recognized_string=='main':
            token=self.get_token()
            self.declarations()
            self.code_block()

def code_block(self):
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
            self.expression(expr_place)
            self.generated_program.genQuad('=',expr_place,'_',ID)
            if token.recognized_string=='int':
                token=self.get_token()
                if token.recognized_string=='(':
                    token=self.get_token()
                    if token.recognized_string=='input':
                        token=self.get_token()
                        if token.recognized_string=='(':
                            token=self.get_token()
                            if token.recognized_string==')':
                                token=self.get_token()
                            else:
                                self.error("Error: never closed input, missing ')'")
                        else:
                            self.error("Error: INPUT function missing parentheses")
                else:
                    self.error("Error: INT missing INPUT function")
        else:
            self.error("Error: ASSIGNMENT missing")

def print_stat(self):
    global token
    if token.recognized_string=='print':
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
    if token.recognized_string=='return':
        token=self.get_token()
        self.expression()

def statement_or_block(self):
    global token
    self.statement()
    if token.recognized_string=='#{':
        token=self.get_token()
        self.statement()
        if token.recognized_string=='#}':
            token=self.get_token()
        else:
            self.error("Error: STATEMENT BLOCK never closes, missing '#}'")

def if_stat(self):
    global token
    if token.recognized_string=='if':
        token=self.get_token()
        self.condition()
        if token.recognized_string==':':
            token=self.get_token()
            self.statement_or_block()
            while token.recognized_string=='elif':
                token=self.get_token()
                self.condition()
                if token.recognied_string==':':
                    token=self.get_token()
                    self.statement_or_block()
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
    if token.recognized_string=='while':
        token=self.get_token()
        self.condition(c)
        if token.recognized_string==':':
            token=self.get_token()
            self.statement_or_block()
        else:
            self.error("Error: WHILE missing ':'")

def expression(self):
    self.optional_sign()
    self.term()
    self.add_oper()
    while token.family=="addOperator":
        self.term()            

def term(self):
    self.factor()
    self.mul_oper()
    while token.family=="mulOperator":
        self.factor()

def factor(self):
    global token
    if token.family=='number':
        token=self.get_token()
    if token.recognized_string=='(':
        token=self.get_token()
        self.expression()
    if token.family=='identifier':
        token=self.get_token()
        self.idtail()

def idtail(self):
    global token
    if token.recognized_string=='(':
        token=self.get_token()
        self.actual_par_list()
        if token.recognized_string==')':
            token=self.get_token()
        else:
            self.error("Error: IDTAIL never closes, missing ')'")

def actual_par_list(self):
    global token
    self.expression()
    while token.recognized_string==',':
        token=self.get_token()
        self.expression()

def condition(self):
    global token
    self.bool_term()
    while token.recognized_string=='or':
        token=self.get_token()
        self.bool_term()
        
def bool_term(self):
    global token
    self.bool_factor()
    while token.recognized_string=='and':
        token=self.get_token()
        self.bool_factor()

def bool_factor(self):
    global token
    if token.recognized_string=='not':
        token=self.get_token()
        self.condition()
        self.expression()
        self.rel_op()
        self.expression()
    else:
        self.expression()
        self.rel_op()
        self.expression()

def optional_sign(self):
    global token
    if token.family=='addOperator':
        self.add_oper()

def add_oper(self):
    global token
    if token.family=='addOperator':
        token=self.get_token()

def mul_oper(self):
    global token
    if token.family=='mulOperator':
        token=self.get_token()
    
def rel_oper(self):
    global token
    if token.family=='relOperator':
        token=self.get_token()
            
