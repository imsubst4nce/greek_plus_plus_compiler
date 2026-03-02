

        .data  
str_nl: .asciz "\n"


	.text
main:



print:
	li a0,42
	li a7, 1			
	ecall
	la a0,str_nl
	li a7, 4			
	ecall

inputAndPrint:
	li a7, 5			
	ecall
	li a7, 1			
	ecall
	la a0,str_nl
	li a7, 4			
	ecall
	

exit:
        li a0, 0		
        li a7,93	
        ecall			

