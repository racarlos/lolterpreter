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

if sourceLines[0] != "HAI" : 
	printError("Invalid Start of program","")
if sourceLines[-1] != "KTHXBYE" : 
	printError("Invalid End of program","")


print("Lines: ")
for line in sourceLines:
	print("- ",line)

print("\nOutput: ")
tokenizer(sourceLines,tokens)							# Tokenize each line	

print("\nTokens: ")
for token in tokens:
	print(token,"\n")


print("Variable Dictionary: ",varDict)


'''
Longest Match Rule

When the lexical analyzer read the source-code, it scans the code letter by letter; and when it encounters a whitespace,
operator symbol, or special symbols, it decides that a word is completed.
'''