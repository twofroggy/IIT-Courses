# CS350 - Lab 2
# Tiffany Wong

.data
askA: .asciiz "\nEnter a : "
askB: .asciiz "\nEnter b : "
askC: .asciiz "\nEnter c : "
askX: .asciiz "\nEnter x : "
result: .asciiz "\nResult is : "

.text
.globl main

main:
    li $v0, 4        # service code for print string
    la $a0, askA     #it will print prompt
    syscall
    li $v0, 5        #System call code for Read Integer from input
    syscall          #ask user input
    move $t1, $v0    #save a to t1

    li $v0, 4        # service code for print string
    la $a0, askB     #it will print prompt
    syscall
    li $v0, 5        #System call code for Read Integer from input
    syscall          #ask user input
    move $t2, $v0    #save b to t2

    li $v0, 4        # service code for print string
    la $a0, askC     #it will print prompt
    syscall
    li $v0, 5        #System call code for Read Integer from input
    syscall          #ask user input
    move $t3, $v0    #save c to t3

    li $v0, 4        # service code for print string
    la $a0, askX     #it will print prompt
    syscall
    li $v0,5         #System call code for Read Integer from input
    syscall          #ask user input
    move $t4, $v0    #save x to t4

    mul $s0,$t4,$t4  #get x square and save to s0
    mul $s0,$s0,$t1  #get a*x^2 and save to s0

    mul $s1,$t2,$t4  # get bx and save to s1

    add $s2,$s0,$s1  # get a x^2 + bx and save to s2
    add $s2,$s2,$t3  # get a x^2 + bx + c and save to s2


    li $v0, 4        # service code for print string
    la $a0, result   #it will print prompt for result
    syscall

    li $v0, 1        # system call code for print_int
    move $a0, $s2    # move the polynomial's result to a0
    syscall