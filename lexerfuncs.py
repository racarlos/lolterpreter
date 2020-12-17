from arith import *
from booleans import *
from comp import *
from ifelse import *

import os
import sys


def evaluateExpression(expr,lineNumber,lineTokens):

	finalAnswer = None						# Final answer is value of the expression to be returned
	# Arithmetic Expressions
	if re.match(sumof,expr) or re.match(diffof,expr) or re.match(produktof,expr) or re.match(quoshuntof,expr) or re.match(modof,expr) or re.match(biggrof,expr) or re.match(smallrof,expr):

		arithExpr = manageArithKeywords(expr)			
		
		for lexeme in arithExpr:

			if lexeme in arithOpsList:								# If the lexeme is an arith operator (SUMOF,DIFFOF)	
				lineTokens.append(('Arithmetic Operator',lexeme))
			elif lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			elif isArithOperand(lexeme) != False:
				lineTokens.append(('Arithmetic Operand',lexeme))
			elif isVariable(lexeme) and lexeme in varDict:
				lineTokens.append(('Variable Identfier',lexeme))
			else :
				printError("Arithmetic Operation Lexical Error: ",lineNumber)

		value = str(mainArith(arithExpr,lineNumber))
		varType = getVarType(value)
		finalAnswer = [varType,value]
	
	# Comparison Expressions
	elif re.match(bothsaem,expr) or re.match(diffrint,expr):

		compExpr = manageCompKeywords(expr)
			
		for lexeme in compExpr:

			if lexeme in compOpsList:
				lineTokens.append(('Comparison Operator',lexeme))
			elif lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			elif isCompOperand(lexeme) != False:
				lineTokens.append(('Comparison Operand',lexeme))
			elif isVariable(lexeme) and lexeme in varDict:
				lineTokens.append(('Variable Identfier',lexeme))
			else :
				print(lexeme)
				printError("Comparison Operation Lexical Error ",lineNumber)

		value = str(mainComp(compExpr,lineNumber))
		varType = getVarType(value)
		finalAnswer = [varType,value]

	# Boolean Expressions
	elif re.match(notop,expr) or re.match(eitherof,expr) or re.match(wonof,expr) or re.match(bothof,expr) or re.match(allof,expr) or re.match(anyof,expr):	

		boolExpr = manageBoolKeywords(expr)

		for lexeme in boolExpr:

			if lexeme in boolOpsList:
				lineTokens.append(('Boolean Operator',lexeme))
			elif lexeme == "AN":
				lineTokens.append(('Operand Separator',lexeme))
			elif isBoolOperand(lexeme) != False:
				lineTokens.append(('Boolean Operand',lexeme))
			elif isVariable(lexeme) and lexeme in varDict:
				lineTokens.append(('Variable Identfier',lexeme))
			elif lexeme == "MKAY":
				lineTokens.append(('End Keyword',lexeme))
			else :
				print(lexeme)
				printError("Boolean Operation Lexical Error: ",lineNumber)
		
		value = str(mainBool(boolExpr,lineNumber))
		varType = getVarType(value)
		finalAnswer = [varType,value]

	# String Concatenation 
	elif re.match(smoosh,expr):
		m = re.match(smoosh,expr)
		kw = m.group('kw')
		ops = m.group('ops')

		ops = smooshHelper(ops)

		smooshLine = []
		smooshLine.append(('Print Keyword','VISIBLE'))
		smooshLine.append(('Concatenate KeyWord',kw))
		for lexeme in ops:
			if lexeme == "AN":
				smooshLine.append(('Operand Separator',lexeme))
			else:
				smooshLine.append(('Concatenation Operator',lexeme))
		lineTokens.append(smooshLine)
		finalAnswer = smooshExpression(ops,lineNumber)
		varType = getVarType(finalAnswer)
		varDict['IT'] = [varType,finalAnswer]

	# If it doesn't match with any expression print an error 
	else:
		print("Invalid Expression: ",expr)
		printError("Invalid Expression",lineNumber)

	if finalAnswer != None:
		#print("Answer to Eval Expression: ",finalAnswer)
		return finalAnswer
	else:
		printError("Expression has no return value",lineNumber)

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

def tokenizer(sourceLines,tokens,visibleLines):
	lineNumber = 0
	disabled = False

	for line in sourceLines:	# tokenize every line in the sourceLines 

		lineNumber += 1				# Increment Line Number
		thisLine = line.split()		# List form of the line 
		lineTokens = []
		printLine = []				# List to append with stuff to print
		
		if re.match(hai,line):											# Start
			lineTokens.append(('Program Start',line))

		elif re.match(kthxbye,line):								    # End
			lineTokens.append(('Program End',line))

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

				elif isVariable(m[4]) == True and (m[4] in varDict): 				# Used in I HAS A X ITZ Y 
					value = varDict[m[4]][1]
					varType = varDict[m[4]][0]
					varDict[m[2]] = [varType,value]
					lineTokens.append(("Assign to Variable",m[4]))	

				elif isExpression(m[4]):
					exprValue = evaluateExpression(m[4],sourceLines.index(line)+1,lineTokens)	# exprValue[0] = type | exprValue[0] = value 
					varDict[m[2]] = exprValue
				else:
					printError("Variable Declaration Error",sourceLines.index(line)+1)
					
			else: 
				printError("Error in Lexer - Variable Declaration",sourceLines.index(line)+1)
	
		elif re.match(gimmeh,line) and disabled == False:												# If it is an input Statement 
			m = re.match(gimmeh,line)
			kw = m.group('kw')
			var = m.group('var')
			lineTokens.append(('Input KeyWord',kw))								# Gimmeh tokenized as keyword
			if isVariable(var) and (var in varDict):
				lineTokens.append(('Variable Identfier',var))					# IF variable passes, tokenized as variable identifier 
				varVal = input()
				varVal = str(varVal)
				varType = getVarType(varVal)
				varDict[var] = [varType,varVal]
		
			else:
				printError("Error at Gimmeh, Variable Not Found",sourceLines.index(line)+1)
		
		elif re.match(r,line) and disabled == False:													# If assignment Statement

			m = re.match(r,line)
			var = m.group('var')
			kw = m.group('kw')
			val = m.group('val')

			if isVariable(var): lineTokens.append(('Variable Identifier',var))

			if kw == "R": lineTokens.append(('Assignment Keyword', kw))

			if isLiteral(val) != False:
				literalType = isLiteral(val)
				lineTokens.append((literalType,val))
				val = str(val)
				varType = getVarType(val)
				varDict[var] = [varType,val]
			elif isVariable(val) and val in varDict:
				varDict[var][0] = varDict[val][0]
				varDict[var][0] = varDict[val][0] 
			elif isExpression(val) :
				exprValue = evaluateExpression(val,sourceLines.index(line)+1,lineTokens)
				varDict[var] = exprValue
			else:
				printError("Error at R: ",sourceLines.index(line)+1)
				
		elif re.match(visible,line) and disabled == False :											# If it is a print statement 
			
			m = re.match(visible, line)
			kw = m.group('kw')
			lineTokens.append(('Print Keyword',kw))	
			expr = m.group('expr')
			
			if re.match(smoosh,expr):											#currently special case
				lineTokens.pop()
				value = evaluateExpression(expr,sourceLines.index(line)+1,lineTokens)
				tokens.append(lineTokens)
				print("-",value,len(value))
				printLine.append(value)
				if len(printLine) > 0:visibleLines.append(printLine)
				continue
			
			strList = re.findall(r"\"[^\"]*\"",expr)
			expr = expr.split('"')				# Split by double quotes delimiter, original list, changes will be stored here 
			copy = []							# Copy list used for evaluation
		
			for entry in expr: 					# Copy the trimmed strings to copy list 
				new = re.sub(r"^\s+|\s+$", "", entry)
				copy.append(new)

			for string in strList:
				lineTokens.append(("String Literal",string))

			for entry in copy:													# Substitute Variables in the Statement 

				if entry in varDict and isVariable(entry):						# If it is a variable 
					expr[copy.index(entry)] = varDict[entry][1] 				# Get the value in vardict and replace it in the original list 
					lineTokens.append(('Variable Identfier',entry))

				elif isLiteral(entry) !=  False:								# If printing a Literal
					dataType = isLiteral(entry)
					lineTokens.append((dataType,entry))
				
				elif isExpression(entry):										# If printing an expression 
					
					value = evaluateExpression(entry,sourceLines.index(line)+1,lineTokens)
					varDict['IT'] = value
					strVal = str(value[1])
					expr[copy.index(entry)] = strVal

			finalStr = ""
			for element in expr:
				finalStr = finalStr + element
			
			printLine.append(finalStr)

		elif (re.match(sumof,line) or re.match(diffof,line) or re.match(produktof,line) or re.match(quoshuntof,line) or re.match(modof,line) or re.match(biggrof,line) or re.match(smallrof,line)) and disabled == False :	# Arithmetic Statement 
		
			arithExpr = manageArithKeywords(line)			
			
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
					printError("Arithmetic Operation Lexical Error: ",sourceLines.index(line)+1)
			
			# Assign Expression's return value to IT 
			finalAnswer = mainArith(arithExpr,sourceLines.index(line)+1)
			finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("Final Answer to Arithmetic Expression: ",finalAnswer)

		elif (re.match(bothsaem,line) or re.match(diffrint,line))  and disabled == False:		# Comparison Expressions 

			compExpr = manageCompKeywords(line)
			
			for lexeme in compExpr:

				if lexeme in compOpsList:
					lineTokens.append(('Comparison Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isCompOperand(lexeme) != False:
					lineTokens.append(('Comparison Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				else :
					print(lexeme)
					printError("Comparison Operation Lexical Error ",sourceLines.index(line)+1)
						
			# Assign Expression's return value to IT 
			finalAnswer = mainComp(compExpr,sourceLines.index(line)+1)
			finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("Final Answer to Comparison Expression: ",finalAnswer)

		elif (re.match(notop,line) or re.match(eitherof,line) or re.match(bothof,line) or re.match(wonof,line) or re.match(allof,line) or re.match(anyof,line)) and disabled == False :		# Boolean operations

			boolExpr = manageBoolKeywords(line)

			for lexeme in boolExpr:

				if lexeme in boolOpsList:
					lineTokens.append(('Boolean Operator',lexeme))
				elif lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				elif isBoolOperand(lexeme) != False:
					lineTokens.append(('Boolean Operand',lexeme))
				elif isVariable(lexeme) and evalVar(lexeme):
					lineTokens.append(('Variable Identfier',lexeme))
				elif lexeme == "MKAY":
					lineTokens.append(('Boolean Delimiter',lexeme))
				else :
					printError("Boolean Operation Lexical Error: ",sourceLines.index(line)+1)

			# Assign Expression's return value to IT 
			finalAnswer = mainBool(boolExpr,sourceLines.index(line)+1)
			finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("Final Answer to Boolean Expression: ",finalAnswer)

		elif re.match(smoosh,line) and disabled == False:
			m = re.match(smoosh,line)
			kw = m.group('kw')
			ops = m.group('ops')

			ops = smooshHelper(ops)

			lineTokens.append(('Concatenate KeyWord',kw))
			for lexeme in ops:
				if lexeme == "AN":
					lineTokens.append(('Operand Separator',lexeme))
				else:
					lineTokens.append(('Concatenation Operator',lexeme))

			finalAnswer = smooshExpression(ops,lineNumber)
			finalAnswer = str(finalAnswer)
			varType = getVarType(finalAnswer)
			varDict['IT'] = [varType,finalAnswer]
			print("SMOOSH: "+ finalAnswer)
		
		elif re.match(orly,line):									 # Start of If statement 
			lineTokens.append(('Start of Condtional',lexeme))

			start = sourceLines.index(line)							 # Index of YA RLY, start of loop 

			inds = findIndex(start,sourceLines)						# Finds the Indices of YA RLY, NO WAI, and OIC
			ya = inds[0]
			no = inds[1]
			end = inds[2]

			condValue = varDict['IT'][1]

			if condValue == None: printError("IT has no value thus Condtional Statement, cannot be evaluated",lineNumber)

			if condValue == 'WIN':		
				print("YA RLY block will execute")
				disabled = False		# Will Disable at NO WAI and Reenable at OIC
			else:					
				print("NO WAI block will execute")	
				disabled = True			# Will Disable here and Reenable at NO WAI 
					
			# print("Start: ",start,sourceLines[start])
			# print("YA: ",ya,sourceLines[ya])
			# print("NO: ",no,sourceLines[no])
			# print("End: ",end,sourceLines[end])	
														
		elif re.match(nowai,line):
			lineTokens.append(('Conditional Else Block',line))
			disabled = not(disabled)

		elif re.match(oic,line):				# End of Loop, expression evaluation returns to normal
			lineTokens.append(('End of Conditional',sourceLines[end]))
			disabled = False

		elif re.match(yarly,line):
			lineTokens.append(('Conditional IF Block',line))	

		elif re.match(empty,line) or disabled == True:
			pass

		else :
			print("Unrecognized Line: ",line)
			printError("Unrecognized Pattern",lineNumber)
	


		## End
		if len(printLine) > 0: visibleLines.append(printLine)
		if len(lineTokens) > 0 : tokens.append(lineTokens)

# Switch case