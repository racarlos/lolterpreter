import re

stack = []
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
str0 = "SUM OF 1 AN 2"
str2 = "SUM OF SUM OF 5 AN 6 AN 7"                     # left leaning                                                                   # left leaning      - Solved
str1 = "SUM OF 10.5 AN SUM OF 20.5 AN 30.6"            # Right leaning   
                                                
str5 = "SUM OF SUM OF 1 AN 2 AN SUM OF 3 AN 4"                                           # Both left and right - Partially Solved , 
str6 = "SUM OF SUM OF SUM OF 1 AN 2 AN SUM OF 3 AN 4 AN SUM OF SUM OF 5 AN 6 AN SUM OF 7 AN 8"

sample = str6.replace("SUM OF","SUMOF")        # replace SUM OF with SUMOF to allow string split and store each word as an element 
sample = sample.replace("DIFF OF","DIFFOF")
sample = sample.split()                          # convert string to list 
print(sample)


# Make function to convert ops to 1 word operations  EX : SUM OF - > SUMOF


def isArithOperand(number):                                     # Check if the operand is a float or integer 
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
                ops = stack[anIndex-2]                                  # Operation, 2 steps behind AN
                op1 = stack[anIndex-1]                                  # Operand 1, 1 step behind AN
                op2 = stack[anIndex+1]                                  # Operand 2, 1 step ahead AN 
            
                print("Ops: ",ops," Op1: ",op1," Op2: ",op2)
                
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







#     for i in range(len(stack)-1):
#         char = stack[i]
#         if char == "AN":
#             anIndex = i
#             try:
#                 ops = stack[anIndex-2]                          # Operation, 2 steps behind AN
#                 op1 = stack[anIndex-1]                          # Operand 1, 1 step behind AN
#                 op2 = stack[anIndex+1]                          # Operand 2, 1 step ahead AN 

#                 if ops == "SUMOF" and op1.isnumeric() and op2.isnumeric():                                                             # if ops == "SUMOF" and isnumeric(int(op1)) and isnumeric(int(op2)):
#                     # convert op1 and op2 to theit literal types or evaluate if variable                                               # type casting op1 and op 2 respectiv etypes
#                     print("Addition: ",op1,op2)
#                     answer = float(op1) + float(op2)
#                     print("Answer: ",answer)
#                     for i in range(4):      
#                         stack.pop(-1)    
                
#                     stack.append(answer)    # append the answer
#                     print("Stack after Operation: ",stack)
                
#                 elif ops == "OTHER OPERATIONS":
#                     pass
#             except :
#                 pass

# print("-----------------------------------") 
# print(stack)

# # Complete Stack Calculation 
# flag = True
# while flag:

#     for i in range(len(stack)-1):
#         char = stack[i]
#         if char == "AN":
#             anIndex = i
#             print("AN Index: ",anIndex)
            
#             try:
#                 ops = stack[anIndex-2]                          # Operation, 2 steps behind AN
#                 op1 = stack[anIndex-1]                          # Operand 1, 1 step behind AN
#                 op2 = stack[anIndex+1]                          # Operand 2, 1 step ahead AN 
#                 print("Possible Operation: ",ops,op1,op2)
             
#                 #print(stack)
#                 if ops == "SUMOF" and isArithOperand(op1) and isArithOperand(op2):                                   # if ops == "SUMOF" and isnumeric(int(op1)) and isnumeric(int(op2)):
#                     # convert op1 and op2 to theit literal types or evaluate if variable                     # type casting op1 and op 2 respectiv etypes
#                     print("Addition: ",op1,op2)
#                     answer = float(op1) + float(op2)
#                     print("Answer: ",answer)
#                     for i in range(3): stack.pop(anIndex-2)                # Pop the Stack 4 times: Operation, OP1 , AN 
                          
#                     stack[anIndex-2] = answer                              # Substitute OP 2 with answer
#                     print("Stack after Operation: ",stack)
                
#                 elif ops == "OTHER OPERATIONS":
#                     pass
#             except :
#                 print("Not a valid ops")
     
#     if len(stack) == 1:     # Terminating Condition 
#         flag = False
    
