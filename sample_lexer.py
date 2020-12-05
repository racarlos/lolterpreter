import sys
import re
#import os

if len(sys.argv) < 2:								#no file called
	print("place the file somewhere there...")
	quit()

with open(sys.argv[1]) as f:
	source= f.read()

def handleComments(sourceLines):					#skips the comments and returns the edited file
	newSourceLines= []
	notEndComment= True

	for i in range(len(sourceLines)):				#fix intentional comment mistake later
		if re.match(r'.*BTW ',sourceLines[i]):
			sourceLines[i]= re.sub(r'\s*BTW .*$', "",sourceLines[i])		#fix match for BTW after a statement
		elif re.match(r'\s*OBTW',sourceLines[i]):		# (OBTW(\s.*\s)*TLDR$)-----only works if comment is valid for multi line; has an end clause
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

def makeTokens(line,tokens):						#handles tokens per line
	i= 0
	currentToken= ''
	endString= False
	varDeclaration= False
	while i<len(line):
		currentToken+=line[i]
		if line=='HAI':								#start
			tokens.append(('Code Delimiter',line))
			break
		if line=='KTHXBYE':							#end
			tokens.append(('Code Delimiter',line))
			break
		if re.match(r'^\s*I HAS A',line) and not varDeclaration:
			tokens.append(('Variable Declaration','I HAS A'))
			varName= ''
			varDeclaration= True
		if 'I HAS A ' in currentToken and varDeclaration:
			varName+=line[i]
			if varName[0]==' ' and varName[len(varName)-1]==' ':
				if re.match(r'^[a-zA-Z][a-zA-Z0-9_]*$',varName[1:len(varName)-1]):
					tokens.append(('Variable Identifier',varName[1:len(varName)-1]))
					varName= ' '
				if re.match(r'^ITZ$',varName[1:len(varName)-1]):
					tokens.append(('Variable Assignment',varName[1:len(varName)-1]))
					varName= ' '
				
		if line[i]=='"' or endString:				#handles string
			currentToken+=line[i]
			if line[i]=='"' and endString:
				endString= False
				tokens.append(('String Delimiter','"'))
				tokens.append(('String Literal',currentToken[1:len(currentToken)-1]))			#takes out quotes not sure if i should lol
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
	return tokens

tokens= []
sourceLines= re.split("\n",source)
newLines= handleComments(sourceLines)	#new source lines here

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

for j in newLines:
	makeTokens(j,tokens)
print(tokens)

# for i in newLines:
# 	print(i)

'''
Longest Match Rule

When the lexical analyzer read the source-code, it scans the code letter by letter; and when it encounters a whitespace,
operator symbol, or special symbols, it decides that a word is completed.
'''