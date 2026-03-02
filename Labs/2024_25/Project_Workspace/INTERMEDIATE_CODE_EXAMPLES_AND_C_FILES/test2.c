#include <stdio.h>

int main()
{
int α ;
int t$1 ;
int β ;
int t$2 ;
int t$3 ;
int t$4 ;
int t$5 ;
int t$6 ;

L1: 
L2: α=1;
L3: if (α < 10) goto L5;
L4: goto L8;
L5: t$1=α+1;
L6: α=t$1;
L7: goto L3;
L8: printf("%d\n",α);
L9: β=α;
L10: t$2=β+1;
L11: β=t$2;
L12: t$3=β-2;
L13: β=t$3;
L14: if (β == 0) goto L16;
L15: goto L10;
L16: printf("%d\n",β);
L17: t$4=0-1;
L18: if (β <= t$4) goto L20;
L19: goto L23;
L20: t$5=0-1;
L21: α=t$5;
L22: goto L25;
L23: t$6=0-2;
L24: α=t$6;
L25: printf("%d\n",α);
L26: if (α < β) goto L28;
L27: goto L30;
L28: α=1;
L29: goto L31;
L30: α=2;
L31: printf("%d\n",α);
L32: 
L33: 
}

