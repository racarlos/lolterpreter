import re

varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]+$"	# Patterns for Literals 
strIdentifier = r"^\".+\"$"
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

arithOpsList = ["SUMOF","DIFFOF","PRODUKTOF","QUOSHUNTOF","MODOF","BIGGROF","SMALLROF"]
compOpsList = ["BOTHSAEM","DIFFRINT"]
relOpsList = [None]
logicOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]

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

def isArithOperand(value):	# Just like isLiteral but specific for arithmetic operands 
	if isVariable(value): return "Variable Identifier"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	else : return False




def evaluateIfVar(operand):		# Evaluates a possible variable to its value in string format 

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

def evalArithOperand(operand):
	if isNumber(operand): return int(operand)
	elif isFloat(operand): return float(operand)
	elif isVariable(operand): return evalVar(operand)					#key is string

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
        answer = max(operand1,operand2)
    elif operator == "SMALLROF":
        answer = min(operand1,operand2)     			# Return the smaller Value
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
