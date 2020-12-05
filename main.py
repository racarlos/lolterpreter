
from lexical import *


varList = {}            # Dictionary for Variables - variable name : type,value
lines = []              # Store all lines here


inputFile = open("test.lol")    # Add every line to the lines list 
for line in inputFile: 
    line = line.strip()     
    lines.append(line)               
inputFile.close()


# For every line in the code match with a regex 
for line in lines:
    for pattern in patterns:
        if re.match(pattern,line):
            print("Pattern - ",pattern,"\t| Line - ",line)
            lexicalAnalzyer(pattern)
            break                                                # Stop searching when a match is found 