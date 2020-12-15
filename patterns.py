

# Patterns to Match With for a lexeme
varIdentifier = r"^[a-zA-Z][a-zA-Z0-9_]*$"
strIdentifier = r"^\".+\"$"
numIdentifier = r"^[0-9]+$"
floatIdentifier = r"^-?[0-9]+.[0-9]+$"
troofIdentifier = r"^WIN$|^FAIL$"

# Patterns to match with a line
hai = r"^HAI(.*)$"						# Done 
kthxbye = r"^KTHXBYE$"
empty = r"^(\s*)$"
ihasa = r"(\s*)(I HAS A) ([a-zA-Z][a-zA-Z0-9_]*)"
ihasitz = r"(\s*)(I HAS A) ([a-zA-Z][a-zA-Z0-9_]*) (ITZ) (.+)"
gimmeh = r"(\s*)(?P<kw>GIMMEH) (?P<var>[a-zA-Z][a-zA-Z0-9_]*)"
r = r"(\s*)(?P<var>[a-zA-Z][a-zA-Z0-9_]*) (?P<kw>R) (?P<val>.+)"
visible = r"(\s*)(?P<kw>VISIBLE) (?P<expr>.+)"

sumof = r"(\s*)(?P<kw>SUM OF) (?P<op1>.+) (AN) (?P<op2>.+)"					# Arithmetic Expressions 
diffof = r"^(\s*)(?P<kw>DIFF OF) (?P<op1>.+) (AN) (?P<op2>.+)"
produktof = r"^(\s*)(?P<kw>PRODUKT OF) (?P<op1>.+) (AN) (?P<op2>.+)"
quoshuntof = r"^(\s*)(?P<kw>QUOSHUNT OF) (?P<op1>.+) (AN) (?P<op2>.+)"
modof = r"^(\s*)(?P<kw>MOD OF) (?P<op1>.+) (AN) (?P<op2>.+)"

# Comparison Expressions
biggrof = r"^(\s*)(?P<kw>BIGGR OF) (?P<op1>.+) (AN) (?P<op2>.+)"		# > Operator, returns the bigger number
smallrof = r"^(\s*)(?P<kw>SMALLR OF) (?P<op1>.+) (AN) (?P<op2>.+)"		# < Operator, returns the smaller number 
bothsaem = r"^(\s*)(?P<kw>BOTH SAEM) (?P<op1>.+) (AN) (?P<op2>.+)"		# == Operator
diffrint = r"^(\s*)(?P<kw>DIFFRINT) (?P<op1>.+) (AN) (?P<op2>.+)"		# != Operator 

# Logical Expressions 
notop = r"^(\s*)(?P<kw>NOT) (?P<op1>.+)"										# NOT 
bothof = r"^(\s*)(?P<kw>BOTH OF) (?P<op1>.+) (AN) (?P<op2>.+)"					# AND
eitherof = r"^(\s*)(?P<kw>EITHER OF) (?P<op1>.+) (AN) (?P<op2>.+)" 				# OR
wonof = r"^(\s*)(?P<kw>WON OF) (?P<op1>.+) (AN) (?P<op2>.+)"					# XOR
anyof = r"^(\s*)(?P<kw>ANY OF) .+"												# Will take infinite arguments and apply AND
allof = r"^(\s*)(?P<kw>ALL OF) .+"												# Will take infinite arguments and apply OR

wtf = r"^WTF\?$"
omg = r"^OMG .+"
omgwtf = r"^OMGWTF$"

# Lists of Compatible Operands
arithOpsList = ["SUMOF","DIFFOF","PRODUKTOF","QUOSHUNTOF","MODOF","BIGGROF","SMALLROF"]
compOpsList = ["BIGGROF","SMALLROF","BOTHSAEM","DIFFRINT"]
boolOpsList = ["NOT","BOTHOF","EITHEROF","WONOF","ANYOF","ALLOF"]