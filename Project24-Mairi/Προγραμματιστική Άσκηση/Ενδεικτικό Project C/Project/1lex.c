//PAPAKALOUSI NATALIA 1391
//SKALIDIS DIMITRIS 1264

#include "lex.h"
#include <string.h>

//Deikths pros to source file (ths greeklish)
FILE *fin;

//H synarthsh tou lektikou analyth:
//Otan kaleitai epistrefei thn epomenh lektikh monada
//Sto token mpainei h lektikh monada ws string kai epistrefei ton kwdiko ths
int lex(char token[MAXLEN])
{
	int pinakas[8][23]={
		{0,1,2, ADDTK,MINUSTK,ERROR,TIMESTK,DIVTK,EQTK,4,5,6,QMARKTK,COMMATK,PERTK,7,EOF,ERROR,ERROR,LPARTK,RPARTK,LBRATK,RBRATK}, 
		{E1,1,1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1,E1},
		{E2,E2,2,E2,E2,3,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2,E2},
		{E3,E3,3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3,E3},
		{LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSEQTK,LESSTK,DIFFTK,LESSTK,
		 LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK,LESSTK},
		{MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MOREEQTK,MORETK,MORETK,MORETK,
		 MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK,MORETK},
		{TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,ASSIGNTK,TWODOTSTK,TWODOTSTK,
		TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK,TWODOTSTK},
		{7,7,7,7,7,7,7,7,7,7,7,7,7,ERROR,7,0,7,7,7,7}
		};
	int state,input,i;
	char c;
	

	state=0; //gia na 3ekinhsw apo thn arxikh katastash
	i=0;     //gia na paw arxika stin prwti 8esh tou string pou 8a apo8ikeusw
	while(state>=0 && state <100){
		c=getc(fin);//diavazw ton epomeno xarakhra apo to arxeio
		if(isspace(c)){
			input=0;
		}else if(isalpha(c)){
			input=1;
		}else if(isdigit(c)){
			input=2;
		}else if(c=='+'){
			input=3;
		}else if(c=='-'){
			input=4;
		}else if(c=='.'){
			input=5;
		}else if(c=='*'){
			input=6;
		}else if(c=='/'){
			input=7;
		}else if(c=='='){
			input=8;
		}else if(c=='<'){
			input=9;
		}else if(c=='>'){
			input=10;
		}else if(c==':'){
			input=11;
		}else if(c==';'){
			input=12;
		}else if(c==','){
			input=13;
		}else if(c=='%'){
			input=14;
		}else if(c=='{'){
			input=15;
		}else if(c==EOF){
			input=16;
		}else if(c=='}'){
			input=18;
		}else if(c=='('){
			input=19;
		}else if(c==')'){
			input=20;
		}else if(c=='['){
			input=21;
		}else if(c==']'){
			input=22;
		}else{
			input=17;
		}
		state=pinakas[state][input]; //me paei stin epomeni mou katastash
		token[i]=c; //apo8ikeuw to string,dld h epomenh lektiki monada
		i++; //ka8e fora pou diavazw ena stoixeio paw sto i kai to auxanw
		if(state==0) i=0;  //oso eimai sth 0 den 8elw na apo8ikeuw kati, ara xanaarxikopoiw to i sto 0
	}
	token[i]='\0';

	if(state==LESSTK || state==E1 || state==E2 || state==E3 || state==MORETK || state==TWODOTSTK){
		ungetc(c,fin); //epistrefw sto arxeio ton teleutaio xarakthra pou exw diavasei
		token[i-1]='\0';// afou exw apo8ikeusei to c ston pinaka k twra to epistrefw pisw,prepei na to diagrapsw k apo ton pinaka(string)
	}
	//telikes katastaseis
	if(state>=100){ //termatizw 
		return state; //epistrefw ton kwdiko
	}
	else if(state==E1){
		if(strcmp(token,"programa")==0) return PROGRAMATK;
		if(strcmp(token,"ean")==0)	return EANTK;
		if(strcmp(token,"epanalabe")==0) return EPANALABETK;
		if(strcmp(token,"gia")==0) return GIATK;
		if(strcmp(token,"grapse")==0) return GRAPSETK;
		if(strcmp(token,"eisodos")==0) return EISODOSTK;
		if(strcmp(token,"telossynartisis")==0) return TELOSSYNARTISISTK;
		if(strcmp(token,"h")==0) return HTK;
		if(strcmp(token,"diloseis")==0) return DILOSEISTK;
		if(strcmp(token,"tote")==0) return TOTETK;
		if(strcmp(token,"mexri")==0) return MEXRITK;
		if(strcmp(token,"eos")==0) return EOSTK;
		if(strcmp(token,"synartisi")==0) return SYNARTISITK;
		if(strcmp(token,"exodos")==0) return EXODOSTK;
		if(strcmp(token,"kai")==0) return KAITK;
		if(strcmp(token,"akeraios")==0) return AKERAIOSTK;
		if(strcmp(token,"allios")==0) return ALLIOSTK;
		if(strcmp(token,"oso")==0) return OSOTK;
		if(strcmp(token,"me_bima")==0) return MEBIMATK;
		if(strcmp(token,"diadikasia")==0) return DIADIKASIATK;
		if(strcmp(token,"arxi")==0) return ARXITK;
		if(strcmp(token,"telosdiadikasias")==0) return TELOSDIADIKASIASTK;
		if(strcmp(token,"oxi")==0) return OXITK;
		if(strcmp(token,"pragmatikos")==0) return PRAGMATIKOSTK;
		if(strcmp(token,"ean_telos")==0) return EANTELOSTK;
		if(strcmp(token,"oso_telos")==0) return OSOTELOSTK;
		if(strcmp(token,"diabase")==0) return DIABASETK;
		if(strcmp(token,"diaprosopia")==0) return DIAPROSOPIATK;
		if(strcmp(token,"telos")==0) return TELOSTK;
		if(strcmp(token,"ektelese")==0) return EKTELESETK;
		if(strcmp(token,"gia_telos")==0) return GIATELOSTK;	
		//to return epistrefei ton kwdiko
		return IDTK; 
	}
	else if(state==E2){
		return CONSTTK;
	}
	else if(state==E3){
		return REALTK;
	}
	return state;		
}

