.data
ms1_msg:.asciiz "Enter the number you want converted to binary form: "

.text
.globl main
main:
    la $a0,ms1_msg    
    li $v0,4
    syscall

    li $v0,5          #user enters number and it is stored in t0
    syscall
    move $t0,$v0

    addi $t1,$zero,1  #t1=1
    addi $t2,$zero,2  #t2=2
    add $t5,$zero,1   #t5=1
    add $t8,$zero,$zero 

    add $t6,$zero,$t0  #t6=1

loop1:            #trying to find the counter for loop 2
    addi $t5,$t5,1    
    div $t0,$t2       
    mflo $t4          
    beq $t4,$t1,loop2 
    sub $t0,$t0,$t0   
    add $t0,$t4,$t0
    j loop1 

loop2:      #twith using the counter (t5) I define how many times loop should circle. 
    addi $t9,$t9,1    
    div $t6,$t2       
    mfhi $t7          
    mflo $t8          
    move $a0, $t7     
    li $v0, 1
    syscall
    beq $t9,$t5,exit
    sub $t6,$t6,$t6   
    add $t6,$t8,$t6 
    j loop2           

    exit:                                      
    li $v0,10       
    syscall