import re

compOpsList = ["BIGGROF","SMALLROF","BOTHSAEM","DIFFRINT"]
stack = []

numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

#test case
str1 = "BOTH SAEM 1 AN 1"
str2 = "BOTH SAEM 1 AN 1.0"
str3 = "DIFFRINT 1 AN 1"
str4 = "DIFFRINT 1 AN 1.0"
str5 = "BOTH SAEM 4 AN BIGGR OF 4 AN 5"
str6 = "BOTH SAEM 4 AN BIGGR OF 4.0 AN 5"
str7 = "DIFFRINT 4 AN BIGGR OF 4 AN 5"
str8 = "DIFFRINT 4 AN BIGGR OF 4.0 AN 5"

def evaluateRelationalExpr(operator,operand1,operand2,compoundExprFlag,relationalFlag):			#compundExprFlag checks whether the line has the BIGGR OF or SMALLR OF keyword
	if operator == "BOTHSAEM":
		if compoundExprFlag:
			if type(operand1) == type(operand2) and operand1 >= operand2 and relationalFlag == "BIGGROF":
				return "WIN"
			elif type(operand1) == type(operand2) and operand1 <= operand2 and relationalFlag == "SMALLROF":
				return "WIN"
			else: return "FAIL"
		else:
			if type(operand1) == type(operand2) and operand1 == operand2: return "WIN"
			else: return "FAIL"
	elif operator == "DIFFRINT":
		if compoundExprFlag:
			if operand1 < operand2 and relationalFlag == "BIGGROF": return "WIN"
			elif operand1 > operand2 relationalFlag == "SMALLROF": return "WIN"
			else: return "FAIL"
		else:
			if type(operand1) == type(operand2) and operand1 == operand2: return "FAIL"
			else: return "WIN"
	else:
		print("Unknown Operator")
		exit(1)

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