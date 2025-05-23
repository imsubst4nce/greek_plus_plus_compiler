

# sort array of N integers
# located at the first 4*N bytes

	.data  
str_nl: .asciz "\n"
	.text


main:
	li t0,1
	sw t0,0(sp)
	li t0,2
	sw t0,4(sp)
	li t0,3
	sw t0,8(sp)
	li t0,4
	sw t0,12(sp)
	li t0,5
	sw t0,16(sp)
	

input:	li a7, 5			# input N
	ecall
	
init:	li t0, 4			# initialization of index1(s1)
	mul s1, a0, t0
	addi s1,s1,-8		
	
main_loop:	
	li s2,0				# initialization of index2(s2)

	inner_loop:
		add t0,sp,s2
		lw t1,(t0)
		lw t2,4(t0)
		bge t1,t2,after_swap
	swap:	
		sw t1,4(t0)
		sw t2,(t0)
	
	after_swap:
		addi s2,s2,4
		ble s2,s1,inner_loop
		addi s1,s1,-4
		bge s1,zero,main_loop
		
		
exit:	
        li a0, 0			# the end
        li a7,93	
        ecall
