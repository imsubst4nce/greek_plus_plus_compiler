//PAPAKALOUSI NATALIA 1391
//SKALIDIS DIMITRIS 1264

#include <stdio.h>
#include <stdlib.h>
#include <ctype.h>

#define MAXLEN 		31 	//30 xarakthres kai \0

#define EOFTK		-1	// kwdikos oti sunantisa to telos tou arxeiou
#define ERROR		-2	// error	
#define E1		-3	// anagnwristiko h desmeumenh lexh
#define E2		-4	// akeraia stathera
#define E3		-5	// pragmatikh stathera


#define ADDTK		100	// +
#define MINUSTK		101	// -
#define TIMESTK		102	// *
#define DIVTK		103	// /
#define EQTK		104	// =
#define LESSTK		105	// <
#define DIFFTK		106	// <>
#define LESSEQTK	107	// <=
#define TWODOTSTK	108	// :
#define QMARKTK		109	// ;
#define COMMATK		110	// ,
#define PERTK		111	// %
#define MORETK		112	// >
#define MOREEQTK	113	// >=
#define ASSIGNTK	114	// :=
#define IDTK		115	// anagnwristiko
#define CONSTTK		116	// akeraia stathera
#define REALTK		117	// pragmatikos arithmos
#define LPARTK		118	// (
#define RPARTK		119	// )
#define LBRATK		120	// [
#define RBRATK		121	// ]

//desmeumenes lexeis
#define PROGRAMATK	130	// programa
#define EANTK		131	// ean	
#define EPANALABETK	132	// epanalave
#define GIATK		133	// gia
#define GRAPSETK	134	// grapse
#define EISODOSTK	135	// eisodos
#define TELOSSYNARTISISTK 136	// telossynartisis
#define HTK		137	// H
#define DILOSEISTK	138	// diloseis
#define TOTETK		139	// tote
#define MEXRITK		140	// mexri
#define EOSTK		141	// eos
#define SYNARTISITK	142	// synartisi
#define EXODOSTK	143	// exodos
#define KAITK		144	// kai	
#define AKERAIOSTK	145	//akeraios
#define ALLIOSTK	146	//allios
#define OSOTK		147	//oso
#define MEBIMATK	148	//me_bima
#define DIADIKASIATK	149	//diadikasia
#define ARXITK		150	//arxi
#define TELOSDIADIKASIASTK 151 	//telosdiadikasia
#define OXITK		152	//oxi
#define PRAGMATIKOSTK	153	//pragmatikos
#define EANTELOSTK	154	//ean_telos
#define OSOTELOSTK	155	//oso_telos
#define DIABASETK	156	//diabase
#define DIAPROSOPIATK	157	//diaprosopia
#define TELOSTK		158	//telos
#define EKTELESETK	159	//ektelese
#define GIATELOSTK	160	//gia_telos

