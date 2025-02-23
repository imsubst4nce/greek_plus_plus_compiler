#include <stdio.h>
#include <stdlib.h>

FILE *finalfp;

void loadvr(char v[MAXLEN], int r)
{
	struct entity *ent;

	ent = search_entity(v);
	
	//1h periptwsh - an to v einai sta8era
	if(isdigit(v[0])){
		fprintf(finalfp, "movi R[%d], %s\n",r, v);
	}
	//2h periptwsh - an to v einai global	
	else if(ent->nestinglevel==0){
		fprintf(finalfp, "movi R[%d], M[%d]\n",r, 600+ent->offset); //prepei na paw sti mnimi gia na to diavasw
	}
	//3h periptwsh - (topikh metavliti)
	else if(ent->nestinglevel==SCOPES->nestinglevel  && ent->type==VARIABLE){ //an h metavlhth einai sto trexon vathos fwliasmatos
		fprintf(finalfp, "movi R[%d], M[R[0] + %d]\n", r, ent->offset);
	}
	//3h periptwsh - (parametros me timi)
	else if(ent->nestinglevel==SCOPES->nestinglevel  && ent->type==PARAM && ent->parammode==VALUE){ 
		fprintf(finalfp, "movi R[%d], M[R[0] + %d]\n", r, ent->offset);
	}
	//4h periptwsh - (parametros me anafora)
	else if(ent->nestinglevel==SCOPES->nestinglevel  && ent->type==PARAM && ent->parammode==VALUE){ 
		fprintf(finalfp, "movi R[255], M[R[0] + %d]\n", ent->offset);
		fprintf(finalfp, "movi R[%d], M[R[255]]\n",r);
	}
}

void storerv(char v[MAXLEN], int r)
{
	struct entity *ent;

	ent = search_entity(v);

	//1h periptwsh - an to v einai global	
	if(ent->nestinglevel==0){
		fprintf(finalfp, "movi M[%d], R[%d]\n", 600+ent->offset,r);
	}
	//2h periptwsh - (topikh metavliti)
	else if(ent->nestinglevel==SCOPES->nestinglevel  && ent->type==VARIABLE){ //an h metavlhth einai sto trexon vathos fwliasmatos
		fprintf(finalfp, "movi M[R[0] + %d], R[%d]\n", ent->offset,r);
	}
	//2h periptwsh - (parametros me timi)
	else if(ent->nestinglevel==SCOPES->nestinglevel  && ent->type==PARAM && ent->parammode==VALUE){ 
		fprintf(finalfp, "movi M[R[0] + %d], R[%d]\n", ent->offset,r);
	}
	//3h periptwsh - (parametros me anafora)
	else if(ent->nestinglevel==SCOPES->nestinglevel  && ent->type==PARAM && ent->parammode==VALUE){ 
		fprintf(finalfp, "movi R[255], M[R[0] + %d]\n", ent->offset);
		fprintf(finalfp, "movi M[R[255]], R[%d]\n",r);
	}
}




