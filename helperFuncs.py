from patterns import * 
import re

# Patterns to Match With for a lexeme
varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]*$"
strIdentifier = r"\".+\""
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

# Global Lists
varDict = {'IT':[None,None]} 

def printError(message,lineNumber):
	if lineNumber == "":
		print(message)
	else:
		print("Line:",lineNumber,"",message)
	exit(1)

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
	if isNumber(value): return "Integer"
	elif isFloat(value): return "Float"
	elif isTroof(value): return "Troof"
	elif isString(value): return "String"
	else : return False	

def isLiteral(value):	# Checks for the type of the value, returns a string of its type, Used for Tokenizing Literals

	if isString(value): return "String Literal"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	elif isTroof(value): return "Troof Literal"
	else : return False

def isExpression(expr):

	if re.match(sumof,expr) or re.match(diffof,expr) or re.match(produktof,expr) or re.match(quoshuntof,expr) or re.match(modof,expr) or re.match(biggrof,expr) or re.match(smallrof,expr):
		print("Matched With Arithmetic Expression",expr)
		return True
	elif re.match(bothsaem,expr) or re.match(diffrint,expr):
		print("Matched With Comparison Expression")
		return True
	elif re.match(notop,expr) or re.match(eitherof,expr) or re.match(bothof,expr) or re.match(wonof,expr) or re.match(allof,expr) or re.match(anyof,expr):
		print("Matched With Boolean Expression",expr)
		return True
	else:
		#print("Did not match with any expression: ",expr)
		return False

def evaluateIfVar(operand):		# Evaluates a possible variable to its value in string format, Used in Operations

	if operand in varDict:					# If the operand is the lsit of variables 
		varVal = varDict[operand][1]		# Get the value and the type 
		operand = str(varVal)

	return operand

def evalVar(var):				# Function for Evaluating Variable value
	if var in varDict:
		val = varDict[var]
		return val[1]			# Returns the 2nd element of the list which is the value 
	else : 
		return False			# If the var is not in the list return False 



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

def checkExpression(stack,listFlag,lineNumber):	#checks the stack if it's balanced
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
		printError("Error: Unbalanced pairs of Arithmetic Operands and Operators",lineNumber)

#constantly checks within the loop the stack and the series of elements in it
def checkStackExpr(stack,listFlag):
	operationsList= None
	if listFlag == "Arithmetic": operationsList = arithOpsList
	elif listFlag == "Boolean": operationsList = boolOpsList
	elif listFlag == "Comparison": operationsList = compOpsList

	try:
		if stack[-1] == "AN" or stack[0] == "AN" or stack[1] == "AN":
			print("Syntax Error,",listFlag," Incorrect AN Placement")
			return True
		elif not (stack[0] in operationsList):
			print("Syntax Error,",listFlag," First Element not an Operator")
			return True
		elif stack[-1] in operationsList:
			print("Syntax Error,",listFlag," Last Element is an Operator")
			return True
	except:
		pass


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

def evaluateCompExpr(operator,operand1,operand2,lineNumber) :

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
		printError("Error Unrecognized Comparison Operator or Invalid Pair of Operands",lineNumber)


	return answer

def mainComp(compExpr,lineNumber):
	flag = True							# Flag if running should still continue
	stack = []							# Stack used for computation
										
	inputLength = len(compExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = compExpr.pop(0)
		stack.append(new)   
	
	checkExpression(stack,"Comparison",lineNumber)

	while flag == True:
		hasError = checkStackExpr(stack,"Comparison")

		if hasError == True :											  # Exit if there is an error detected 
			printError("Error in Comparison Expression",lineNumber)

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
						answer = evaluateCompExpr(ops,op1,op2,lineNumber)
						for j in range(3): stack.pop(anIndex-2)				  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer								# Replace OP2 with the answer
						break													 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					printError("Error in Comparison Expression",lineNumber)
			


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

def evaluateBoolExpr(operator,operand1,operand2,lineNumber):

	print("Operator: ",operator," Op1: ",operand1," Op2: ",operand2)

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
		printError("Unrecognized boolean operator",lineNumber)
	
	if answer == True: answer = "WIN"
	elif answer == False: answer = "FAIL"

	return answer


def mainBool(boolExpr,lineNumber):
	flag = True
	stack = []							    # Stack used for computation
										
	inputLength = len(boolExpr)

	for i in range(inputLength):									      # Add every element of String to the stack
		new = boolExpr.pop(0)
		stack.append(new)   
	
	#checkExpression(stack,"Boolean")
	while flag == True:

		hasError = checkStackExpr(stack,"Boolean")
		if hasError == True : 									  		# Exit if there is an error detected 
			printError("Error in Boolean Expression",lineNumber)

		if len(stack) == 1:                                               # Only final answer should be left 
			flag = False
			finalAnswer = stack.pop(0)
			return finalAnswer

		for i in range(len(stack)-1):                                     # Len of Stack Refreshes after every iteration
			char = stack[i] 
			print(stack)
			if char == "NOT" :                                             # Not of is separated because it only has 1 operand 
				valid = True
				try:
					ops = stack[i]
					op1 = stack[i+1]
					op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  

					# Evaluate op1 if variable 
					print("Ops: ",ops," Op1: ",op1)

					if isBoolOperand(op1) and op1 == "WIN":	
						answer = "FAIL"
					elif isBoolOperand(op1) and op1 == "FAIL": 
						answer = "WIN"
					else : 
						valid = False
						
					stack.pop(i)                                            # Pop the not of
					stack[i] = answer
				except: 
					pass

				if valid == False: 
					printError("Invalid Not Operand",lineNumber)

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
							operation = "BOTHOF"									# ALL OF is a reeated form of BOTH OF 
							op1 = str(stack[i+1])
							op2 = str(stack[i+3])

							op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
							op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 

							if (operation in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
								answer = evaluateBoolExpr(operation,op1,op2,lineNumber)
								print("Answer: ",answer)
								for j in range(2): stack.pop(i+1)
								stack[i+1] = answer
								
								continue									
							else: 
								print("Failed to Evaluate Boolean: ",operation,op1,op2)
								pass
						
						stack.pop(i+2)				# pop MKAY
						stack.pop(i)				# pop ALL OF 
						break						# break out of outer loop to refresh count
						
					elif end == False: valid = False
				except:
					pass

				if valid == False: 
					printError("Error in All OF, matching MKAY not found.",lineNumber)

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

							op1 = evaluateIfVar(op1)									 # Checks if the Operands are Possible Variables  
							op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 
							
							if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
								answer = evaluateBoolExpr(ops,op1,op2,lineNumber)
								for j in range(2): stack.pop(i+1)
								stack[i+1] = answer
								continue									
							else: 
								pass
						
						stack.pop(i+2)				# pop MKAY
						stack.pop(i)				# pop ANY OF 
						print(stack)
						break						# break out of outer loop to refresh count
					
					elif end == False: valid = False
				except:
					pass

				if valid == False: 
					printError("Error in ANY OF, matching MKAY not found.",lineNumber)

			elif char == "AN":
				valid = True
				anIndex = i

				if stack.index(stack[i]) == 0 or stack.index(stack[i]) == 1: 
					valid = False
		
				try:
					print("AN Index: ",anIndex)
					ops = stack[anIndex-2]                  	                 # Operation, 2 steps behind AN
					op1 = str(stack[anIndex-1])                                  # Operand 1, 1 step behind AN
					op2 = str(stack[anIndex+1])                                  # Operand 2, 1 step ahead AN 

					op1 = str(evaluateIfVar(op1))									 # Checks if the Operands are Possible Variables  
					op2 = str(evaluateIfVar(op2))									 # then evaluates them to their value in string 
			
					if (ops in boolOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
					
						answer = evaluateBoolExpr(ops,op1,op2,lineNumber)
						print("Answer: ",answer)
						for j in range(3): stack.pop(anIndex-2)                  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer                                # Replace OP2 with the answer
						break									        		 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass

				if valid == False: 
					printError("Boolean Operation Syntax Error",lineNumber)


## End of Functions for Boolean Expressions =======================================================================================================================

def smooshExpression(stack,lineNumber):															# return the concatenated string
	smooshedWords = ""
	if stack[-1] == "AN": printError("Incomplete number of items to SMOOSH",lineNumber)			# Hanging AN keyword

	for i in range(len(stack)):
		if i%2 == 1:
			if stack[i] != "AN": printError("Mismatched items in SMOOSH",lineNumber)			# AN delimeter
		else:
			if isLiteral(stack[i]): smooshedWords += str(stack[i])								# Literal
			elif isVariable(stack[i]):															# Variable
				temp = evalVar(stack[i])
				if temp != False: smooshedWords += str(temp)
				else: printError(str(stack[i])+ " is not defined",lineNumber)
			else: printError(str(stack[i])+ ": invalid element in SMOOSH",lineNumber)
	return smooshedWords