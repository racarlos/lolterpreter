import re
from helperFuncs import * 

boolOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]


def isBoolOperand(x):
	if re.match(troofIdentifier,x):
		return True
	else:
		return False

def manageBoolKeywords(line):
	keywordListTuple = [("BOTH OF","BOTHOF"),("EITHER OF","EITHEROF"),("WON OF","WONOF"),("ANY OF","ANYOF"),("ALL OF","ALLOF")]
	for keyword in keywordListTuple:
		line = line.replace(keyword[0],keyword[1])
	line = line.split()
	return line

def evaluateBoolExpr(operator,operand1,operand2):

	print("Ops: ",operator," Op1: ",operand1," Op2: ",operand2)

	if operand1 == "WIN": operand1 = True				# Cast to Boolean Type to take advantage of pythhon operations
	elif operand1 == "FAIL": operand1 = False

	if operand2 == "WIN": operand2 = True				
	elif operand2 == "FAIL": operand2 = False

	if operator == "BOTHOF":
		answer = operand1 and operand2
	elif operator == "EITHEROF":
		answer = operand1 or operand2
	elif operator == "WONOF":               # XOR is similar to !=
		if operand1 != operand2: answer = True
		else: answer = False
	else:
		print("Unrecognized boolean operator")
		exit(1)
	
	if answer == True: answer = "WIN"
	elif answer == False: answer = "FAIL"

	return answer


def boolMain(boolExpr):
	flag = True
	stack = []							    # Stack used for computation
										
	inputLength = len(boolExpr)

	for i in range(inputLength):									      # Add every element of String to the stack
		new = boolExpr.pop(0)
		stack.append(new)   
	
	while flag == True:

		# Error Conditions : First Element is AN or not an Operator or last element is AN or Operator

		if stack[-1] == "AN" or stack[-1] in boolOpsList or not(stack[0] in boolOpsList) or stack[0] == "AN" or stack[1] == "AN":			# Exit if the last element is An or Operator 
			print("Syntax Error Boolean Operation - Precheck")
			exit(1)		

		if len(stack) == 1:                                               # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		for i in range(len(stack)-1):                                     # Len of Stack Refreshes after every iteration
			char = stack[i] 

			if char == "NOT":                                             # Not of is separated because it only has 1 operand 
				valid = True
				try:
					ops = stack[i]
					op1 = stack[i+1]

					# Evaluate op1 if variable 

					if isBoolOperand(op1) and op1 == "WIN":	
						answer = "FAIL"
					elif isBoolOperand(op1) and op1 == "FAIL": 
						answer = "WIN"
					else : 
						valid = False
						print("Invalid NOT Operand")
						exit(1)

					stack.pop(i)                                            # Pop the not of
					stack[i] = answer
				except: 
					pass

				if valid == False: exit(1)

			elif char == "ALLOF":                                           #  Infinite Arity And
				valid = True
				try:
					start = i
					ops = stack[i]
					end = False

					for m in stack: 										# Traverse the stack and find its matching MKAY
						if m == "MKAY": 
							end = stack.index(m)	
							break						
					
					if end != False:
						
						while stack[i+2] != "MKAY":
							ops = "BOTHOF"									# ALL OF is a reeated form of BOTH OF 
							op1 = str(stack[i+1])
							op2 = str(stack[i+3])
	
							if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
								answer = evaluateBoolExpr(ops,op1,op2)
								for j in range(2): stack.pop(i+1)
								stack[i+1] = answer
								continue									
							else: 
								print("ERROR ====================",stack)
								pass
						
						stack.pop(i+2)				# pop MKAY
						stack.pop(i)				# pop ALL OF 
						print(stack)
						break						# break out of outer loop to refresh count
						

					elif end == False:
						valid = False
						print("Error in All OF, matching MKAY not found.")
				
				except:
					pass

				if valid == False: exit(1)


			elif char == "ANYOF":                                           	 # Infinite Arity Or
				valid = True													
				try:
					start = i
					ops = stack[i]
					end = False

					for m in stack: 										# Traverse the stack and find its matching MKAY
						if m == "MKAY": 
							end = stack.index(m)	
							break						
					
					if end != False:
						
						while stack[i+2] != "MKAY":
							ops = "EITHEROF"									# ANY OF is a reeated form of EITHER OF 
							op1 = str(stack[i+1])
							op2 = str(stack[i+3])
	
							if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
								answer = evaluateBoolExpr(ops,op1,op2)
								for j in range(2): stack.pop(i+1)
								stack[i+1] = answer
								continue									
							else: 
								print("ERROR ====================",stack)
								pass
						
						stack.pop(i+2)				# pop MKAY
						stack.pop(i)				# pop ANY OF 
						print(stack)
						break						# break out of outer loop to refresh count
						

					elif end == False:
						print("Error in ANY OF, matching MKAY not found.")
						valid = False
				except:
					pass

				if valid == False: exit(1)


			elif char == "AN":
				valid = True
				anIndex = i

				if stack.index(stack[i]) == 0 or stack.index(stack[i]) == 1: 
					print("Boolean Operation Syntax Error")
					valid = False
		
				try:
					print("AN Index: ",anIndex)
					ops = stack[anIndex-2]                  	                 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])                                  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])                                  # Operand 2, 1 step ahead AN 

					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 
		
					if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
						answer = evaluateBoolExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)                  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer                                # Replace OP2 with the answer
						break									        		 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass

				if valid == False: exit(1)


str1 = "AN WOW"
str2 = "NOT FAIL"
str3 = "BOTH OF BOTH OF WIN AN WIN AN BOTH OF WIN AN FAIL"
str4 = "EITHER OF FAIL AN FAIL"
str5 = "WON OF WIN AN WIN"

str6 = "WIN AN BOTH OF WIN AN FAIL AN"

sample = manageBoolKeywords(str2)
print(sample)
final = boolMain(sample)
print("Final Answer: ",final)