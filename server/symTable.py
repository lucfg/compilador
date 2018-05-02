import sys

# Symbol Table
symbolTable = {}

# ----------------------------------------------------------------
class DirectoryTuple:
  def __init__(self, funcName, returnType):
    self.funcName = funcName
    self.returnType = returnType
    self.localVariables = {}	#dict of varTuple
    
  # Check if the name is in the symbol table
  def findVarKey(name):
    if name in self.localVariables:
      return True
    else:
      return False
    
  # Adds a variable to the variable symbol table contained within a function
  def addVarKey(varName, varType):
    # Checks if the symbol already exists
    if findVarKey(varName):
      print("Symbol already exists in the table")
    else:
      # Adds the new variable to the dictionary
      temp = VarTuple(varName, varType)
      self.localVariables[varName] = temp
  
class VarTuple:
  def __init__(self, varName, varType):
  	self.varName = varName
  	self.varType = varType
# ----------------------------------------------------------------

# Check if the name is in the symbol table
def findKey(name):
    if name in symbolTable:
      return True
    else:
      return False

# Adds a tuple to the function symbol table
def addFuncKey(funcName, returnType):
  if findKey(funcName):
    print("Symbol already exists in the table")
  else:
    temp = DirectoryTuple(funcName, returnType)
    symbolTable[funcName] = temp

# Removes a function tuple from the symbol table
def removeFuncKey(funcName):
  if findKey(funcName):
  	del symbolTable[funcName]
  else:
  	print("Could not find function " + funcName + " in symbol table.")
