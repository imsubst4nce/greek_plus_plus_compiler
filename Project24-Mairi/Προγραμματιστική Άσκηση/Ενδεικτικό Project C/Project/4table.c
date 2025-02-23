//PAPAKALOUSI NATALIA 1391
//SKALIDIS DIMITRIS 1264

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PARAM 		0
#define FUNC  		1
#define VARIABLE 	2

#define VALUE		100
#define REFER		101


struct entity{
	char name[MAXLEN];
	int type;   	//ti entity einai. PARAM,FUNC,VARIABLE
	int offset; 	//gia tis metavlites kai tis parametrous
	int parammode; 	//me timh h me anafora (VALUE,REFER) an einai parametros
	int nestinglevel; //apo8hkeuw to vathos fwliasmatos gia ka8e metavlhth wste na 3erw an einai topikh h global
	struct entity *next; // gia thn lista
};

struct scope{
	char name[MAXLEN];
	int nestinglevel; 	//va8os fwliasmatos
	struct entity *elist;	//h lista me ta entities gia to sygkekrimeno scope
	struct scope *next;
};


struct scope * SCOPES=NULL; //PANTA stin korufh ths stoivas

void create_scope(char name[MAXLEN])
{
	struct scope *news;// ston kainourgio komvo
	//desmeuw mnhmh gia to neo scope
	news = (struct scope *)malloc( sizeof(struct scope));
	if(news==NULL){
		printf("ERROR in malloc (create_scope)\n");
		exit(1);
	}
	strcpy(news->name,name);
	news->elist = NULL; //arxikopoiw se NULL thn lista me ta entities
	if(SCOPES==NULL){ //einai mono gia ton prwto prwto pou dimiourgoume 
		SCOPES=news;
		news->nestinglevel=0;
		news->next = NULL;
	}
	else{
		news->nestinglevel=SCOPES->nestinglevel + 1;
		news->next = SCOPES;
		SCOPES = news;//kainourgios
	}
}

//kanw delete auto pou vrisketai sthn koryfh ths stoivas
void delete_scope()
{
	if(SCOPES==NULL){ //den mporw na kanw delete
		printf("DEN yparxei scope gia diagrafh\n");
		exit(1);
	}
	SCOPES=SCOPES->next;
}


//eisagw mia kainourgia entity sthn koryfh ths stoivas
void insert_entity(char name[MAXLEN], int type, int parammode)
{
	struct entity *newe;
	struct entity *tmp,*prev;
	int lastoffset=-1;
	
	newe= (struct entity *)malloc(sizeof(struct entity));
	if(newe==NULL){
		printf("ERROR in malloc (insert_entity)\n");
		exit(1);
	}
	strcpy(newe->name,name);
	newe->type = type;
	newe->parammode = parammode;
	newe->next = NULL;
	newe->nestinglevel = SCOPES->nestinglevel; // gia na mhn mperdepsw ta x otan einai se diaforetika scope

	//diatrexw thn lista me ta entities wste na to valw sto telos
	//proxwrane mazi
	prev=NULL; 
	tmp=SCOPES->elist; //vazw ton deixth sthn arxh ths listas
	while(tmp!=NULL){ //gia na dw an uparxoun hdh entities,pou na valw to epomeno
		prev=tmp;
		if(tmp->type != FUNC){
			lastoffset = tmp->offset;
		}
		tmp=tmp->next;
	}
	if(prev==NULL){ //kenh lista
		SCOPES->elist = newe;	//arxikopoiw thn lista sto neo komvo
		newe->offset = 12;
	}
	else{
		prev->next = newe; 	//vazw ton teleutaio na deixnei sto kainourgio
		newe->offset = lastoffset + 4;
	}
}

//mou epistrefei ena deikth pros thn antistoixh ontothta. An den yparxei auth h ontothta,
//tote epistrefei NULL
struct entity *search_entity(char name[MAXLEN])
{
	struct entity *etmp;  //gia na diasxisw ta entities
	struct scope *stmp;  //gia na diasxisw ta scopes

	stmp=SCOPES;
	while(stmp!=NULL){
		etmp = stmp->elist;
		while(etmp!=NULL){
			if(strcmp(etmp->name,name)==0){ //sygkrinw ta onomata gia na dw an yparxei sth lista
				return etmp;
			}
			etmp=etmp->next;
		}
		stmp=stmp->next;
	}
	return NULL;
	
}

void print_table()
{
	struct entity *etmp;
	struct scope *stmp;

	printf("=========================================\n");
	stmp=SCOPES;
	while(stmp!=NULL){
		etmp=stmp->elist;
		printf("SCOPE: %s\n",stmp->name);
		printf("\t");
		while(etmp!=NULL){
			if(etmp->type==VARIABLE){
				printf("%s (%d) -> ",etmp->name, etmp->offset);
			}
			else if(etmp->type==PARAM){
				printf("%s (PARAM - %d) -> ",etmp->name, etmp->offset);
			}
			else{
				printf("%s -> ",etmp->name);
			}
			etmp=etmp->next; 
		}
		printf("\n");
		stmp=stmp->next; //proxwraei sto epomeno simeio tis stoivas
	}
	printf("=========================================\n\n");
}

/* parageigma dokimis twn synarthsewn tou pinaka symvolwn
int main()
{
	create_scope("main");
	insert_entity("x",VARIABLE,0);
	insert_entity("y",VARIABLE,0);
	insert_entity("myfunction",FUNC,0);
	create_scope("myfunction");
	insert_entity("i",VARIABLE,0);
	insert_entity("j",VARIABLE,0);
	print_table();
}

*/





