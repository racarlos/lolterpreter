import re               # For Regex Matching 
import os
import sys

# Patterns to match with a line
hai = r"HAI"
kthxbye = r"KTHXBYE"
ihasa = r"I HAS A .+"
gimmeh = r"GIMMEH .+"
visible = r"VISIBLE .+"
varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]*"


# tokenDict= {								#add some more later
# 	PROG_START : 'HAI',
# 	PROG_END : 'KTHXBYE',
# 	PLUS : 'SUM OF',
# 	MINUS : 'DIFF OF',
# 	MULTIPLY : 'PRODUKT OF',
# 	DIVIDE : 'QUOSHUNT OF',
# 	MODULO : 'MOD OF',
# 	GREATER_THAN : 'BIGGR OF'
# 	LESS_THAN : 'SMALLR OF'
# 	PRINT : 'VISIBLE',
# 	DECLARATION : 'I HAS A'					#noob data type

# }


# List of regex patterns to match with
patterns = [hai,kthxbye,ihasa,visible]


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


def lineTokenizer(line,tokens):						# Handles tokens per line
	i = 0
	currentToken = ''
	endString = False
	varDeclaration = False

	while i<len(line):													# Iterates per character through the whole line 
		currentToken += line[i]											# Per character building of the token

		if re.match(hai,line):											# Start
			tokens.append(('Program Delimiter',line))
			break
		elif re.match(kthxbye,line):								    # End
			tokens.append(('Program Delimiter',line))
			break
		elif re.match(ihasa,line) and varDeclaration == False:				# Variable Declaration 
			tokens.append(('Variable Declaration','I HAS A'))
			varName = ''
			varDeclaration = True
			
			thisLine = line.split()
			print(thisLine)
		
			if (len(thisLine) == 4 or len(thisLine) == 6) and re.match(varIdentifier,thisLine[3]):	# Variable Declaration with no initialization
				varName = thisLine[3]
				tokens.append(('Variable Identifier',varName))
			if len(thisLine) == 6 and re.match(r"ITZ",thisLine[4]):		# Variable Declaration with no initialization
				tokens.append(('Variable Assignment',thisLine[4]))
				
				# Change to call to function to verify literal type -------------------------------------------------------------
				tokens.append(('Literal Value',thisLine[5]))		
				# ===============================================================================================================
			else: print("Error in Lexer - Variable Declaration")
			break	

		elif line[i]=='"' or endString:				#handles string
			currentToken+=line[i]
			if line[i]=='"' and endString:
				endString= False
				tokens.append(('String Delimiter','"'))
				tokens.append(('String Literal',currentToken[0:len(currentToken)-1]))			#takes out quotes not sure if i should lol
				tokens.append(('String Delimiter','"'))
				currentToken= ''
				i+=1
				continue
			endString= True

			
		#variable
		#numbr
		#numbar
		#bool

		i+=1		
