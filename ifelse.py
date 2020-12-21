from helperFuncs import *

def ifChecker(sourceLines):									# Checks for errors in the else-if statement
    pass

def findIndex(start,sourceLines):

    ya = None
    no = None
    end = None

    for i in range(start+1,len(sourceLines)-1):					# Find Index of Loop Start
        if re.match(empty,sourceLines[i]): pass
        elif re.match(yarly,sourceLines[i]): 
            ya = i
            break 
        else : printError("Statement to Execute if True (YA RLY) not found",i)

    for i in range(ya+1,len(sourceLines)-1):					# Find the NO WAI, error if it finds OIC first 
        if re.match(empty,sourceLines[i]): pass
        elif re.match(nowai,sourceLines[i]): 
            no = i
            break 
        elif re.match(oic,sourceLines[i]) : 
            printError("Statement to Execute if False (NO WAI) not found",i)
        else: pass

    for i in range(no+1,len(sourceLines)-1):					# Find the OIC, error if it sees kthxbye 
        if re.match(empty,sourceLines[i]): pass
        elif re.match(oic,sourceLines[i]): 
            end = i
            break
        elif re.match(kthxbye,sourceLines[i]):
            printError("End of Loop (OIC) not found",i)
        else: pass

    if ya != None and no != None and oic != None:
        return [ya,no,end]
    else:   
        printError("A none type Found on the IF ELSE indices")