.data # Text prompts and data for calculator function
	# Prompts:
	prompt: .asciiz "Before using this calculator, please read the User Manual instructions to know how to operate it.\n"
	input_request: .asciiz "Please enter an integer: "
	input_request1: .asciiz "Please enter the first integer : "
	input_request2: .asciiz "Please enter the second integer: "
	current_result: .asciiz "Your current result is: "
	operation_request: .asciiz "Please enter an operator key: "
	operation_request2: .asciiz "\nPlease enter an operator key: "
	final_result: .asciiz "Final result: "


.text # Main project components
	main: # Main program operation
		welcome: # Welcome prompt for user.
			li $v0, 4
			la $a0, prompt 
			syscall #prompt presented to user.
			
			j first_operation
			
		first_operation: # User's first operation.
			li $v0, 4
			la $a0, input_request1
			syscall # The user is prompted to enter a first integer value.
			
			li $v0, 5
			syscall
			move $s0, $v0 # The user's first integer is stored.
			
			li $v0, 4
			la $a0, operation_request
			syscall # The user is prompted to enter an operator key.
			
			li $v0, 5
			syscall
			move $s1, $v0 # The user's operator key is stored.
			
			# If user wants to terminate:
			beq $s1, 0, end
			
			# If square:
			beq $s1, 6, square
			
			# If factorial:
			beq $s1, 7, fact
			
			# If clear:
			beq $s1, 8, clear
			
			li $v0, 4
			la $a0, input_request2
			syscall # The user is prompted to enter a second integer value.
			
			li $v0, 5
			syscall
			move $s2, $v0 # The user's second integer is stored.
			
			# If addition:
			beq $s1, 1, adding
			
			# If subtraction:
			beq $s1, 2, subtract
			
			# If multiplication:
			beq $s1, 3, multiply
			
			# If division:
			beq $s1, 4, divide
			
			# If modulus:
			beq $s1, 5, mod
			
			
		adding: # Addition operation (1)
			add  $s0, $s0, $s2
			
			j result
		
		subtract: # Subtraction operation (2)
			sub $s0, $s0, $s2
			
			j result
			
		multiply: # Multiplication operation (3)
			mult $s0, $s2
			mflo $s0
			
			j result
			
		divide: # Division operation (4)
			div $s0, $s2
			mflo $s0
			
			j result
		
		mod: # Modulus operation (5)
			div $s0, $s2
			mfhi $s0
			
			j result
		
		square: # Square operation (6)
			mult $s0, $s0
			mflo $s0
			
			j result
		
		fact: # Factorial operation (7)
			move $t0, $s0 # Move first integer to temporary register
			while:
				
				beq $t0, 1, result # If temp value = 1, go to result
				beq $t0, 0, zero_fact # If temp value = 0, go to zero_fact
				blt $t0, 0, result # If temp value <0, go to result
				
				sub $t0, $t0, 1
				mult $s0, $t0
				mflo $s0
			
				j while
				
			zero_fact:
				add $s0, $s0, 1
				
				j result
			
		clear: # Clear operation (8)
			la $s0, ($zero) 
			
			j result
		
		result: # Result of an operation:
			li $v0, 4
			la $a0, current_result
			syscall 
			
			li $v0, 1
			move $a0, $s0
			syscall
			
			j operate
		
		operate: # Continuation of operation:
			li $v0, 4
			la $a0, operation_request2
			syscall # The user is prompted to enter an operator key.
			
			li $v0, 5
			syscall
			move $s1, $v0 # The user's operator key is stored.
			
			# If user wants to terminate:
			beq $s1, 0, end
			
			# If square:
			beq $s1, 6, square
			
			# If factorial:
			beq $s1, 7, fact
			
			# If clear:
			beq $s1, 8, clear
			
			li $v0, 4
			la $a0, input_request
			syscall # The user is prompted to enter integer value.
			
			li $v0, 5
			syscall
			move $s2, $v0 # The user's integer is stored.
			
			
			# If addition:
			beq $s1, 1, adding
			
			# If subtraction:
			beq $s1, 2, subtract
			
			# If multiplication:
			beq $s1, 3, multiply
			
			# If division:
			beq $s1, 4, divide
			
			# If modulus:
			beq $s1, 5, mod

		end: # End of program:
			li $v0, 4
			la $a0, final_result
			syscall 
			
			li $v0, 1
			move $a0, $s0
			syscall
			
			li, $v0, 10
			syscall
			