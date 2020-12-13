import re

# Patterns to Match With 
varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]*$"
strIdentifier = r"^\".+\"$"
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

# Lists of Compatible Operands
arithOpsList = ["SUMOF","DIFFOF","PRODUKTOF","QUOSHUNTOF","MODOF","BIGGROF","SMALLROF"]
compOpsList = ["BIGGROF","SMALLROF","BOTHSAEM","DIFFRINT"]
relOpsList = [None]
boolOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]

# Global Lists
varDict = {'IT':[None,None]} 


def isVariable(var):					# Checks if the given parameter fits as a variable identifier 
	if re.match(varIdentifier,var):
		return True
	else: return False

def isString(val):
	if re.match(strIdentifier,val):
		return True
	else:
		return False

def isNumber(val):
	if re.match(numIdentifier,val):
		return True
	else:
		return False

def isFloat(val):
	if re.match(floatIdentifier,val):
		return True
	else : 
		return False

def isTroof(val):
	if re.match(troofIdentifier,val):
		return True
	else: 
		return False

def getVarType(value):	# Returns the type of the Variable, Used for Tokenizing Variables
	if isString(value): return "String"
	elif isNumber(value): return "Integer"
	elif isFloat(value): return "Float"
	elif isTroof(value): return "Troof"
	else : return False	

def isLiteral(value):	# Checks for the type of the value, returns a string of its type, Used for Tokenizing Literals

	if isString(value): return "String Literal"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	elif isTroof(value): return "Troof Literal"
	else : return False


def evaluateIfVar(operand):		# Evaluates a possible variable to its value in string format, Used in Operations

	if operand in varDict:					# If the operand is the lsit of variables 
		varVal = varDict[operand][0]		# Get the value and the type 
		operand = str(varVal)

	return operand

def evalVar(var):				# Function for Evaluating Variable value
	if var in varDict:
		val = varDict[var]
		return val[1]			# Returns the 2nd element of the list which is the value 
	else : 
		return False			# If the var is not in the list return False 

def printError(message,lineNumber):
	if lineNumber = "":
		print(message)
	else:
		print("Line: ",lineNumber," ",message)
	exit(1)

## Functions for Arithmetic Expressions =======================================================================================================================

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

def evaluateArithExpr(operator,operand1,operand2):		# Evaluates the Given Arithmetic Expression, Called by Main Arith
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
	elif operator == "BIGGROF":             			# Return the bigger value
		if operand1 > operand2:
			answer = operand1
		elif operand2 > operand1:
			answer = operand2
		else:											#if operands are equal returns operand1 data type and value
			answer = operand1
	elif operator == "SMALLROF":
		if operand1 < operand2:
			answer = operand1
		elif operand2 < operand1:
			answer = operand2
		else:											#if operands are equal returns operand1 data type and value
			answer = operand1
	elif operator == "QUOSHUNTOF":
		try:
			answer = operand1 / operand2
		except ZeroDivisionError:
			print("Zero division error",sourceLines.index(line))
			exit(1)
	else:
		print("Error Unrecognized Arithmetic Operand")
		exit(1)

	return answer		# When conditions are cleared return the final answer 

def mainArith(arithExpr):				# Function for handling arithmetic Expressions and returns the value or an error 
	flag = True							# Flag if running should still continue
	stack = []							# Stack used for computation

	inputLength = len(arithExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = arithExpr.pop(0)
		stack.append(new)   
	
	while flag == True:

		if len(stack) == 1:      # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		for i in range(len(stack)-1):                                       # Len of Stack Refreshes after every iteration
			char = stack[i] 

			if char == "AN":
				anIndex = i
				try:
					print("AN Index: ",anIndex)
					ops = stack[anIndex-2]                  	                 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])                                  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])                                  # Operand 2, 1 step ahead AN 

					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value but in string 

					print("Ops: ",ops," Op1: ",type(op1)," Op2: ",type(op2))
					
					# Handle Possible Variables 
					if (ops in arithOpsList) and isArithOperand(op1) and isArithOperand(op2):
						answer = evaluateArithExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)             # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer                           # Replace OP2 with the answer
						print("Stack after Operation: ",stack)
						break												# Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass



## End of Functions for Arithmetic Expressions =======================================================================================================================

## Functions for Comparison Expressions =======================================================================================================================
def isCompOperand(x):
	if re.match(troofIdentifier,x): return True
	elif re.match(numIdentifier,x): return True
	elif re.match(floatIdentifier,x): return True
	else: return False 

def manageCompKeywords(line):
	keywordListTuple = [("BIGGR OF","BIGGROF"),("SMALLR OF","SMALLROF"),("BOTH SAEM","BOTHSAEM")]
	for keyword in keywordListTuple:
		line = line.replace(keyword[0],keyword[1])
	line = line.split()
	return line

def evaluateCompExpr(operator,operand1,operand2) :

	print("Ops: ",operator," Op1: ",operand1," Op2: ",operand2)
	answer = None

	if isNumber(operand1): operand1 = int(operand1)				# Cast Operand 1 to Its Type
	elif isFloat(operand1) : operand1 = float(operand1)

	if isNumber(operand2): operand2 = int(operand2)				# Cast Operands 2 to Its Type 
	elif isFloat(operand2) : operand2 = float(operand2)

	if operator == "BOTHSAEM":
		if operand1 == operand2: answer = "WIN"     # Win if equal, Fail if not
		else: answer = "FAIL"
	elif operator == "DIFFRINT":
		if operand1 != operand2: answer = "WIN"     # Win if not equal, Fail if not 
		else: answer = "FAIL"

	elif operator == "BIGGROF" and (isinstance(operand1,int) or isinstance(operand1,float)) and  (isinstance(operand2,int) or isinstance(operand2,float)):
		
		answer = max(operand1,operand2)

	elif operator == "SMALLROF" and (isinstance(operand1,int) or isinstance(operand1,float)) and  (isinstance(operand2,int) or isinstance(operand2,float)):

		answer = min(operand1,operand2)
	else:
		print("Error Unrecognized Comparison Operator or Invalid Pair of Operands")
		exit(1)

	return answer

def mainComp(compExpr):
	flag = True							# Flag if running should still continue
	stack = []							# Stack used for computation
										
	inputLength = len(compExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = compExpr.pop(0)
		stack.append(new)   
	
	while flag == True:

		if len(stack) == 1:             # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		for i in range(len(stack)-1):                                       # Len of Stack Refreshes after every iteration
			char = stack[i] 

			if char == "AN":
				anIndex = i
				try:
					print("AN Index: ",anIndex)
					ops = stack[anIndex-2]                  	                 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])                                  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])                                  # Operand 2, 1 step ahead AN 

					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 
		
					if (ops in compOpsList) and isCompOperand(op1) and isCompOperand(op2):
						answer = evaluateCompExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)                  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer                                # Replace OP2 with the answer
						break									        		 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass


## End of Functions for Comparison Expressions =======================================================================================================================