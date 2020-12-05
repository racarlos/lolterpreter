from lexerfuncs import * 

# Variables 
tokens = []											# List of Tokens, will be appended through line tokenizer 

if len(sys.argv) < 2:								# No file called, Print Error and Exit 
	print("Error - No File Called ")
	exit(1)

with open(sys.argv[1]) as f:						# Read the file 
	sourceLines = f.read()							# sourceLines is list of individual lines 

sourceLines = re.split("\n",sourceLines)			# split into list per newline
sourceLines = handleComments(sourceLines)			# Remove Comments here 

for line in sourceLines:							# Tokenize each line
	lineTokenizer(line,tokens)


for token in tokens:
	print(token,"\n")


'''
Longest Match Rule

When the lexical analyzer read the source-code, it scans the code letter by letter; and when it encounters a whitespace,
operator symbol, or special symbols, it decides that a word is completed.
'''