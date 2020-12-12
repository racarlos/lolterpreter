import re


compOpsList = ["BIGGROF","SMALLROF","BOTHSAEM","DIFFRINT"]
stack = []

numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

## Test Cases

str1 = "SUM OF 1 AN 2"
str2 = "SUM OF SUM OF 5 AN 6 AN 7"                          # left leaning                                                                   # left leaning      - Solved
str3 = "SUM OF 10.5 AN SUM OF 20.5 AN 30.6"                 # Right leaning   
str4 = "SUM OF SUM OF 1 AN 2 AN SUM OF 3 AN 4"              # Both left and right - Partially Solved , 
str5 = "SUM OF SUM OF SUM OF 1 AN 2 AN SUM OF 3 AN 4 AN SUM OF SUM OF 5 AN 6 AN SUM OF 7 AN 8"


def manageCompKeywords(line):
    keywordListTuple = [("BIGGR OF","BIGGROF"),("SMALLR OF","SMALLROF"),("BOTH SAEM","BOTHSAEM")]
    for keyword in keywordListTuple:
        line = line.replace(keyword[0],keyword[1])
    line = line.split()
    return line



def evaluateCompExpr(operator,operand1,operand2) 

    if operator == "BOTHSAEM":
        if operand1 == operand2: answer = "WIN"     # Win if equal, Fail if not
        else: answer = "FAIL"
    elif operator == "DIFFRINT":
        if operand1 != operand2: answer = "WIN"     # Win if not equal, Fail if not 
        else: answer = "FAIL"
    else:
        print("Unrecognized Comparison Operator")
        exit(1)


def isCompOperand(x):
    if re.match(troofIdentifier,x):
        return True
    elif re.match(numIdentifier,x):
        return True
    elif re.match(floatIdentifier,x):
        pass
    else:
        return False 

def checkCompOperands(op1,op2):         # Valid are number to number - biggr and smallr and boolean to boolean

    
def compMain():
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
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 

					print("Ops: ",ops," Op1: ",type(op1)," Op2: ",type(op2))
					
                    valid = checkCompOperands(ops,op1,op2)                       # Check if the set of operands are valid 

					# Handle Possible Variables 
					if (ops in arithOpsList) and isArithOperand(op1) and isArithOperand(op2):
						answer = evaluateCompExpr(ops,op1,op2)
						for j in range(3): stack.pop(anIndex-2)             # Pop the Stack 3 times: Operation, OP1 , AN 
						stack[anIndex-2] = answer                           # Replace OP2 with the answer
						print("Stack after Operation: ",stack)
						break												# Break Iteration after an operation has completed 
					else:
						pass
				except: 
					pass