from lexerfuncs import * 

# Variables 
tokens = []											# List of Tokens, will be appended through line tokenizer 
sourceLines = []									# List of Lines

if len(sys.argv) < 2:								# No file called, Print Error and Exit 
	print("Error - No File Called ")
	exit(1)

with open(sys.argv[1]) as f:						# Read the file 
	sourceLines = f.read()							# sourceLines is list of individual lines 

sourceLines = re.split("\n",sourceLines)			# split into list per newline
sourceLines = handleComments(sourceLines)			# Remove Comments here 

if not(re.match(hai,sourceLines[0])): 							# First line must be HAI
	printError("Invalid Start of program",1)

while not(re.match(kthxbye,sourceLines[-1])):
	if re.match(empty,sourceLines[-1]): sourceLines.pop()			# removes whitespaces after the KTHXBYE
	else: printError("Invalid End of program",len(sourceLines))		# Last Line must be KTHXBYE

if not(re.match(kthxbye,sourceLines[-1])) : 
	printError("Invalid End of program",len(sourceLines))		# Last Line must be KTHXBYE 

print("Lines: ")
for line in sourceLines:
	print("- ",line)

print("\nOutput: ")
tokenizer(sourceLines,tokens)							# Tokenize each line	

# print("\nTokens: ")
# for token in tokens:
# 	print(token,"\n")


print("Variable Dictionary: ",varDict)
