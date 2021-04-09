.data
    programExitMsg: .asciiz "\nProgram exits.\n"
    evenNumberMsg: .asciiz "\nThe number is even.\n"
    userMsg: .asciiz "\nEnter an integer (0 to exit): "
    oddNumberMsg: .asciiz "\nThe number is odd.\n"

.text
loopIterate:
    #print the prompt string
    la $a0, userMsg
    li $v0, 4
    syscall

    # get the user input
    li $v0, 5
    syscall

    # If number is 0(zero), exit program.
    beq $v0,$zero,programExit

    # pass the value stored in $v0 to label findEvenOrOdd
    add $a0, $v0, $zero
    jal findEvenOrOdd
    #goto the begining of the loop
    j loopIterate

findEvenOrOdd:
   #set the value to 2 as divisor to find even or odd number
    addi $t0, $zero, 2
    div $a0, $t0
    #store the reminder in $t0, which is present in high register
    mfhi $t0
    #if $t0 ois zero, then its even number, else odd number   
    beq $t0, $zero, evenLabel
    j oddLabel

evenLabel:
   #print the even number message
    la $a0, evenNumberMsg   
    li $v0, 4
    syscall
    j retlabel
oddLabel:  
   #print the odd number message
    la $a0, oddNumberMsg
    li $v0, 4
    syscall
    j retlabel

retlabel:
   #adjust the stack pointer and return to callee
    lw $t0, 0($sp)
    addi $sp, $sp, 4
    jr $ra

programExit:
    la $a0, programExitMsg
    li $v0, 4
    syscall
   #exit the program by load immediate
    li $v0, 10
    syscall