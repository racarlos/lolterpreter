from helperFuncs import *
import re               # For Regex Matching 
import os
import sys

# Patterns to match with a line

hai = r"^HAI$"						# Done 
kthxbye = r"^KTHXBYE$"
ihasa = r"(\s*)(I HAS A) ([a-zA-Z][a-zA-Z0-9_]+)"
ihasitz = r"(\s*)(I HAS A) ([a-zA-Z][a-zA-Z0-9_]+) (ITZ) (.+)"
gimmeh = r"(\s*)(GIMMEH) ([a-zA-Z][a-zA-Z0-9_]+)"
r = r"(\s*)(?P<var>[a-zA-Z][a-zA-Z0-9_]+) (?P<kw>R) (?P<val>.+)"
visible = r"(\s*)(?P<kw>VISIBLE) (?P<expr>.+)"

sumof = r"(\s*)(?P<kw>SUM OF) (?P<op1>.+) (AN) (?P<op2>.+)"					# Arithmetic Expressions 
diffof = r"^(\s*)(?P<kw>DIFF OF) (?P<op1>.+) (AN) (?P<op2>.+)"
produktof = r"^(\s*)(?P<kw>PRODUKT OF) (?P<op1>.+) (AN) (?P<op2>.+)"
quoshuntof = r"^(\s*)(?P<kw>QUOSHUNT OF) (?P<op1>.+) (AN) (?P<op2>.+)"
modof = r"^(\s*)(?P<kw>MOD OF) (?P<op1>.+) (AN) (?P<op2>.+)"

# Comparison Expressions
biggrof = r"^(\s*)(?P<kw>BIGGR OF) (?P<op1>.+) (AN) (?P<op2>.+)"		# > Operator, returns the bigger number
smallrof = r"^(\s*)(?P<kw>SMALLR OF) (?P<op1>.+) (AN) (?P<op2>.+)"		# < Operator, returns the smaller number 
bothsaem = r"^(\s*)(?P<kw>BOTH SAEM) (?P<op1>.+) (AN) (?P<op2>.+)"		# == Operator
diffrint = r"^(\s*)(?P<kw>DIFFRINT) (?P<op1>.+) (AN) (?P<op2>.+)"		# != Operator 

# Logical Expressions 
notop = r"^NOT .+"				# NOT 
bothof = r"^BOTH OF .+" 		# AND
eitherof = r"^EITHER OF .+" 	# OR
wonof = r"^WON OF .+"			# XOR
anyof = r"^ANY OF .+"			# Will take infinite arguments and apply AND
allof = r"^ALL OF .+"			# Will take infinite arguments and apply OR

wtf = r"^WTF\?$"
omg = r"^OMG .+"
omgwtf = r"^OMGWTF$"

varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]+$"	# Patterns for Literals 
strIdentifier = r"^\".+\"$"
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"



def handleComments(sourceLines):					                        # Skips the comments and returns the edited file
	newSourceLines= []
	notEndComment= True

	for i in range(len(sourceLines)):				                        # Fix intentional comment mistake later
		if re.match(r'.*BTW ',sourceLines[i]):
			sourceLines[i]= re.sub(r'\s*BTW .*$', "",sourceLines[i])		# Fix match for BTW after a statement
		elif re.match(r'\s*OBTW',sourceLines[i]):							# (OBTW(\s.*\s)*TLDR$)-----only works if comment is valid for multi line; has an end clause
			notEndComment= False
		elif re.match(r'\s*TLDR',sourceLines[i]) and not notEndComment:
			notEndComment= True
			continue
		elif not notEndComment:
			continue
		if sourceLines[i]=='':
			continue
		newSourceLines.append(sourceLines[i])

	return newSourceLines


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
					op2 = evaluateIfVar(op2)									 # then evaluates them to their value in string 

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
        	

def tokenizer(sourceLines,tokens):
	lineNumber = 0

	for line in sourceLines:	# tokenize every line in the sourceLines 

		lineNumber += 1				# Increment Line Number
		thisLine = line.split()		# List form of the line 
		lineTokens = []
		
		if re.match(hai,line):											# Start
			lineTokens.append(('Program Delimiter',line))

		elif re.match(kthxbye,line):								    # End
			lineTokens.append(('Program Delimiter',line))

		elif re.match(ihasa,line):										# Variable Declaration 

			lineTokens.append(('Declaration Keyword','I HAS A'))
			
			if (len(thisLine) == 4) and isVariable(thisLine[3]):					# Variable Declaration with no initialization
				lineTokens.append(('Variable Identifier',thisLine[3]))
				varName = thisLine[3]
		
				varDict[varName] = [None,None]										# Add to variable dictionary with unknown type and unknown value 
			
			elif re.match(ihasitz,line):											# Variable Declaration with initialization
				
				m = re.match(ihasitz,line).groups()
				lineTokens.append(('Variable Identifier',m[2]))
				lineTokens.append(("Assigment KeyWord",m[3]))

				if getVarType(m[4]) != False:										# m[2] is the variable , m[3] = ITZ, m[4] is the value 
					varType = getVarType(m[4])
					lineTokens.append((varType,m[4]))	
					varDict[m[2]] = [varType,m[4]]

				elif isVariable(m[4]) == True: 
					print("This a Variable")
					## Evaluate Variable Value 
					lineTokens.append(("Assign to Variable",m[4]))	
				elif m[4] != "":
					lineTokens.append(("Possible Expression",m[4]))	
				else:
					print("Error at Ihasa: ",sourceLines.index(line))
					
			else: 
				print("Line:",lineNumber,"Error in Lexer - Variable Declaration")
				exit(1)

		elif re.match(gimmeh,line):												# If it is an input Statement 
			m = re.match(gimmeh,line).groups()
			lineTokens.append(('Input KeyWord',m[1]))							# Gimmeh tokenized as keyword
			
			if isVariable(m[2]):
				lineTokens.append(('Variable Identfier',m[2]))					# IF variable passes, tokenized as variable identifier 
			else:
				print("Line: ",lineNumber," Error at Gimmeh")
				exit(1)
		
		elif re.match(r,line):													# If assignment Statement

			m = re.match(r,line)
			var = m.group('var')
			kw = m.group('kw')
			val = m.group('val')

			if isVariable(var): lineTokens.append(('Variable Identifier',var))

			if kw == "R": lineTokens.append(('Assignment Keyword', kw))

			if isLiteral(val) != False:
				literalType = isLiteral(val)
				lineTokens.append((literalType,val))
			else:
				print("Error at R: ",sourceLines.index(line))
				exit(1)
		
		elif re.match(visible,line) :											# If it is a print statement 
			
			m = re.match(visible, line)
			kw = m.group('kw')
			expr = m.group('expr')

			lineTokens.append(('Print Keyword',kw))

			if isVariable(expr): 
				lineTokens.append(('Variable Identfier',expr))
			elif isString(expr): 
				lineTokens.append(('String Literal',expr))
			elif expr != "" :
				lineTokens.append(('Possible Expression',expr))
			else :
				print("Error at Visible: ",sourceLines.index(line))
				exit(1)
		
		elif re.match(sumof,line) or re.match(diffof,line) or re.match(produktof,line) or re.match(quoshuntof,line) or re.match(modof,line) or re.match(biggrof,line) or re.match(smallrof,line):	# Arithmetic Statement 
		
			arithExpr = manageArithKeywords(line)			# Converts SUM OF to SUMOF , and returns a list of individual lexemes
			
			for lexeme in arithExpr:

				if lexeme in arithOpsList:								# If the lexeme is an arith operator (SUMOF,DIFFOF)	
					lineTokens.append(('Arithmetic Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isArithOperand(lexeme) != False:
					lineTokens.append(('Arithmetic Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				else :
					print("Arithmetic Lexical Error: ",sourceLines.index(line))
					exit(1)

			## Probably Part of Syntax analysis 
			finalAnswer = mainArith(arithExpr)
			print("Final Answer to Arithmetic Expression: ",finalAnswer)

		elif re.match(bothsaem,line) or re.match(diffrint,line) or re.match(biggrof,line) or re.match(smallrof,line) :
			
			for lexeme in thisLine:

				if lexeme in compOpsList:
					lineTokens.append(('Comparison Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isCompOperand(lexeme) != False:
					lineTokens.append(('Comparison Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				else :
					print("Arithmetic Lexical Error: ",sourceLines.index(line))
					exit(1)

		else :
			print("Gago ano yan!: ",print(line))


		## End
		tokens.append(lineTokens)


