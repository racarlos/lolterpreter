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
	if lineNumber == "":
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
			print("Zero division error",sourceLines.index(line))
			exit(1)
	else:
		print("Error Unrecognized Arithmetic Operand")
		exit(1)

	return answer		# When conditions are cleared return the final answer 

def checkArithExpression(stack,listFlag):	#checks the stack if it's balanced # I should probably change the name for both Arithmetic and Boolean
	countArithKey = 0
	countAnKey = 0
	operationsList= None
	if listFlag == "Arithmetic": operationsList = arithOpsList
	elif listFlag == "Boolean": operationsList = boolOpsList
	elif listFlag == "Comparison": operationsList = compOpsList
	
	for key in stack:
		if key in operationsList: countArithKey+=1
		elif key == "NOT": continue
		elif key == "AN": countAnKey+=1

	#break for ALL OF and ANY OF
	if countArithKey != countAnKey:
		print("Error: Unbalanced pairs of Arithmetic Operands and Operators")
		exit(1)

#constantly checks within the loop the stack and the series of elements in it
def checkStackExpr(stack,listFlag):
	operationsList= None
	if listFlag == "Arithmetic": operationsList = arithOpsList
	elif listFlag == "Boolean": operationsList = boolOpsList
	elif listFlag == "Comparison": operationsList = compOpsList

	if stack[-1] == "AN" or stack[0] == "AN" or stack[1] == "AN":
		print("Syntax Error, Incorrect AN Placement")
		return True
	elif not (stack[0] in operationsList):
		print("Syntax Error, First Element not an Operator")
		return True
	elif stack[-1] in operationsList:
		print("Syntax Error, Last Element is an Operator")
		return True
	else: return False


def mainArith(arithExpr):				# Function for handling arithmetic Expressions and returns the value or an error 
	flag = True							# Flag if running should still continue
	stack = []							# Stack used for computation

	inputLength = len(arithExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = arithExpr.pop(0)
		stack.append(new)   

	# Error Detection here
	checkArithExpression(stack,"Arithmetic")										#Exits if it encounters an error

	while flag == True:

		hasError= checkStackExpr(stack,"Arithmetic")
		if hasError == True : exit(1)									  # Exit if there is an error detected 

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

					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value but in string 

					print("Ops: ",ops," Op1: ",type(op1)," Op2: ",type(op2))
					
					# Handle Possible Variables 
					if (ops in arithOpsList) and isArithOperand(op1) and isArithOperand(op2):
						answer = evaluateArithExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)			 # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer						   # Replace OP2 with the answer
						print("Stack after Operation: ",stack)
						break												# Break Iteration after an operation has completed 
					else:
						pass
				except:
					#printError("Error in Arithmetic Expression",sourceLines.index(line))
					print("Error in Arithmetic Expression")
					exit(1)



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
		if operand1 == operand2: answer = "WIN"	 # Win if equal, Fail if not
		else: answer = "FAIL"
	elif operator == "DIFFRINT":
		if operand1 != operand2: answer = "WIN"	 # Win if not equal, Fail if not 
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
	

	checkArithExpression(stack,"Comparison")
	while flag == True:
		hasError= checkStackExpr(stack,"Comparison")
		if hasError == True : exit(1)									  # Exit if there is an error detected 

		if len(stack) == 1:			 # Only final answer should be left 
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

					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 
		
					if (ops in compOpsList) and isCompOperand(op1) and isCompOperand(op2):
						answer = evaluateCompExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)				  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer								# Replace OP2 with the answer
						break													 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					print("Error in Comparison Expression")
					exit(1)


## End of Functions for Comparison Expressions =======================================================================================================================

## Functions for Boolean Expressions =======================================================================================================================
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


def mainBool(boolExpr):
	flag = True
	stack = []							    # Stack used for computation
										
	inputLength = len(boolExpr)

	for i in range(inputLength):									      # Add every element of String to the stack
		new = boolExpr.pop(0)
		stack.append(new)   
	
	#checkArithExpression(stack,"Boolean")
	while flag == True:

		hasError= checkStackExpr(stack,"Boolean")
		if hasError == True : exit(1)									  # Exit if there is an error detected 

		if len(stack) == 1:                                               # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		for i in range(len(stack)-1):                                     # Len of Stack Refreshes after every iteration
			char = stack[i] 

			if char == "NOT" and isBoolOperand(stack[i+1]):                                             # Not of is separated because it only has 1 operand 
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


## End of Functions for Boolean Expressions =======================================================================================================================
