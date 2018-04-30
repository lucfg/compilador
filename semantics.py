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
    #print ("entered show")
    
    indent = " "* iN;

    sS = indent + "type: " + str(self.type) + "\n"

    for iI in self.args:
      if not isinstance(iI, FuncNode):
        sS += indent + str(iI)
      else:
        sS += indent + iI.show(iN + 1)
      
      sS += "\n"

      #sS += indent + "quad length is: " + str(len(quadruples))

    return sS

# -------------------------------------------------------------
  
  def semanticAll(self):
    class_dir = []
    return self.semantic("global", class_dir)

# -------------------------------------------------------------

  def semantic(self, funcName, result):
    result = {}
    
    if funcName is None:
      funcName = "global"
      
    if funcName == "global":
      currentTable = globalTable
    else:
      currentTable = localTable

# -------------------------------------------------------------

    if self.type == "program":
      quadruples.append(["GOTO","","","main"])

      for elem in self.args:
        if elem is not None:
          if isinstance(elem, str):
            print("Processing program " + elem + ".")
          else:
            elem.semantic(funcName, result)
      quadruples.append(["END","","",""])
      #print (dict(globalTable.items() + localTable.items() + auxTable.items()), quadruples)

# -------------------------------------------------------------

    elif self.type == "main":
      quadruples.append(["main","","",""])
      function_name = self.args[1]
      # TODO: check that it has not been declared before
      localTable.add("main", "int", "return")
      localTable.add(funcName, "funcType", self.args[0])

      for element in self.args[2:]:
        if element is not None:
          element.semantic(funcName, result)

      quadruples.append(["ret","","",""])
# -------------------------------------------------------------

    elif self.type == "function":
      print ("Received info from function: args0 " + self.args[0] + " args1 " + self.args[1])
      function_name = self.args[1]
      localTable.add(funcName, self.args[0], "return")
      localTable.add(funcName, "funcType", self.args[0])
      quadruples.append(["func", function_name, self.args[0],""])

      for element in self.args[2:]:
        if element is not None:
          element.semantic(funcName, result)

      quadruples.append(["ret","","",""])

# -------------------------------------------------------------

    elif self.type == "lparameters":
      print (self.args[0])
      for i in self.args[0]:
        print (i[0], i[1])
        currentTable.add(function_name, i[0], i[1])

# -------------------------------------------------------------

    elif self.type == "variables":
      if self.args[0] is not None:
        result = self.args[0].semantic(funcName, result)

# -------------------------------------------------------------
        
    elif self.type == "statement":
      if self.args[0] is not None:
        result = self.args[0].semantics(funcName, result)

# -------------------------------------------------------------
        
    elif self.type == "print":
      resultType, address = self.args[0].expression(funcName, result)
      quadruples.append(["print", address, "", ""])

# -------------------------------------------------------------

    elif self.type == "read":
      resultType, address = self.args[0].expression(funcName, result)
      quadruples.append(["read", "", "", address])

# -------------------------------------------------------------

  # TODO: Por especificar
  #elif self.type == "assignment":

# -------------------------------------------------------------

    #conditions
    elif self.type == "if":
      print ('args', self.args[0].args[0])
      tipo, address = self.args[0].args[0].expression(funcName, result)

      if tipo != 'bool':
        raise Exception("Condition must be bool type")

      #GotoF
      gotof = ['gotof', address, " ", " "]
      quadruples.append(gotof)
      lena = len(quadruples)
      result = self.args[1].semantic(funcName, result)

      goto = ['goto', " ", " ", 0]
      quadruples.append(goto)
      gotof[3] = len(quadruples) - lena

      if self.args[2] is not None:
        lenelsea = len(quadruples)
        result = self.args[2].semantic(funcName, result)
        goto[3] = len(quadruples) - lenelsea

# -------------------------------------------------------------

#while
    elif self.type == "while":
      print ('args', self.args[0].args[0])
      tipo, address = self.args[0].args[0].expression(funcName, result)

      if tipo != 'bool':
        raise Exception("Condition must be bool type")

      #GotoF
      gotof = ['gotof', address, " ", " "]
      quadruples.append(gotof)
      lena = len(quadruples)
      result = self.args[1].semantic(funcName, result)

      goto = ['goto', " ", " ", 0]
      quadruples.append(goto)
      gotof[3] = len(quadruples) - lena

      if self.args[2] is not None:
        lenelsea = len(quadruples)
        result = self.args[2].semantic(funcName, result)
        goto[3] = len(quadruples) - lenelsea

# -------------------------------------------------------------

    elif self.type == "for" :
      back = len(quadruples)
      pointer = currentTable.getpInt()
      currentTable.add(funcName, 'int', self.args[0])
      quadruples.append(['=', 0 , '', currentTable[funcName]['int'][self.args[0]]])

      # Length Array
      for key in currentTable[funcName]:
        if self.args[2] in currentTable[funcName][key].keys():
          saveLength = auxTable.add("Aux", "int", "aux")
          quadruples.append(['length', currentTable[funcName][key][self.args[2]], "",saveLength])
        else:
          raise Exception("The array is not defined")

      saveBool = auxTable.add("Aux", "int", "aux")
      quadruples.append(['<',currentTable[funcName]['int'][self.args[0]] ,currentTable[funcName][key][self.args[2]], saveBool])
      gotof = ['gotof', saveBool, " ", " "]
      quadruples.append(gotof)

      lena = len(quadruples)
      result = self.args[3].semantic(funcName, result)
      quadruples.append(['+', 1, currentTable[funcName]['int'][self.args[0]], currentTable[funcName]['int'][self.args[0]]])

      goto = ['goto', back - len(quadruples), " ", ]
      quadruples.append(goto)
      
      gotof[3] = len(quadruples) - lena
      print (quadruples)

    else:
      print("Error. Type " + self.type + " not supported.")

# -------------------------------------------------------------
# -------------------------------------------------------------
# -------------------------------------------------------------
  
  def expression(self, funcName, result):
    if funcName == "main":
      currentTable = globalTable
    else:
      currentTable = localTable

    # varTypes = {'int' : 1, 'decim' : 2, 'bool' : 3, 'char' : 4, 'String' : 5}

# -------------------------------------------------------------

    if self.type == "assignment":
      varName = self.args[1].args[0]
      resultType, address = self.args[2][0].expression(funcName, result)
      
      for key in currentTable[funcName]:
      #verifies that the variable has been declared
        if self.args[1].args[0] in currentTable[funcName][key].keys():
          if resultType == key:
            quadruples.append(["=", address, "", currentTable[funcName][resultType][varName]])
            break
          else:
            raise Exception("Cannot assign a value of different type to the variable " + self.args[1].args[0] + ".")
        else:
          print (self.args[1].args[0], currentTable[funcName][key].keys())
          raise Exception("Variable '" + self.args[1].args[0] + "' has not been declared. Cannot assign value.")

# -------------------------------------------------------------
    if self.type == "assignmentIncrease":
      varName = self.args[1].args[0]
      resultType, address = self.args[2][0].expression(funcName, result)
      
      for key in currentTable[funcName]:
      #verifies that the variable has been declared
        if self.args[1].args[0] in currentTable[funcName][key].keys():
          quadruples.append(['++', '', '', currentTable[funcName][resultType][varName]])
          break
        else:
          print (self.args[1].args[0], currentTable[funcName][key].keys())
          raise Exception("Variable '" + self.args[1].args[0] + "' has not been declared. Cannot increment.")

# -------------------------------------------------------------
    if self.type == "assignmentDecrease":
      varName = self.args[1].args[0]
      resultType, address = self.args[2][0].expression(funcName, result)
      
      for key in currentTable[funcName]:
      #verifies that the variable has been declared
        if self.args[1].args[0] in currentTable[funcName][key].keys():
          quadruples.append(['--', '', '', currentTable[funcName][resultType][varName]])
          break
        else:
          print (self.args[1].args[0], currentTable[funcName][key].keys())
          raise Exception("Variable '" + self.args[1].args[0] + "' has not been declared. Cannot increment.")

# -------------------------------------------------------------

    elif self.type == "expressions":
      result = self.args[0].semantic(funcName, result)

      if self.args[1] is not None:
        result = self.args[1].semantic(funcName, result)

# -------------------------------------------------------------
          
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

# -------------------------------------------------------------

    elif self.type == "int" :
      return "int", currentTable.add(funcName, "int", self.args[0])

# -------------------------------------------------------------

    elif self.type == "decim" :
      return "decim", currentTable.add(funcName, "decim", self.args[0])

# -------------------------------------------------------------

    elif self.type == "bool" :
      return "bool", currentTable.add(funcName, "int", self.args[0])

# -------------------------------------------------------------

    elif self.type == "id":
      table = currentTable[funcName]

      for i in table:
        for j in table[i]:
          if j == self.args[0]:
            return i, table[i][j]

      raise Exception("Variable does not exist: " + self.args[0])

# -------------------------------------------------------------

    #call function. Receives id(params)
    elif self.type == "functionCall" :
      global nextReturn

      #separates a space for the function call
      quadruples.append(["ERA", self.args[0], "",""])
      contp = 1

      #TODO: does this truly iterate through all possible parameters? Isn't the Gosub appended multiple times
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
