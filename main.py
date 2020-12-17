from lexerfuncs import * 

# Variables 
tokens = []											# List of Tokens, will be appended through line tokenizer 
sourceLines = []									# List of Lines
visibleLines = []									# Strings to be printed per line in Visible 

if len(sys.argv) < 2:								# No file called, Print Error and Exit 
	print("Error - No File Called ")
	exit(1)

with open(sys.argv[1]) as f:						# Read the file 
	sourceLines = f.read()							# sourceLines is list of individual lines 

sourceLines = re.split("\n",sourceLines)			# split into list per newline
sourceLines = handleComments(sourceLines)			# Remove Comments here 

for i in range(len(sourceLines)):				# Checks if the first non comment line is HAI 
	if re.match(empty,sourceLines[i]):	pass
	elif re.match(hai,sourceLines[i]):	break
	else: printError("Invalid Start of program",sourceLines.index(sourceLines[i]))

while not(re.match(kthxbye,sourceLines[-1])):
	if re.match(empty,sourceLines[-1]): sourceLines.pop()			# removes whitespaces after the KTHXBYE
	else: printError("Invalid End of program",len(sourceLines))		# Last Line must be KTHXBYE

if not(re.match(kthxbye,sourceLines[-1])) : 
	printError("Invalid End of program",len(sourceLines))		# Last Line must be KTHXBYE 


print("Lines: ")
for i in range(len(sourceLines)):
	print(i,"-",sourceLines[i])


tokenizer(sourceLines,tokens,visibleLines)							# Tokenize each line	

print("\nOutput: ")													# Print contents of Visible line which are the
for element in visibleLines:										# Outputs of Visible Statements 
	print(element)

# print("\nTokens: ")
# for token in tokens:
# 	print(token,"\n")


#print("Variable Dictionary: ",varDict)
