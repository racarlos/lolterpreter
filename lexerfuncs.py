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

sumof = r"^SUM OF .+"				# Osie Half
diffof = r"^DIFF OF .+"
produktof = r"^PRODUKT OF .+"
quoshuntof = r"^QUOSHUNT OF .+"
modof = r"^MOD OF .+"
biggrof = r"^BIGGR OF .+"
smallrof = r"^SMALLR OF .+"
bothof = r"^BOTH OF .+" 

eitherof = r"^EITHER OF .+" 		# Robie Half 
wonof = r"^WON OF .+"
anyof = r"^ANY OF .+"
allof = r"^ALL OF .+"
bothsaem = r"^BOTH SAEM .+"
diffrint = r"^DIFFRINT .+"
wtf = r"^WTF\?$"
omg = r"^OMG .+"
omgwtf = r"^OMGWTF$"


varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]+"
strIdentifier = r"\".+\""
numIdentifier = r"[0-9]+"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

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

	for line in sourceLines:	# tokenize every line in the sourceLines 

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

			elif re.match(ihasitz,line):											# Variable Declaration with initialization
				
				m = re.match(ihasitz,line).groups()
				lineTokens.append(('Variable Identifier',m[2]))
				lineTokens.append(("Assigment KeyWord",m[3]))
				if isLiteral(m[4]) != False:										# m[2] is the variable , m[3] = ITZ, m[4] is the value 
					literalType = isLiteral(m[4])
					lineTokens.append((literalType,m[4]))	
				elif isVariable(m[4]) == True: 
					print("This a Variable")
					lineTokens.append(("Assign to Variable",m[4]))	
				else:
					print("Error at Ihasa: ",sourceLines.index(line))
					
			else: 
				print("Error in Lexer - Variable Declaration")
				exit(1)

		elif re.match(gimmeh,line):												# If it is an input Statement 
			m = re.match(gimmeh,line).groups()
			lineTokens.append(('Input KeyWord',m[1]))							# Gimmeh tokenized as keyword
			
			if isVariable(m[2]):
				lineTokens.append(('Variable Identfier',m[2]))					# IF variable passes, tokenized as variable identifier 
			else:
				print("Error at Gimmeh: ",sourceLines.index(line))

		elif re.match(r,line):									# If assignment Statement

			m = re.match(r,line)
			var = m.group('var')
			kw = m.group('kw')
			val = m.group('val')

			if isVariable(var): lineTokens.append(('Variable Identifier',var))

			if kw == "R": lineTokens.append(('Assignment Keyword', kw))

			if isLiteral(var) != False:
				literalType = isLiteral(var)
				lineTokens.append((literalType,var))
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
		
		elif re.match(visible,line) :	


		## End
		tokens.append(lineTokens)



		

			








# def tokenizer(sourceLines,tokens):						# Handles tokens per line
# 	i = 0
# 	currentToken = ''
# 	endString = False
# 	varDeclaration = False

# 	while i<len(line):													# Iterates per character through the whole line 
# 		currentToken += line[i]											# Per character building of the token

# 		if re.match(hai,line):											# Start
# 			tokens.append(('Program Delimiter',line))
# 			break
# 		elif re.match(kthxbye,line):								    # End
# 			tokens.append(('Program Delimiter',line))
# 			break
# 		elif re.match(ihasa,line) and varDeclaration == False:			# Variable Declaration 
# 			tokens.append(('Variable Declaration','I HAS A'))
# 			varName = ''
# 			varDeclaration = True
			
# 			thisLine = line.split()
# 			print(thisLine)
		
# 			if (len(thisLine) == 4 or len(thisLine) == 6) and re.match(varIdentifier,thisLine[3]):	# Variable Declaration with no initialization
# 				varName = thisLine[3]
# 				tokens.append(('Variable Identifier',varName))
# 			if len(thisLine) == 6 and re.match(r"ITZ",thisLine[4]):		# Variable Declaration with no initialization
# 				tokens.append(('Variable Assignment',thisLine[4]))
				
# 				# Change to call to function to verify literal type -------------------------------------------------------------
# 				tokens.append(('Literal Value',thisLine[5]))		
# 				# ===============================================================================================================
# 			else: print("Error in Lexer - Variable Declaration")
# 			break	

# 		elif re.match(gimmeh,line):									# If it is an input Statement 
# 			thisLine = line.split()
# 			tokens.append(('KeyWord',thisLine[0]))					# Gimmeh tokenized as keyword
# 			if isVariable(thisLine[1]):
# 				tokens.append(('Variable Identfier',thisLine[1]))	# IF variable passes, tokenized as variable identifier 
# 			break

# 		elif re.match(visible,line) :								# If it is a print statement 

# 		#variable
# 		#numbr
# 		#numbar
# 		#bool

# 		i+=1		