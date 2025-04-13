#include <stdio.h>

int main()
{
int income ;
int tax ;
int t$1 ;
int t$2 ;
int t$3 ;
int t$4 ;
int t$5 ;
int t$6 ;
int t$7 ;
int t$8 ;
int t$9 ;
int t$10 ;
int t$11 ;
int t$12 ;
int t$13 ;
int t$14 ;
int t$15 ;

L1: 
L2: scanf("%d",&income);
L3: if (income <= 10000) goto L5;
L4: goto L7;
L5: tax=0;
L6: goto L31;
L7: if (income <= 30000) goto L9;
L8: goto L13;
L9: t$1=income-10000;
L10: t$2=t$1/10;
L11: tax=t$2;
L12: goto L31;
L13: if (income <= 70000) goto L15;
L14: goto L22;
L15: t$3=30000-10000;
L16: t$4=t$3/10;
L17: t$5=income-30000;
L18: t$6=t$5/5;
L19: t$7=t$4+t$6;
L20: tax=t$7;
L21: goto L31;
L22: t$8=30000-10000;
L23: t$9=t$8/10;
L24: t$10=70000-30000;
L25: t$11=t$10/5;
L26: t$12=t$9+t$11;
L27: t$13=income-70000;
L28: t$14=t$13/2;
L29: t$15=t$12+t$14;
L30: tax=t$15;
L31: printf("%d\n",tax);
L32: 
L33: 
}

