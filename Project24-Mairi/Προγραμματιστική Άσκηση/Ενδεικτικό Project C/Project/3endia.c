//PAPAKALOUSI NATALIA 1391
//SKALIDIS DIMITRIS 1264

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int quadnum = 1; //gia thn epomenh tetrada pou 8a parax8ei.(gia etiketes)

struct quad{
	int num;
	char op[4][MAXLEN];
	struct quad *next;
};

//struct gia tis listes twn tetradwn
struct list{
	int quad; //o arithmos tis tetradas
	struct list *next;  //deikths ston epomeno
};

struct kanonas{
	struct list *true;
	struct list *false;
};

//deikths pros thn lista twn tetradwn.
struct quad *QUADS = NULL;

//epistrefei ton ari8mo ths epomenhs tetradas pou 8a parax8ei.
int nextquad()
{
	return quadnum;
}

//dhmiourgei thn tetrada: op0,op1,op2,op3,
void genquad(char op0[MAXLEN],char op1[MAXLEN], char op2[MAXLEN],char op3[MAXLEN])
{
	struct quad *q;
	struct quad *prev, *tmp;
	
	q = (struct quad *)malloc(sizeof(struct quad));
	if(q==NULL){
		printf("Error in malloc\n");
		exit(1);
	}
	strcpy(q->op[0],op0);
	strcpy(q->op[1],op1);
	strcpy(q->op[2],op2);
	strcpy(q->op[3],op3);
	q->num = quadnum;
	quadnum++;
	q->next = NULL;

	prev=NULL;
	tmp=QUADS;
	while(tmp!=NULL){
		prev=tmp;
		tmp=tmp->next;
	}
	if(prev==NULL){ //gia thn prwth tetrada pou 8a dhmiourgh8ei
		QUADS=q;
	}else{
		prev->next = q;
	}
}

void print_quads()
{
	struct quad *tmp;

	tmp=QUADS;
	while(tmp!=NULL){
		printf("%d: %s\t%s\t%s\t%s\n",tmp->num,tmp->op[0],tmp->op[1],tmp->op[2],tmp->op[3]);
		tmp=tmp->next;
	}
}

//dhmiourgei mia lista tetradwn, apo8hkeuontas kai ton arithmo tis prwths tetradas
//epistrefei deikth sth lista pou dhmiourghse
struct list *makelist(int q)
{
	struct list *l;

	l = (struct list *)malloc(sizeof(struct list));
	if(l==NULL){
		printf("Error in malloc\n");
		exit(1);
	}
	l->quad=q;
	l->next=NULL;
}

//pairnei ws orisma 2 listes. tis synenonei kai epistrefei to apotelesma
struct list *merge(struct list *l1, struct list *l2)
{
	struct list *prev, *tmp;
	
	if(l1==NULL) return l2;
	if(l2==NULL) return l1;

	//prepei na ftasw sto telos ths l1, wste
	//na valw ton teleutaio komvo ths l1, na deinei ston prwto ths l2
	prev=NULL;
	tmp=l1;
	while(tmp!=NULL){
		prev=tmp;
		tmp=tmp->next;
	}
	prev->next = l2; //edw vazw ton teleutaio ths l1 na deixnei ston prwto ths l2
	return l1;
}

//pairnei tis tetrades tis listas l kai symplhrwnei to 4o pedio me to noumero ths tetradas q, dld pou 8a kanei goto
void backpatch(struct list *l, int q)
{
	struct list *ltmp; //deikths gia thn diasxish ths listas l
	struct quad *qtmp; //deikths gia thn diasxish ths listas twn tetradwn (QUADS)

	ltmp =l;
	while(ltmp!=NULL){
		//prepei na psaxw kai na vrw thn tetrada me arithmo ltmp->quad
		qtmp=QUADS;
		while(qtmp!=NULL){
			if(qtmp->num==ltmp->quad){
				sprintf(qtmp->op[3],"%d",q); //antistrofh diadikasia ths atoi()
				break; //an vrw ton kombo stamataw
			}
			qtmp=qtmp->next; //to epomeno gia to apo mesa
		}
		ltmp=ltmp->next; //to epomeno gia to ap'exw
	}
}

int tmpcnt=1;
	
char *newTemp()
{
	char *s;
	
	s = (char *)malloc(MAXLEN*sizeof(char));
	if(s==NULL){
		printf("Error in malloc\n");
		exit(1);
	}
	sprintf(s,"T_%d",tmpcnt);
	tmpcnt++;
	return s;
}
/*
//dokimastikh main
void main()
{
	struct list *l1;
	struct list *l2;
	
	genquad("+","a","b","c");
	genquad("<=","xx","tetst","100");
	genquad(":=","sdfads","tdssdf","200");
	l1=makelist(nextquad());
	genquad(">","x","a","_");
	l2=makelist(nextquad());
	genquad("jump","_","_","_");
	l1=merge(l1,l2);
	backpatch(l1,nextquad());
	print_quads();
	
}

*/



