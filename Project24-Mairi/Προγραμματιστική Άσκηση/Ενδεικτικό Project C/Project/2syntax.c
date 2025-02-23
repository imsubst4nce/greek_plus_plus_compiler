//PAPAKALOUSI NATALIA 1391
//SKALIDIS DIMITRIS 1264

#include "lex.c"
#include "endia.c"
#include "table.c"
#include "final.c"

int tk;//ston tk apo8ikeuetai o kwdikos
char str[MAXLEN]; // string pou 8a apo8ikeuei tin epomeni lektiki monada

void program();
void programblock(char name[MAXLEN]);
void declarations();
void varlist(int type); //pernei ws orisma an 8a vrei parametrous h metavlites
void type();
void subprograms();
void func();
void proc();
void formalpars();
void formalparlist();
void formalparitem();
void funcblock(char name[MAXLEN]);
void procblock(char name[MAXLEN]);
void funcinput(); 
void funcoutput();
void sequence();
void statement();
void assignment_stat();
void if_stat();
void elsepart();
void while_stat();
void do_stat();
void for_stat();
void step();
void print_stat();
void printelement();
void input_stat();
void call_stat();
void idtail();
void actualpars();
void actualparlist();
void actualparitem();
void condition(struct kanonas *c);
void boolterm(struct kanonas *bt);
void boolfactor(struct kanonas *bf);
void expression(char eplace[MAXLEN]);
void term(char tplace[MAXLEN]);      
void factor(char fplace[MAXLEN]);
void relational_oper(char oper[MAXLEN]);
void add_oper(char oper[MAXLEN]);
void mul_oper(char oper[MAXLEN]);
void optional_sign(); 


int main(int argc, char *argv[])
{	
	if(argc!=2){
		printf("Error!!!!\n");
		exit(1);
	}
	fin=fopen(argv[argc-1],"r");
	if(fin==NULL){//den exei anoixei swsta
		printf("ERROR opening file\n");
		exit(1);
	}
	/*arxika diavazw thn prwth lektikh monada*/
	tk=lex(str);
	/*kalw ton arxiko kanona tou syntaktikou analyth*/
	program();//----------------------
	print_quads(); //typwnoume oles tis tetrades tou endiamesou kwdika
	fclose(fin);
	return 0;
}

void program()
{
	char name[MAXLEN];
	
	if(tk==PROGRAMATK){
		tk=lex(str); //diavazw epomenh lektikh monada
		if(tk==IDTK){
			create_scope(str);
			strcpy(name,str); //apo8hkeuw to onoma tou programmatos wste na to perasw ws orisma sthn programblock()
			tk=lex(str);   //epeidh to katanalwnw prepei na to exw kapou apo8ikeumeno
			programblock(name);
			print_table();
			delete_scope();
		}
		else{
			printf("Error: Perimena ID kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimenw programa kai vrika: %s\n",str);
		exit(1);
	}
}

void programblock(char name[MAXLEN])
{
	declarations();
	subprograms();
	if(tk==ARXITK){
		tk=lex(str);
		genquad("begin_block",name,"_","_");
		sequence();
		if(tk==TELOSTK){
			tk=lex(str);
			genquad("end_block",name,"_","_");
		}
		else{
			printf("Error perimenw telos kai vrika: %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimenw arxi kai vrika: %s\n",str);
		exit(1);
	}
}

void declarations()
{
	if(tk==DILOSEISTK){
		tk=lex(str);
		while(tk==IDTK){
			varlist(VARIABLE);
		}
	}
}

void varlist(int t)
{
	if(tk==IDTK){  //an h epomenh lektikh monada einai id
		insert_entity(str,t,0);
		tk=lex(str); //thn katanalwnw k diavazw tin epomenh
		while(tk==COMMATK){ //an h epomenh einai ,
			tk=lex(str); //thn katanalwnw 
			if(tk==IDTK){ //kai prepei na vrw meta ena id
				insert_entity(str,t,0);
				tk=lex(str); //diavazw epomeni lektiki monada
			}
			else{ //an den vrw id exw lathos
				printf("Error perimena id kai vrika %s\n",str);
				exit(1);
			}
		}
		if(tk==TWODOTSTK){
			tk=lex(str);
			type();
			if(tk==QMARKTK){
				tk=lex(str);
			}
			else{
				printf("Error perimena ; kai vrika %s\n",str);
				exit(1);
			}
		}
	}
}

void type()
{
	if(tk==AKERAIOSTK){
		tk=lex(str);
	}
	else if(tk==PRAGMATIKOSTK){
		tk=lex(str);
	}
	else{
		printf("Error perimenw akeraios h pragmatikos kai vrika: %s\n",str);
		exit(1);
	}
}

void subprograms()
{
	while(tk==SYNARTISITK || tk==DIADIKASIATK){
		if(tk==SYNARTISITK){
			//den diavazw epomenh lektikh monada. tha to kanei h func
			func(); 
		}
		else if(tk==DIADIKASIATK){
			proc();
		}
		else{
			printf("Error perimena synartisi h diadikasia kai vrika %s\n",str);
			exit(1);
		}
	}
}

void func()
{
	char name[MAXLEN];
	
	if(tk==SYNARTISITK){
		tk=lex(str);
		if(tk==IDTK){
			strcpy(name,str); //krataw to onoma ths synartisis wste na to xrhsimopoihsw otan 8a kanw create_scope()
			insert_entity(str,FUNC,0); //eisagw to entity gia thn synarthsh
			tk=lex(str);
			formalpars();
			if(tk==TWODOTSTK){
				tk=lex(str);
				type();
				create_scope(name); //eisagw ena neo scope
				funcblock(name);
				print_table();
				delete_scope();  //diagrafw to scope ths synartisis pou teleiwnei
			}
			else{
				printf("Error perimena : kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena id kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena synartisi kai vrika %s\n",str);
		exit(1);
	}
}

void proc()
{
	char name[MAXLEN];  //------
	
	if(tk==DIADIKASIATK){
		tk=lex(str);
		if(tk==IDTK){
			strcpy(name,str); //--------
			tk=lex(str);
			formalpars();
			insert_entity(name,FUNC,0);
			create_scope(name); //-------
			procblock(name);
			print_table(); //--------
			delete_scope();	//---------
		}
		else{
			printf("Error perimena id kai vrika: %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena diadikasia kai vrika: %s\n",str);
		exit(1);
	}
}

void formalpars()
{
	if(tk==LPARTK){
		tk=lex(str);
		formalparlist();//---------------------
		if(tk==RPARTK){
			tk=lex(str);
		}
		else{
			printf("Error perimena ) kai vrika %s\n",str);
			exit(1);
		}
	}
}

void formalparlist()
{
	formalparitem();
	while(tk==COMMATK){
		tk=lex(str);
		formalparitem();
	}
}

void formalparitem()
{
	if(tk==IDTK){
		tk=lex(str);
	}
	else if(tk==PERTK){
		tk=lex(str);
		if(tk==IDTK){
			tk=lex(str);
		}
		else{
			printf("Error perimena id kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena id h  kai vrika %s\n",str);
		exit(1);
	}
}

void funcblock(char name[MAXLEN])
{
	if(tk==DIAPROSOPIATK){
		tk=lex(str);
		funcinput();
		funcoutput();
		declarations();
		if(tk==ARXITK){
			tk=lex(str);
			genquad("begin_block",name,"_","_");
			sequence();
			if(tk==TELOSSYNARTISISTK){
				tk=lex(str);
				genquad("end_block",name,"_","_");
			}
			else{
				printf("Error perimena telossynartisis kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena arxi kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena diaprosopia kai vrika %s\n",str);
		exit(1);
	}
}

void procblock(char name[MAXLEN])
{
	if(tk==DIAPROSOPIATK){
		tk=lex(str);
		funcinput();
		funcoutput();
		declarations();
		if(tk==ARXITK){
			tk=lex(str);
			genquad("begin_block",name,"_","_");
			sequence();
			if(tk==TELOSDIADIKASIASTK){
				tk=lex(str);
				genquad("end_block",name,"_","_");
			}
			else{
				printf("Error perimena telos_diadikasias kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena arxi kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena diaprosopia kai vrika %s\n",str);
		exit(1);
	}	
}

void funcinput()
{
	if(tk==EISODOSTK){
		tk=lex(str);
		while(tk==IDTK){
			varlist(PARAM);
		}	
	}
}

void funcoutput()
{
	if(tk==EXODOSTK){
		tk=lex(str);
		while(tk==IDTK){
			varlist(PARAM);
		}	
	}
}

void sequence()
{
	statement();
	while(tk==QMARKTK){
		tk=lex(str);
		statement();
	}
}

void statement()
{
	if(tk==IDTK){
		assignment_stat();
	}
	else if(tk==EANTK){
		if_stat();
	}
	else if(tk==OSOTK){
		while_stat();
	}
	else if(tk==EPANALABETK){
		do_stat();
	}
	else if(tk==GIATK){
		for_stat();
	}
	else if(tk==DIABASETK){
		input_stat();
	}
	else if(tk==GRAPSETK){
		print_stat();
	}
	else if(tk==EKTELESETK){
		call_stat();
	}
	
}

void assignment_stat()
{
	char eplace[MAXLEN];
	char name[MAXLEN];
	
	if(tk==IDTK){
		strcpy(name,str);
		tk=lex(str);
		if(tk==ASSIGNTK){
			tk=lex(str);
			expression(eplace);
			genquad(":=",eplace,"_",name);
		}
		else{
			printf("Error perimena := kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena id kai vrika %s\n",str);
		exit(1);
	}
}

void if_stat()
{
	struct kanonas c;
	struct list *l1;
	
	if(tk==EANTK){
		tk=lex(str);
		if(tk==LPARTK){
			tk=lex(str);
			condition(&c);                                                              
			if(tk==RPARTK){
				tk=lex(str);
				if(tk==TOTETK){
					tk=lex(str);
					backpatch(c.true,nextquad());
					sequence();
					l1 = makelist(nextquad());
					genquad("jump","_","_","_");
					backpatch(c.false,nextquad());
					elsepart();
					if(tk==EANTELOSTK){
						tk=lex(str);
						backpatch(l1,nextquad());	
					}
					else{
						printf("Error perimena ean_telos kai vrika %s\n",str);
						exit(1);
					}
				}
				else{
					printf("Error perimena tote kai vrika %s\n",str);
					exit(1);
				}
			}
			else{
				printf("Error perimena ) kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena ( kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena ean kai vrika %s\n",str);
		exit(1);
	}
}

void elsepart()
{
	if(tk==ALLIOSTK){
		tk=lex(str);
		sequence();
	}
	//yparxei to e sto kanona ara den vgazw mnm lathous
}

void while_stat()
{
	struct kanonas c;
	int q;
	char tmp[MAXLEN];

	if(tk==OSOTK){
		tk=lex(str);
		if(tk==LPARTK){
			tk=lex(str);
			q=nextquad();
			condition(&c);
			if(tk==RPARTK){
				tk=lex(str);
				if(tk==EPANALABETK){
					tk=lex(str);
					backpatch(c.true,nextquad());
					sequence();
					if(tk==OSOTELOSTK){
						tk=lex(str);
						sprintf(tmp,"%d",q);
						genquad("jump","_","_",tmp);
						backpatch(c.false,nextquad());
					}
					else{
						printf("Error perimena oso_telos kai vrika %s\n",str);
						exit(1);
					}
				}
				else{
					printf("Error perimena epanalabe kai vrika %s\n",str);
					exit(1);
				}
			}
			else{
				printf("Error perimena ) kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena ( kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena oso kai vrika %s\n",str);
		exit(1);
	}
}

void do_stat()
{
	struct kanonas c;
	
	if(tk==EPANALABETK){
		tk=lex(str);
		sequence();
		if(tk==MEXRITK){
			tk=lex(str);
			if(tk==LPARTK){
				tk=lex(str);
				condition(&c);
				if(tk==RPARTK){
					tk=lex(str);
				}
				else{
					printf("Error perimena ) kai vrika %s\n",str);
					exit(1);
				}
			}
			else{
				printf("Error perimena ( kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena mexri kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena epanalabe kai vrika %s\n",str);
		exit(1);
	}
}

void for_stat()
{
	char eplace[MAXLEN];
	char e2place[MAXLEN];
	char e3place[MAXLEN];
	
	if(tk==GIATK){
		tk=lex(str);
		if(tk==IDTK){
			tk=lex(str);
			if(tk==ASSIGNTK){
				tk=lex(str);
				expression(eplace);
				if(tk==EOSTK){
					tk=lex(str);
					expression(e2place);
					step(e3place);
					if(tk==EPANALABETK){
						tk=lex(str);
						sequence();
						if(tk==GIATELOSTK){
							tk=lex(str);
						}
						else{
							printf("Error perimena gia_telos kai vrika %s\n",str);
							exit(1);
						}
					}
					else{
						printf("Error perimena epanalabe kai vrika %s\n",str);
						exit(1);
					}
				}
				else{
					printf("Error perimena eos kai vrika %s\n",str);
					exit(1);
				}
			}
			else{
				printf("Error perimena := kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena id kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena gia kai vrika %s\n",str);
		exit(1);
	}
}

void step(char place[MAXLEN])
{
	if(tk==MEBIMATK){
		tk=lex(str);
		expression(place);
	}
}

void print_stat()
{
	if(tk==GRAPSETK){
		tk=lex(str);
		printelement();
		while(tk==COMMATK){
			tk=lex(str);
			printelement();
		}
	}
	else{
		printf("Error perimena grapse kai vrika %s\n",str);
		exit(1);
	}
}

void printelement()
{
	char eplace[MAXLEN];
	
	expression(eplace);
	//TODO: string
}

void input_stat()
{
	if(tk==DIABASETK){
		tk=lex(str);
		if(tk==LPARTK){
			tk=lex(str);
			if(tk==IDTK){
				tk=lex(str);
				if(tk==RPARTK){
					tk=lex(str);
				}
				else{
					printf("Error perimena ) kai vrika %s\n",str);
					exit(1);
				}
			}
			else{
				printf("Error perimena id kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena ( kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena diavase kai vrika %s\n",str);
		exit(1);
	}
}

void call_stat()
{
	if(tk==EKTELESETK){
		tk=lex(str);
		if(tk==IDTK){
			tk=lex(str);
			idtail();
		}
		else{
			printf("Error perimena id kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena ektelese kai vrika %s\n",str);
		exit(1);
	}
}

void idtail()
{
	if(tk==LPARTK){
		actualpars();
	}
}

void actualpars()
{
	if(tk==LPARTK){
		tk=lex(str);
		actualparlist();
		if(tk==RPARTK){
			tk=lex(str);
		}
		else{
			printf("Error perimena ) kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		printf("Error perimena ( kai vrika %s\n",str);
		exit(1);
	}
}

void actualparlist()
{
	actualparitem();
	while(tk==COMMATK){
		tk=lex(str);
		actualparitem();
	}
}

void actualparitem()
{
	char eplace[MAXLEN];
	
	if(tk==PERTK){
		tk=lex(str);
		if(tk==IDTK){
			tk=lex(str);
		}
		else{
			printf("Error perimena id kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		expression(eplace);
	}
}

void condition(struct kanonas *c)
{
	struct kanonas bt1,bt2;
	
	boolterm(&bt1);
	c->true=bt1.true;
	c->false=bt1.false;
	while(tk==HTK){
		tk=lex(str);
		backpatch(c->false,nextquad());
		boolterm(&bt2);
		c->false = bt2.false;
		c->true = merge(c->true,bt2.true);
	}
}

void boolterm(struct kanonas *bt)
{
	struct kanonas bf1,bf2;
	
	boolfactor(&bf1);
	bt->true = bf1.true;
	bt->false = bf1.false;
	while(tk==KAITK){
		tk=lex(str); 
		backpatch(bt->true,nextquad());  //an einai swsto 8a me paei stin epomeni tetrada
		boolfactor(&bf2);
		bt->true = bf1.true;
		bt->false = merge(bt->false, bf2.false);
	}
}

void boolfactor(struct kanonas *bf)
{
	char e1place[MAXLEN];
	char e2place[MAXLEN];
	char oper[MAXLEN];
	struct kanonas c;
	
	if(tk==OXITK){
		tk=lex(str);
		if(tk==LBRATK){
			tk=lex(str);
			condition(&c);
			bf->true = c.false;
			bf->false = c.true;
			if(tk==RBRATK){
				tk=lex(str);
			}
			else {
				printf("Error perimena ] kai vrika %s\n",str);
				exit(1);
			}
		}
		else{
			printf("Error perimena [ kai vrika %s\n",str);
			exit(1);
		}
	}
	else if(tk==LBRATK){
		tk=lex(str);
		condition(&c);
		bf->true = c.true;
		bf->false = c.false;
		if(tk==RBRATK){
			tk=lex(str);
		}
		else{
			printf("Error perimena ] kai vrika %s\n",str);
			exit(1);
		}
	}
	else{
		expression(e1place);
		relational_oper(oper);
		expression(e2place);
		bf->true=makelist(nextquad());
		genquad(oper,e1place,e2place,"_");
		bf->false=makelist(nextquad());
		genquad("jump","_","_","_");
	}
}

void expression(char eplace[MAXLEN]) //tha apo8hkeusei sto eplace, pou einai to apotelesma ths
{
	char t1place[MAXLEN]; //gia na apo8hkeusei h prwth term to apotelesma ths
	char t2place[MAXLEN]; //gia na apo8hkeusei h deuterh term to apotelesma ths
	char *w;
	char oper[MAXLEN];
	
	optional_sign();
	term(t1place);
	while(tk==ADDTK || tk==MINUSTK){
		add_oper(oper);
		term(t2place);
		w = newTemp();
		genquad(oper,t1place,t2place,w);
		strcpy(t1place,w);
	}
	strcpy(eplace,t1place);
}

void term(char tplace[MAXLEN])
{
	char f1place[MAXLEN];
	char f2place[MAXLEN];
	char *w;
	char oper[MAXLEN];
	
	factor(f1place);
	while(tk==TIMESTK || tk==DIVTK){
		mul_oper(oper);
		factor(f2place);
		w = newTemp();
		genquad(oper,f1place,f2place,w);
		strcpy(f1place,w);
	}
	strcpy(tplace,f1place);
}

void factor(char fplace[MAXLEN])
{
	char eplace[MAXLEN];
	
	if(tk==CONSTTK || tk==REALTK){
		strcpy(fplace,str);
		tk=lex(str);
	}
	else if(tk==LPARTK){
		tk=lex(str);
		expression(eplace);
		strcpy(fplace,eplace);
		if(tk==RPARTK){
			tk=lex(str);
		}
		else{
			printf("Error perimena ) kai vrika %s\n",str);
			exit(1);
		}
	}
	else if(tk==IDTK){
		strcpy(fplace,str);
		tk=lex(str);
		idtail();
	}
	else{
		printf("Error perimena const | real | ( | id kai vrika %s\n",str);
		exit(1);
	}
}

void relational_oper(char oper[MAXLEN])
{
	if(tk==EQTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==LESSTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==LESSEQTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==DIFFTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==MORETK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==MOREEQTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else{
		printf("Error perimena =|<|<=|<>|>|>= kai vrika %s\n",str);
		exit(1);
	}
}

void add_oper(char oper[MAXLEN])
{
	if(tk==ADDTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==MINUSTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else{
		printf("Error perimena +|- kai vrika %s\n",str);
		exit(1);
	}
}

void mul_oper(char oper[MAXLEN])
{
	if(tk==TIMESTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else if(tk==DIVTK){
		strcpy(oper,str);
		tk=lex(str);
	}
	else{
		printf("Error perimena * | / kai vrika %s\n",str);
		exit(1);
	}
	
}

void optional_sign()
{
	char oper[MAXLEN];
	
	if(tk==ADDTK || tk==MINUSTK){
		add_oper(oper);
	}
}

