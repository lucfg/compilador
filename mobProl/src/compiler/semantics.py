import sys
from semanticCube import *
from varTable import *

globalTable = VarTable()
localTable = VarTable(15001, 20001, 25001)
auxTable = VarTable(30001, 35001, 40001)
quadruples = []

def isPrimitive(t):
    if isinstance(t, str):
        if t == "true" or t == "false":
            return True
    elif isinstance(t, int):
        return True
    elif isinstance(t, float):
        return True
    return False


def getType(v, funcName="missingFuncName", currentTable="error"):
    print("Getting type of " + str(v))
    if isinstance(v, str):
        if v == "true" or v == "false":
            print("Si es bool")
            return "bool"
        else:
            found = False
            for key in currentTable[funcName]:
                print ("GetType key: " + key)
            #verifies that the variable has been declared
                if v in currentTable[funcName][key].keys():
                    print("Lo encontre")
                    found = True
                    return key, False
                    break

            for key in globalTable["global"]:
                print ("GetType key global: " + key)
            #verifies that the variable has been declared
                if not found and (v in globalTable["global"][key].keys()):
                    print("Lo encontre")
                    found = True
                    return key, True
                    break
                
        if not found:
            print (v, currentTable[funcName][key].keys())
            raise Exception("Variable '" + str(v) + "' has not been declared. Cannot assign value.")

            return "string"
    elif isinstance(v, int):
        return "int", "value"
    elif isinstance(v, float):
        return "decim", "value"
    else:
        return "other"

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
    quadruples = []
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
      funcName = self.type
      # TODO: check that it has not been declared before
      currentTable.add(funcName, "int", "main")
      localTable.add(funcName, "funcType", self.args[0])

      for elem in self.args[1:]:
        if elem is not None:
          elem.semantic(funcName, result)

      quadruples.append(["ret","","",""])
# -------------------------------------------------------------

    elif self.type == "function":
      print ("Received info from function: args0 " + self.args[0] + " args1 " + self.args[1])
      funcName = self.args[0]
      currentTable.add(funcName, self.args[1],self.args[0])
      localTable.add(funcName, "funcType", self.args[0])
      quadruples.append(["func", funcName, self.args[1],""])

      for elem in self.args[2:]:
        if elem is not None:
          elem.semantic(funcName, result)

      quadruples.append(["ret","","",""])

# -------------------------------------------------------------

    elif self.type == "params":
      #print (self.args[0])
      for i in range(0, len(self.args[0]), 2):
        #print (self.args[0][i], self.args[0][i+1])
        currentTable.add(funcName, self.args[0][i], self.args[0][i+1])

# -------------------------------------------------------------

    elif self.type == "var":
      if self.args[0] is not None:
        if self.args[1] is not None:
          currentTable.add(funcName, self.args[1], self.args[0])
      if self.args[2] is not None:
        result = self.args[2].semantic(funcName, result)

# -------------------------------------------------------------
        
    elif self.type == "statement":
      print("Entro a statement")
      if self.args[0] is not None:
        print(self.args[0])
        result = self.args[0].expression(funcName, result)

# -------------------------------------------------------------
        
    elif self.type == "statements":
      print("Entro a statements")
      print(self.args[0])
      result = self.args[0].expression(funcName, result)
      if self.args[1] is not None:
          result = self.args[1].semantic(funcName, result)

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
    if funcName == "global":
      currentTable = globalTable
    else:
      currentTable = localTable

# -------------------------------------------------------------

    print("Entro a expresion")
    print(funcName)
    if self.type == "assignment":
      varName = self.args[0].args[0]
      resultType, address = self.args[2].expression(funcName, result)
      print("Result type: " + str(resultType))
      print("Address: " + str(address))
      print("Assignment part 1")
      print(varName)
      found = False
      for key in currentTable[funcName]:
        print("CurTable funcName Key: " + str(globalTable["global"].keys()))
      #verifies that the variable has been declared
        if varName in currentTable[funcName][key].keys():
          if resultType == key:
            found = True
            quadruples.append(["=", address, "", currentTable[funcName][resultType][varName]])
            print("Hice el cuadruplo" + str(["=", address, "", currentTable[funcName][resultType][varName]]))
            break
          else:
            raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0]) + ".")
      for key in globalTable["global"]:
          print("CurTable funcName Key: " + str(globalTable["global"].keys()))
      #verifies that the variable has been declared
          if not found and (varName in globalTable["global"][key].keys()):
              if resultType == key:
                  found = True
                  quadruples.append(["=", address, "", globalTable["global"][resultType][varName]])
                  print("Hice el cuadruplo" + str(["=", address, "", globalTable["global"][resultType][varName]]))
                  break
              else:
                  raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0]) + ".")
        
      if not found:
        print (self.args[0], currentTable[funcName][key].keys())
        raise Exception("Variable '" + str(varName) + "' has not been declared. Cannot assign value.")

# -------------------------------------------------------------
    elif self.type == "assignmentIncrease":
      varName = self.args[1].args[0]
      resultType, address = self.args[2][0].expression(funcName, result)
      
      for key in currentTable[funcName]:
      #verifies that the variable has been declared
        if self.args[1].args[0] in currentTable[funcName][key].keys():
          quadruples.append(['++', '', '', currentTable[funcName][resultType][varName]])
          break
        else:
          print (self.args[1].args[0], currentTable[funcName][key].keys())
          raise Exception("Variable '" + str(varName) + "' has not been declared. Cannot increment.")

# -------------------------------------------------------------
    elif self.type == "assignmentDecrease":
      varName = self.args[1].args[0]
      resultType, address = self.args[2][0].expression(funcName, result)
      
      for key in currentTable[funcName]:
      #verifies that the variable has been declared
        if self.args[1].args[0] in currentTable[funcName][key].keys():
          quadruples.append(['--', '', '', currentTable[funcName][resultType][varName]])
          break
        else:
          print (self.args[1].args[0], currentTable[funcName][key].keys())
          raise Exception("Variable '" + str(varName) + "' has not been declared. Cannot increment.")

# -------------------------------------------------------------

    #elif self.type == "expressions":
#      result = self.args[0].semantic(funcName, result)

#      if self.args[1] is not None:
#        result = self.args[1].semantic(funcName, result)

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

    elif self.type == "megaExp":
      print("Entro a megaExp")
      auxVarName = self.args[0].args[0].args[0].args[0].args[0]
      print(auxVarName)
      if isPrimitive(auxVarName):
          result, address = self.args[0].expression(funcName, result)
          return result, address
      else:
          result, address = self.args[0].expression(funcName, result)
          return result, address
# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "megaExps":
      print("Entro a megaExps")

      #left operator type
      leftType, leftAddress = self.args[0].expression(funcName, result)

      #right operator type
      rightType, rightAddress = self.args[2].expression(funcName, result)

      #result type
      resultType = semanticCube[leftType][rightType][self.args[1]]

      #temp addresses
      resultAddress = auxTable.add("Aux", resultType, "aux")
      quadruples.append([self.args[1], leftAddress, rightAddress, resultAddress])

      return resultType, resultAddress

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "superExp":
      print("Entro a superExp")
      result, address = self.args[0].expression(funcName, result)
      return result, address
    #return getType(auxVarName, funcName, currentTable), auxVarName

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "superExps":
      print("Entro a superExps")
      #left operator type
      leftType, leftAddress = self.args[0].expression(funcName, result)

      #right operator type
      rightType, rightAddress = self.args[2].expression(funcName, result)

      #result type
      print("LeftType: " + leftType)
      print("RightType: " + rightType)
      print("Args[1]: " + str(self.args[1]))
      resultType = semanticCube[leftType][rightType][self.args[1]]

      #temp addresses
      resultAddress = auxTable.add("Aux", resultType, "aux")
      quadruples.append([self.args[1], leftAddress, rightAddress, resultAddress])

      return resultType, resultAddress

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "exp":
      print("Entro a Exp")
      auxVarName = self.args[0].args[0]
      result, address = self.args[0].expression(funcName, result)
      return result, address
          #return getType(auxVarName, funcName, currentTable), auxVarName

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "exps":
      print("Entro a Exps")
      #left operator type
      leftType, leftAddress = self.args[0].expression(funcName, result)

      #right operator type
      rightType, rightAddress = self.args[2].expression(funcName, result)

      #result type
      print("LeftType: " + leftType)
      print("RightType: " + str(rightType))
      print("Args[1]: " + str(self.args[1]))
      resultType = semanticCube[leftType][rightType][self.args[1]]
      print(resultType)
      
      #temp addresses
      resultAddress = auxTable.add("Aux", resultType, "aux")
      quadruples.append([self.args[1], leftAddress, rightAddress, resultAddress])

      return resultType, resultAddress

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "term":
      print("Entro a term")
      print("Term args0: " + str(self.args[0]))
      result, address = self.args[0].expression(funcName, result)
      return result, address
#          auxVarName = self.args[0].args[0].args[0]
#          return getType(auxVarName, funcName, currentTable), auxVarName

# -------------------------------------------------------------

#-------------------------------------------------------------

    elif self.type == "terms":
      print("Entro a terms")
      #left operator type
      leftType, leftAddress = self.args[0].expression(funcName, result)

      #right operator type
      rightType, rightAddress = self.args[2].expression(funcName, result)

      #result type
      resultType = semanticCube[leftType][rightType][self.args[1]]

      #temp addresses
      resultAddress = auxTable.add("Aux", resultType, "aux")
      quadruples.append([self.args[1], leftAddress, rightAddress, resultAddress])

      return resultType, resultAddress

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "factor":
      print("Entro a factor")
      print(self.args[0])
      if isPrimitive(self.args[0]):
        typeGet, valOrAdd = getType(self.args[0], funcName, currentTable)
        print("typeGet de un valor: " + str(typeGet))
        if typeGet == "int" or typeGet == "decim":
            address = "*" + str(self.args[0]) + "*"
 #       auxAddress = auxTable.add("Aux", resultType, "aux")
        return typeGet, address
      else:
        result, address = self.args[0].expression(funcName, result)
        return result, address

# -------------------------------------------------------------
# TODO: arreglos
    elif self.type == "idCall":
        print("Entro a idCall")
        typeGet, isGlobal = getType(self.args[0], funcName, currentTable)
        print("getType de global:" + str(typeGet))
        if isGlobal:
            return typeGet, globalTable["global"][typeGet][self.args[0]]
        else:
            return typeGet, currentTable[funcName][typeGet][self.args[0]]
        if self.args[3] is not None:
            aux = self.args[3].expression(funcName, result)
            quadruples.append([self.args[2], result, aux, currentTable[funcName][resultType][varName]])

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
