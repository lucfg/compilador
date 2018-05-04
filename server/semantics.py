import sys
from semanticCube import *
from varTable import *

globalTable = VarTable()
localTable = VarTable(15001, 20001, 25001)
auxTable = VarTable(30001, 35001, 40001)
quadruples = []
gotoMain = ["GOTO","","",""]
contp = 1

def isPrimitive(t):
    if isinstance(t, str):
        if t == "true" or t == "false":
            return True
        elif t[0] == "\"":
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
            return "bool", "value"
        elif v[0] == "\"":
            return "string", "value"
        else:
            found = False
            for key in currentTable[funcName]:
            #verifies that the variable has been declared
                if v in currentTable[funcName][key].keys():
                    found = True
                    return key, False
                    break
    
            for key in globalTable["global"]:
            #verifies that the variable has been declared
                if not found and (v in globalTable["global"][key].keys()):
                    found = True
                    return key, True
                    break
                
        if not found:
            raise Exception("Variable '" + str(v) + "' has not been declared. Cannot assign value.")

    elif isinstance(v, int):
        return "int", "value"
    elif isinstance(v, float):
        return "decim", "value"
    else:
        return "void", "value"

class FuncNode(object):
  def __init__(self, t, *args):
    self.type = t
    self.args = args
    
  def __str__(self):
    return self.show()
  
  def show(self, iN = 0):
    
    indent = " "* iN;

    sS = indent + "type: " + str(self.type) + "\n"

    for iI in self.args:
      if not isinstance(iI, FuncNode):
        sS += indent + str(iI)
      else:
        sS += indent + iI.show(iN + 1)
      
      sS += "\n"
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
      quadruples.append(gotoMain)

      for elem in self.args:
        if elem is not None:
          if isinstance(elem, str):
            print("Processing program " + elem + ".")
          else:
            elem.semantic(funcName, result)
      quadruples.append(["END","","",""])

# -------------------------------------------------------------

    elif self.type == "main":
      quadruples.append(["main","","",""])
      gotoMain[3] = len(quadruples) - 1
      funcName = self.type
      currentTable.add(funcName, "int", "main")
      localTable.add(funcName, "funcType", self.args[0])

      for elem in self.args[1:]:
        if elem is not None:
          elem.semantic(funcName, result)

      quadruples.append(["ret","*0*","",""])
# -------------------------------------------------------------

    elif self.type == "function":
      funcName = self.args[0]
      currentTable.add(funcName, self.args[1],self.args[0])
      localTable.add(funcName, "funcType", self.args[0])
      auxFuncType = ["func", funcName, self.args[1],""]
      quadruples.append(auxFuncType)

 #     auxReturn = ""

      for elem in self.args[2:]:
        if elem is not None:
          elem.semantic(funcName, result)

      quadruples.append(["ENDPROC","","",""])

# -------------------------------------------------------------

    elif self.type == "return":
        resultType, address = self.args[0].expression(funcName, result)
        print("El result de RETURN" + str(resultType))

        print(str(globalTable[funcName].keys()))
        if resultType in globalTable[funcName].keys(): 
            quadruples.append(["ret", address,"",""])
        else:
            raise Exception("The function " + funcName + " needs to return something of type " + resultType + ".")

# -------------------------------------------------------------

    #TODO: PARAMS
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
        if self.args[0].type == "assignment" or self.args[0].type == "functionCall" or self.args[0].type == "print" or self.args[0].type == "read":
            result = self.args[0].expression(funcName, result)
        else:
            result = self.args[0].semantic(funcName, result)

# -------------------------------------------------------------
        
    elif self.type == "statements":
      print("Entro a statements")
      if self.args[0].type == "assignment" or self.args[0].type == "functionCall" or self.args[0].type == "print" or self.args[0].type == "read":
          result = self.args[0].expression(funcName, result)
      else:
          result = self.args[0].semantic(funcName, result)
      if self.args[1] is not None:
          result = self.args[1].semantic(funcName, result)

# -------------------------------------------------------------

    #conditions
    elif self.type == "if":
      print ("Entro al if")
      resultType, address = self.args[0].expression(funcName, result)
      if resultType != 'bool':
        raise Exception("Condition must be bool type")

      #GotoF
      gotof = ['gotof', address, "", ""]
      quadruples.append(gotof)
      result = self.args[1].semantic(funcName, result)
      auxQuadDesp = len(quadruples)
      
      goto = ['goto', "", "", ""]
      quadruples.append(goto)
      gotof[3] = auxQuadDesp + 1

      # Else
      if self.args[2] is not None:
        auxElseAnt = len(quadruples)
        result = self.args[2].semantic(funcName, result)
        auxElseDesp = len(quadruples)
        goto[3] = auxElseDesp

# -------------------------------------------------------------

#while
    elif self.type == "while":
      print ("Entro al while")
      auxQuadAnt = len(quadruples)
      resultType, address = self.args[0].expression(funcName, result)
      if resultType != 'bool':
        raise Exception("Condition must be bool type")

      #GotoF
      gotof = ['gotof', address, "", ""]
      quadruples.append(gotof)
      result = self.args[1].semantic(funcName, result)
      auxQuadDesp = len(quadruples)

      goto = ['goto', "", "", ""]
      quadruples.append(goto)
      gotof[3] = auxQuadDesp + 1
      goto[3] = auxQuadAnt

# -------------------------------------------------------------

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

    print(funcName)
    if self.type == "assignment":
      varName = self.args[0].args[0]
      address = ""
      auxValue = ""
      if isPrimitive(self.args[2]):
          resultType, auxValue = getType(self.args[2], funcName, currentTable)
      else:
          resultType, address = self.args[2].expression(funcName, result)
      print("auxValue" + auxValue)
      found = False
      for key in currentTable[funcName]:
      #verifies that the variable has been declared in current table
        if varName in currentTable[funcName][key].keys():
          if resultType == key:
            found = True
            if auxValue == "value":
                quadruples.append([self.args[1], currentTable[funcName][resultType][varName], "*1*", currentTable[funcName][resultType][varName]])
            else:
                quadruples.append(["=", address, "", currentTable[funcName][resultType][varName]])
            break
          else:
            raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0]) + ".")
      print(str(globalTable))
      if "global" in globalTable.keys():
          for key in globalTable["global"]:
          #verifies that the variable has been declared in global table
              if not found and (varName in globalTable["global"][key].keys()):
                  if resultType == key:
                      found = True
                      if auxValue == "value":
                          quadruples.append([self.args[1], globalTable["global"][resultType][varName], "*1*", globalTable["global"][resultType][varName]])
                      else:
                          quadruples.append(["=", address, "", globalTable["global"][resultType][varName]])
                      break
                  else:
                      raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0]) + ".")
        
      if not found:
        raise Exception("Variable '" + str(varName) + "' has not been declared. Cannot assign value.")

# -------------------------------------------------------------

    elif self.type == "megaExp":
      print("Entro a megaExp")
      result, address = self.args[0].expression(funcName, result)
      return result, address

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
      resultType = semanticCube[leftType][rightType][self.args[1]]
      
      #temp addresses
      resultAddress = auxTable.add("Aux", resultType, "aux")
      quadruples.append([self.args[1], leftAddress, rightAddress, resultAddress])

      return resultType, resultAddress

# -------------------------------------------------------------

# -------------------------------------------------------------

    elif self.type == "term":
      print("Entro a term")
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
      address = self.args[0]
      if isPrimitive(self.args[0]):
        typeGet, valOrAdd = getType(self.args[0], funcName, currentTable)
        if typeGet == "int" or typeGet == "decim":
            address = "*" + str(self.args[0]) + "*"    
        return typeGet, address
      else:
        result, address = self.args[0].expression(funcName, result)
        return result, address

# -------------------------------------------------------------
# TODO: arreglos
    elif self.type == "idCall":
        print("Entro a idCall")
        typeGet, isGlobal = getType(self.args[0], funcName, currentTable)
        if isGlobal:
            return typeGet, globalTable["global"][typeGet][self.args[0]]
        else:
            return typeGet, currentTable[funcName][typeGet][self.args[0]]
        if self.args[3] is not None:
            aux = self.args[3].expression(funcName, result)
            quadruples.append([self.args[2], result, aux, currentTable[funcName][resultType][varName]])

# -------------------------------------------------------------
        
    elif self.type == "print":
      print ("Entro a print") 
      resultType, address = self.args[0].expression(funcName, result)
      quadruples.append(["print", address, "", ""])

# -------------------------------------------------------------

    #call function. Receives id(params)
    elif self.type == "functionCall" :
        print("Entro a functionCall")
        print("Args de functionCall: " + str(self.args[1]))#parametros
        funcType = ""
        global nextReturn
      #separates a space for the function call
        quadruples.append(["ERA", self.args[0], "",""])
 #       contpar = 1

      #TODO: does this truly iterate through all possible parameters? Isn't the Gosub appended multiple times
        for i in self.args[1:]:
            print("Args del paramtero: " + str(i))
            resultType, resultAddress = i.expression(funcName, result)
            auxGosub = ["Gosub", "", "", ""]
            quadruples.append(auxGosub)

            for key in globalTable[self.args[0]].keys():
                funcType = key
                break

            auxGosub[1] = globalTable[self.args[0]][funcType][self.args[0]]
            auxAddress = auxTable.add("Aux", funcType, "aux")
            nextReturn = ["=", globalTable[self.args[0]][funcType][self.args[0]], "", auxAddress]
            quadruples.append(nextReturn)

            return funcType, auxAddress
# -------------------------------------------------------------

    elif self.type == "params":
        print("entro a params")
        resultType, address = self.args[0].expression(funcName, result)
        print(resultType)
        print(address)
        quadruples.append(["Param", address, "", "param"])
        resultType, address = self.args[1].expression(funcName, result)
        return resultType, address


# -------------------------------------------------------------

    elif self.type == "param":
        print("entro a param")
        resultType, address = self.args[0].expression(funcName, result)
        print(resultType)
        print(address)
        quadruples.append(["Param", address, "", "param"])
        return resultType, address
        

# -------------------------------------------------------------

    elif self.type == "paramF":
        print("entro a paramF")
        resultType, address = self.args[0].expression(funcName, result)
        
        return resultType, address

# -------------------------------------------------------------

    return result
