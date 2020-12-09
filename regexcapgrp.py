import re

stack = []
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
str0 = "SUM OF 1 AN 2"
str1 = "SUM OF 10.5 AN SUM OF 20.5 AN 30.6"            # Right leaning   
str2 = "SUM OF SUM OF 5 AN 6 AN 7"                     # left leaning                                                                   # left leaning      - Solved  
str5 = "SUM OF SUM OF 1 AN 2 AN SUM OF 3 AN 4"                                           # Both left and right - Partially Solved , 
str6 = "SUM OF SUM OF SUM OF 1 AN 2 AN SUM OF 3 AN 4 AN SUM OF SUM OF 5 AN 6 AN SUM OF 7 AN 8"

sample = str6.replace("SUM OF","SUMOF")        # replace SUM OF with SUMOF to allow string split and store each word as an element 
sample = sample.replace("DIFF OF","DIFFOF")
sample = sample.split()                          # convert string to list 
print(sample)


# Make function to convert ops to 1 word operations  EX : SUM OF - > SUMOF


def isArithOperand(number):                                     # Check if the operand is a float or integer 
    print("Arith Check: ",number)
    if re.match(numIdentifier,number) or isinstance(number,int):
        return True
    elif re.match(floatIdentifier,number) or isinstance(number,float):
        return True
    else:
        return False

inputLength = len(sample)
for i in range(inputLength):        # Add every element of String to the stack
    new = sample.pop(0)
    stack.append(new)                                           

flag = True
while flag:                                                             # Only final answer should be left 

    if len(stack) == 1: flag = False                                    # Terminating Condition
        
    print(stack)
 
    for i in range(len(stack)-1):                                       # Len of Stack Refreshes after every iteration
        char = stack[i] 

        if char == "AN":
            anIndex = i
            try:
                print("AN Index: ",anIndex)
                ops = str(stack[anIndex-2])                                  # Operation, 2 steps behind AN
                op1 = str(stack[anIndex-1])                                  # Operand 1, 1 step behind AN
                op2 = str(stack[anIndex+1])                                  # Operand 2, 1 step ahead AN 

                print("Ops: ",ops," Op1: ",type(op1)," Op2: ",type(op2))
                
                # Handle Possible Variables 

                if ops == "SUMOF" and isArithOperand(op1) and isArithOperand(op2):

                    print("Addition: ",op1,op2)
                    answer = float(op1) + float(op2)
                    for j in range(3): stack.pop(anIndex-2)             # Pop the Stack 3 times: Operation, OP1 , AN 
                    stack[anIndex-2] = answer                           # Replace OP2 with the answer
                    print("Stack after Operation: ",stack)

                    break                                               # Break Current Iteration after calculation finished

                elif ops == "DIFFOF" and isArithOperand(op1) and isArithOperand(op2) :
                    print("Subtraction: ",op1,op2)
                    answer = float(op1) - float(op2)
                    for j in range(3): stack.pop(anIndex-2)             # Pop the Stack 3 times: Operation, OP1 , AN 
                    stack[anIndex-2] = answer
                    print("Stack after Operation: ",stack)

                    break  
                
                else:
                    pass
               

            except: 
                pass
        


print("Stack: ",stack)
print("Input: ",sample)

