from helperFuncs import *

## Functions for Arithmetic Expressions 

def isArithOperand(value):	# Just like isLiteral but specific for arithmetic operands 
	if isVariable(value): return "Variable Identifier"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	else : return False

def evalArithOperand(operand):
	if isNumber(operand): return int(operand)
	elif isFloat(operand): return float(operand)
	elif isVariable(operand):			#key is string
		operand = evalVar(operand)
		if type(operand) is int or type(operand) is float:
			return operand
		else:
			print("Error operand is not Numbr or Numbar")
			exit(1)

def manageArithKeywords(line):        		# Make function to convert ops to 1 word operations  EX : SUM OF - > SUMOF, Called by Main arith
	
	keywordListTuple = [("SUM OF","SUMOF"),("DIFF OF","DIFFOF"),("QUOSHUNT OF","QUOSHUNTOF"),("PRODUKT OF","PRODUKTOF"),("MOD OF","MODOF"),("BIGGR OF","BIGGROF"),("SMALLR OF","SMALLROF")]
	for keyword in keywordListTuple:	# Replace keywords to corresponding change to allow string split and store each word as an element 
		line = line.replace(keyword[0], keyword[1])
	line = line.split()
	return line

def evaluateArithExpr(operator,operand1,operand2,lineNumber):		# Evaluates the Given Arithmetic Expression, Called by Main Arith
	operand1 = evalArithOperand(operand1)				#handle data type of operand
	operand2 = evalArithOperand(operand2)

	if operator == "SUMOF":
		answer = operand1 + operand2
	elif operator == "DIFFOF":
		answer = operand1 - operand2
	elif operator == "PRODUKTOF":
		answer = operand1 * operand2
	elif operator == "MODOF":
		answer = operand1 % operand2
	elif operator == "BIGGROF":			 			# Return the bigger value
		if operand1 == operand2:											#if operands are equal returns operand1 data type and value
			answer = operand1
		else:
			answer = max(operand1,operand2)
	elif operator == "SMALLROF":
		if operand1 == operand2:											#if operands are equal returns operand1 data type and value
			answer = operand1
		else:
			answer = min(operand1,operand2)
	elif operator == "QUOSHUNTOF":
		try:
			answer = operand1 / operand2
		except ZeroDivisionError:
			printError("Zero division error",lineNumber)

	else:
		printError("Error Unrecognized Arithmetic Operand",lineNumber)

	return answer		# When conditions are cleared return the final answer 



def mainArith(arithExpr,lineNumber):				# Function for handling arithmetic Expressions and returns the value or an error 
	flag = True							# Flag if running should still continue
	stack = []							# Stack used for computation

	inputLength = len(arithExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = arithExpr.pop(0)
		stack.append(new)   

	# Error Detection here
	checkExpression(stack,"Arithmetic",lineNumber)										#Exits if it encounters an error

	while flag == True:

		hasError = checkStackExpr(stack,"Arithmetic")

		if hasError == True :														  # Exit if there is an error detected 
			printError("Error in Comparison Expression",lineNumber)

		if len(stack) == 1:	  # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		for i in range(len(stack)-1):									   # Len of Stack Refreshes after every iteration
			char = stack[i] 

			if char == "AN":
				anIndex = i
				try:
					print("AN Index: ",anIndex)
					ops = stack[anIndex-2]				  					 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])								  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])								  # Operand 2, 1 step ahead AN 

					op1 = str(evaluateIfVar(op1))								 # Checks if the Operands are Possible Variables  
					op2 = str(evaluateIfVar(op2))									 # then evaluates them to their value but in string 

					print("Ops: ",ops," Op1: ",op1," Op2: ",op2)
					
					# Handle Possible Variables 
					if (ops in arithOpsList) and isArithOperand(op1) and isArithOperand(op2):
						answer = evaluateArithExpr(ops,op1,op2,lineNumber)
						for j in range(3): stack.pop(anIndex-2)			 # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer						   # Replace OP2 with the answer
						print("Stack after Operation: ",stack)
						break												# Break Iteration after an operation has completed 
					else:
						pass
				except:
					printError("Error in Arithmetic Expression",lineNumber)
	