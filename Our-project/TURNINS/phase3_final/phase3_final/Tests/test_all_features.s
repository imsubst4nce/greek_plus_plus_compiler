  # Initialize 
  mv fp, sp

# jump stin main  
j L12

L1: 
  sw ra, 0(sp)
  # Frame length: 24
  # Initializing local variables space
L2: 
  lw t1, -12(sp)
  lw t2, -16(sp)
  mul t1, t1, t2
  sw t1, -40(gp)
L3: 
  lw t1, -40(gp)
  lw t0, -8(sp)
  sw t1, 0(t0)
L4: 
  lw ra, 0(sp)
  jr ra
L5: 
  sw ra, 0(sp)
  # Frame length: 16
  # Initializing local variables space
L6: 
  lw t1, -12(sp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L7: 
  lw ra, 0(sp)
  jr ra
L8: 
  sw ra, 0(sp)
  # Frame length: 20
  # Initializing local variables space
L9: 
  lw t1, -12(sp)
  li t2, 1
  add t1, t1, t2
  sw t1, -44(gp)
L10: 
  lw t1, -44(gp)
  sw t1, -12(sp)
L11: 
  lw ra, 0(sp)
  jr ra
L12: 
  addi sp, sp, 120
  mv gp, sp
L13: 
  li t1, 5
  sw t1, -12(gp)
L14: 
  li t1, 10
  sw t1, -16(gp)
L15: 
  lw t1, -12(gp)
  lw t2, -16(gp)
  add t1, t1, t2
  sw t1, -48(gp)
L16: 
  lw t1, -48(gp)
  sw t1, -20(gp)
L17: 
  lw t1, -20(gp)
  lw t2, -12(gp)
  sub t1, t1, t2
  sw t1, -52(gp)
L18: 
  lw t1, -52(gp)
  sw t1, -24(gp)
L19: 
  lw t1, -12(gp)
  lw t2, -16(gp)
  mul t1, t1, t2
  sw t1, -56(gp)
L20: 
  lw t1, -56(gp)
  li t2, 2
  div t1, t1, t2
  sw t1, -60(gp)
L21: 
  lw t1, -60(gp)
  sw t1, -28(gp)
L22: 
  lw t1, -20(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L23: 
  lw t1, -24(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L24: 
  lw t1, -28(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L25: 
  # Setting up frame pointer for πολλαπλασίασε
  addi fp, sp, 24
  lw t0, -12(gp)
  sw t0, -12(fp)
L26: 
  lw t0, -16(gp)
  sw t0, -16(fp)
L27: 
  addi t0, gp, -64
  sw t0, -8(fp)
L28: 
  # Setting up static link for πολλαπλασίασε
  lw t0, -4(sp)
  sw t0, -4(fp)
  # Calling function πολλαπλασίασε
  addi sp, sp, 24
  jal L1
  # Getting return value from function πολλαπλασίασε
  lw t0, -8(sp)
  lw t1, 0(t0)
  sw t1, 0(t0)
  addi sp, sp, -24
L29: 
  lw t1, -64(gp)
  sw t1, -32(gp)
L30: 
  lw t1, -32(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L31: 
  # Setting up frame pointer for εμφάνισε_μήνυμα
  addi fp, sp, 16
  lw t0, -32(gp)
  sw t0, -12(fp)
L32: 
  # Setting up static link for εμφάνισε_μήνυμα
  lw t0, -4(sp)
  sw t0, -4(fp)
  # Calling procedure εμφάνισε_μήνυμα
  addi sp, sp, 16
  jal L5
  addi sp, sp, -16
L33: 
  li t1, 0
  sw t1, -36(gp)
L34: 
  # Setting up frame pointer for αύξησε_κατά_ένα
  addi fp, sp, 20
  addi t0, gp, -36
  sw t0, -12(fp)
L35: 
  # Setting up static link for αύξησε_κατά_ένα
  lw t0, -4(sp)
  sw t0, -4(fp)
  # Calling procedure αύξησε_κατά_ένα
  addi sp, sp, 20
  jal L8
  addi sp, sp, -20
L36: 
  lw t1, -36(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L37: 
  li t1, 0
  sw t1, -36(gp)
L38: 
  li t1, 1
  sw t1, -12(gp)
L39: 
  li t1, 5
  sw t1, -68(gp)
L40: 
  li t1, 1
  sw t1, -72(gp)
L41: 
  lw t1, -12(gp)
  lw t2, -68(gp)
  ble t1, t2, L43
L42: 
  b L48
L43: 
  lw t1, -36(gp)
  lw t2, -12(gp)
  add t1, t1, t2
  sw t1, -76(gp)
L44: 
  lw t1, -76(gp)
  sw t1, -36(gp)
L45: 
  lw t1, -12(gp)
  lw t2, -72(gp)
  add t1, t1, t2
  sw t1, -80(gp)
L46: 
  lw t1, -80(gp)
  sw t1, -12(gp)
L47: 
  b L41
L48: 
  lw t1, -36(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L49: 
  li t1, 0
  sw t1, -36(gp)
L50: 
  li t1, 0
  sw t1, -12(gp)
L51: 
  li t1, 10
  sw t1, -84(gp)
L52: 
  li t1, 2
  sw t1, -88(gp)
L53: 
  lw t1, -12(gp)
  lw t2, -84(gp)
  ble t1, t2, L55
L54: 
  b L60
L55: 
  lw t1, -36(gp)
  lw t2, -12(gp)
  add t1, t1, t2
  sw t1, -92(gp)
L56: 
  lw t1, -92(gp)
  sw t1, -36(gp)
L57: 
  lw t1, -12(gp)
  lw t2, -88(gp)
  add t1, t1, t2
  sw t1, -96(gp)
L58: 
  lw t1, -96(gp)
  sw t1, -12(gp)
L59: 
  b L53
L60: 
  lw t1, -36(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L61: 
  li t1, 1
  sw t1, -12(gp)
L62: 
  li t1, 0
  sw t1, -36(gp)
L63: 
  lw t1, -12(gp)
  li t2, 5
  ble t1, t2, L65
L64: 
  b L70
L65: 
  lw t1, -36(gp)
  lw t2, -12(gp)
  add t1, t1, t2
  sw t1, -100(gp)
L66: 
  lw t1, -100(gp)
  sw t1, -36(gp)
L67: 
  lw t1, -12(gp)
  li t2, 1
  add t1, t1, t2
  sw t1, -104(gp)
L68: 
  lw t1, -104(gp)
  sw t1, -12(gp)
L69: 
  b L63
L70: 
  lw t1, -36(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L71: 
  li t1, 1
  sw t1, -12(gp)
L72: 
  li t1, 0
  sw t1, -36(gp)
L73: 
  lw t1, -36(gp)
  lw t2, -12(gp)
  add t1, t1, t2
  sw t1, -108(gp)
L74: 
  lw t1, -108(gp)
  sw t1, -36(gp)
L75: 
  lw t1, -12(gp)
  li t2, 1
  add t1, t1, t2
  sw t1, -112(gp)
L76: 
  lw t1, -112(gp)
  sw t1, -12(gp)
L77: 
  lw t1, -12(gp)
  li t2, 5
  bgt t1, t2, L79
L78: 
  b L73
L79: 
  lw t1, -36(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L80: 
  li t1, 5
  sw t1, -12(gp)
L81: 
  li t1, 10
  sw t1, -16(gp)
L82: 
  lw t1, -12(gp)
  lw t2, -16(gp)
  blt t1, t2, L84
L83: 
  b L86
L84: 
  li t1, 1
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L85: 
  b L86
L86: 
  lw t1, -12(gp)
  lw t2, -16(gp)
  bgt t1, t2, L88
L87: 
  b L90
L88: 
  li t1, 1
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L89: 
  b L91
L90: 
  li t1, 0
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L91: 
  lw t1, -12(gp)
  lw t2, -16(gp)
  blt t1, t2, L93
L92: 
  b L97
L93: 
  lw t1, -12(gp)
  li t2, 0
  bgt t1, t2, L95
L94: 
  b L97
L95: 
  li t1, 1
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L96: 
  b L97
L97: 
  lw t1, -12(gp)
  lw t2, -16(gp)
  bgt t1, t2, L101
L98: 
  b L99
L99: 
  lw t1, -16(gp)
  li t2, 0
  bgt t1, t2, L101
L100: 
  b L103
L101: 
  li t1, 1
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L102: 
  b L103
L103: 
  li t1, 100
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L104: 
  li a7, 5
  ecall
  mv t1, a0
  sw t1, -12(gp)
L105: 
  lw t1, -12(gp)
  mv a0, t1
  li a7, 1
  ecall
  li a0, 10
  li a7, 11
  ecall
L106: 
  li a0, 0
  li a7, 93
  ecall
L107: 
