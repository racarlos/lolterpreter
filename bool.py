import re
from helperFuncs import * 

print(boolOpsList)
boolOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]


def isBoolOperand(x):
    if re.match(troofIdentifier,x):
        return True
    else:
        return False

def manageBoolKeywords(line)
	keywordListTuple = [("BOTH OF","BOTHOF"),("EITHER OF","EITHEROF"),("WON OF","WONOF"),("ANY OF","ANYOF"),("ALL OF","ALLOF")]
	for keyword in keywordListTuple:
		line = line.replace(keyword[0],keyword[1])
	line = line.split()
	return line

def evaluateBoolExpr(operator,operand1,operand2):

    print("Ops: ",operator," Op1: ",operand1," Op2: ",operand2)
	answer = None

def mainBool(boolExpr):
    flag = True
	stack = []							    # Stack used for computation
										
	inputLength = len(compExpr)

	for i in range(inputLength):			# Add every element of String to the stack
		new = compExpr.pop(0)
		stack.append(new)   

    while flag == True:
        
        if len(stack) == 1:                                                 # Only final answer should be left 
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
		
					if (ops in compOpsList) and isBoolOperand(op1) and isBoolOperand(op2):
						answer = evaluateCompExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)                  # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer                                # Replace OP2 with the answer
						break									        		 # Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass