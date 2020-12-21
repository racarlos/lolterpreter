from patterns import * 

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
	elif re.match(smoosh,expr):
		print("Matched With Concatenation Expression", expr)
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
			print("Syntax Error,",listFlag,", Incorrect AN Placement")
			return True
		elif not (stack[0] in operationsList):
			print(stack)
			print("Syntax Error,",listFlag,", First Element not an Operator")
			return True
		elif stack[-1] in operationsList:
			print("Syntax Error,",listFlag,", Last Element is an Operator")
			return True
	except:
		pass


def smooshExpression(stack,lineNumber):															# return the concatenated string
	smooshedWords = ""
	if stack[-1] == "AN": printError("Incomplete number of items to SMOOSH",lineNumber)			# Hanging AN keyword

	for i in range(len(stack)):
		if i%2 == 1:
			if stack[i] != "AN": printError("Mismatched items in SMOOSH",lineNumber)			# AN delimeter
		else:
			if isLiteral(stack[i]):
				if isLiteral(stack[i]) == "String Literal":
					smooshedWords += str(stack[i][1:-1])
				else:
					smooshedWords += str(stack[i])								# Literal
			elif isVariable(stack[i]):															# Variable
				temp = evalVar(stack[i])
				if temp != False: 
					if isLiteral(temp) == "String Literal":
						smooshedWords += str(temp[1:-1])
					else:
						smooshedWords += str(temp[i])
				else: printError(str(stack[i])+ " is not defined",lineNumber)
			else: printError(str(stack[i])+ ": invalid element in SMOOSH",lineNumber)
	return smooshedWords

def handleComments(sourceLines):					                        # Replaces the comments with an empty string and returns the edited file
	newSourceLines= []
	notEndComment= True

	for i in range(len(sourceLines)):
		if re.match(r'[^\s]OBTW',sourceLines[i]):
			print("Error in multi-line comment: ",sourceLines[i])
			exit(1)
		elif re.match(r'\s*OBTW',sourceLines[i]):
			notEndComment= False
			sourceLines[i]=""
		elif re.match(r'.*BTW',sourceLines[i]):
			sourceLines[i]= re.sub(r'\s*BTW .*$', "",sourceLines[i])
		elif re.match(r'\s*TLDR',sourceLines[i]) and not notEndComment:
			notEndComment= True
			sourceLines[i]=""
		elif not notEndComment:
			sourceLines[i]=""
		newSourceLines.append(sourceLines[i])

	return newSourceLines
	
def smooshHelper(line):
	stringOpen = r'\".+'					# string with multiple spaces
	stringClose = r'.+\"$'
	stringLiteral = r'\".+\"'				# string has one word

	line = line.split()
	concat = ""
	modifiedLine = []
	flag = False
	for word in line:
		if re.match(stringLiteral,word): modifiedLine.append(word)
		elif re.match(stringOpen,word):
			concat += (word+" ")
			flag = True
		elif re.match(stringClose,word):
			concat += word
			flag = False
			modifiedLine.append(concat)
			concat = ""
		elif flag: concat += (word+" ")
		else: modifiedLine.append(word)
	return modifiedLine