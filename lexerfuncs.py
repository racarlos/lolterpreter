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
bothsaem = r"^(\s*)(?P<kw>BOTH SAEM) (?P<op1>.+) (AN) (?P<op2>.+)"	# == Operator
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


arithOpsList = ["SUMOF","DIFFOF","PRODUKTOF","QUOSHUNTOF","MODOF"]
compOpsList = ["BOTHOF","EITHEROF","NOT","EITHEROF","WONOF",]
logicOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]

# Global Lists
varDict = {} 


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

def tokenizer(sourceLines,tokens):
	lineNumber = 0

	for line in sourceLines:	# tokenize every line in the sourceLines 
		lineNumber += 1				# Incremen Line Number
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
		
				varDict[varName] = [None,None]							# Add to variable dictionary with unknown type and unknown value 
			
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
		
		elif re.match(sumof,line):												# Arithmetic Addition Statement 
			pass
		
		elif re.match(diffof,line):
			pass

		elif re.match(produktof,line):
			pass
		elif re.match(quoshuntof,line):
			pass


		## End
		tokens.append(lineTokens)
