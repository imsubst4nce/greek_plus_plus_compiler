#include <stdio.h>

int main()
{
int α ;
int β ;
int ι ;
int t$1 ;
int τ ;
int t$2 ;
int π ;
int t$3 ;
int t$4 ;

L1: 
L2: α=0;
L3: β=1;
L4: ι=0;
L5: if (ι <= 10) goto L7;
L6: goto L15;
L7: printf("%d\n",α);
L8: t$1=α+β;
L9: τ=t$1;
L10: α=β;
L11: β=τ;
L12: t$2=ι+1;
L13: ι=t$2;
L14: goto L5;
L15: π=1;
L16: ι=1;
L17: printf("%d\n",π);
L18: t$3=π*ι;
L19: π=t$3;
L20: t$4=ι+1;
L21: ι=t$4;
L22: if (ι > 7) goto L24;
L23: goto L17;
L24: 
L25: 
}

