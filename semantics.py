import sys
from semanticCube import *
from varTable import *

globalTable = VarTable()
localTable = VarTable(15001, 20001, 25001)
auxTable = VarTable(30001, 35001, 40001)
quadruples = []

class FuncNode(object):
  def __init__(self, t, *args):
    self.type = t
    self.args = args
    
  def __str__(self):
    return self.show()
  
  def show(self, iN = 0):
    sS = " "* iN + "type: " + str(self.type) + "\n"
    for iI in self.args:
      if not isinstance(iI, funcNode):
        sS += str(iI)
      else:
        sS += iI.show(iN + 1)
      sS += "\n"
    return sS
  
  def semanticAll(self):
    class_dir = []
    return self.semantic("global", class_dir)

  def semantic(self, funcName, result):
    result = {}
    
    if funcName is None:
      funcName = "global"
    if funcName == "global":
      currentTable = globalTable
    else:
      currentTable = localTable
    
    
    if self.type == "program":
      print "Program is beginning.."
      
      for elem in self.args:
        if elem is not None:
          elem.semantic(funcName, result)
      #print (dict(globalTable.items() + localTable.items() + auxTable.items()), quadruples)
    
    # Condicion por definir
    #elif self.type == "functions":
    
    elif self.type == "variables":
      if self.args[0] is not None:
        result = self.args[0].semantic(funcName, result)
        
    elif self.type == "statement":
      if self.args[0] is not None:
        result = self.args[0].semantics(funcName, result)
        
    elif self.type == "print":
      resultType, address = self.args[0].expression(funcName, result)
      quadruples.append(["print", address, "", ""])
      
    else:
      print("Error. Type not found")
    
    
    
  
  
  
  
  
  
  
  
  
	def expression(self, funcName, result):
		if funcName == "main":
			currentTable = globalTable
		else:
			currentTable = localTable

		varTipos = {'int' : 1, 'decim' : 2, 'bool' : 3, 'char' : 4, 'String' : 5}

		if self.type == "assignment":
			varName = self.args[1].args[0]
      
      resultType, address = self.args[2][0].expression(funcName, result)
      for key in currentTable[funcName]:
        #verifies that the variable has been declared
        if self.args[1].args[0] in currentTable[funcName][key].keys():
          if resultType == key:
            quadruples.append([self.args[0], address, "", currentTable[funcName][resultType][varName]])
            break
          else:
            raise Exception("Cannot assign a value of different type to the variable " + self.args[1].args[0] + ".")
        else:
          print self.args[1].args[0], currentTable[funcName][key].keys()
          raise Exception("Variable '" + self.args[1].args[0] + "' has not been declared. Cannot assign value.")

		elif self.type == "expressions":
			result = self.args[0].semantic(funcName, result)
			if self.args[1] is not None:
				result = self.args[1].semantic(funcName, result)
		# Handles an expression
		elif self.type == "expression":
			#left operator type
			leftType, leftAddress = self.args[1].expression(funcName, result)
			#right operator type
			rightType, rightAddress = self.args[2].expression(funcName, result)
			#result type
			resultType = semanticCube[leftType][rightType][self.args[0]]
			#temp addresses
			resultAddress = auxTable.add("Aux", resultType, "aux")
			quadruples.append([self.args[0], leftAddress, rightAddress, resultAddress])
			return resultType, resultAddress

		elif self.type == "int" :
			return "int", currentTable.add(funcName, "int", self.args[0])

		elif self.type == "decim" :
			return "decim", currentTable.add(funcName, "decim", self.args[0])

		elif self.type == "bool" :
			return "bool", currentTable.add(funcName, "int", self.args[0])

		elif self.type == "id":
			table = currentTable[funcName]
			for i in table:
				for j in table[i]:
					if j == self.args[0]:
						return i, table[i][j]
			raise Exception("Variable does not exist: " + self.args[0])
		#call function. Receives id(params)
		elif self.type == "functionCall" :
			global nextReturn
			#separates a space for the function call
			quadruples.append(["ERA", self.args[0], "",""])
			contp = 1
			for i in self.args[1]:
				resultType, resultAddress = i.expression(funcName, result)
				quadruples.append(["Param", resultAddress, "", "param"+str(contp)])
        contp += 1
			quadruples.append(["Gosub", self.args[0], "", ""])
			funcType = localTable[self.args[0]]["funcType"]["return"]
			auxAddress = auxTable.add("Aux", funcType, "aux")
			nextReturn = ["=", localTable[self.args[0]][funcType]["return"], "", auxAddress]
			quadruples.append(nextReturn)
			return funcType, auxAddress

		return result
