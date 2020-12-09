
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
		return
	else: 
		return False


def isLiteral(value):	# Checks for the type of the value, returns a string of its type

	if isString(value): return "String Literal"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	elif isTroof(value): return "Troof Literal"
	else : return False

def isArithOperand(value):
	if isVariable(value): return "Variable Identifier"
	elif isNumber(value): return "Integer Literal"
	elif isFloat(value): return "Float Literal"
	else : return False