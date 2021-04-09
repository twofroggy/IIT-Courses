# CS350 - Lab 1
# Tiffany Wong

.data # section that declare variables for program
firststring: .asciiz "You are " 
secondstring: .asciiz " years old."
prompt: .asciiz "Please enter your age and then press enter: " 

.text
.globl main
main:   
    # print prompt on console 
        la $a0, prompt     # address of prompt goes in
        li $v0, 4          # service code for print string
        syscall 

    # read the integer entered and store as age 
        #store int input in $t0
        li $v0, 5          #System call code for Read Integer from input
        syscall
        move $t0, $v0      # $t0 = value from input

    # print a response string identifying the result, and ending with a new line
        la $a0, firststring
        li $v0, 4 #System call code for printing a string
        syscall

        li $v0, 1  #System call to Print Int
        move $a0, $t0 #Move $t0 into $a0
        syscall

        la $a0, secondstring
        li $v0, 4 #System call code for printing a string
        syscall