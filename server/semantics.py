import sys
from semanticCube import *
from varTable import *

globalTable = VarTable()
localTable = VarTable(20001, 25001, 30001, 35001)
auxTable = VarTable(40001, 45001, 50001, 55001)

listParam = {}

#Array dictionary
# {arr1: [limInf, limSup, -k, r, baseDir]}
arrayList = {}

#Matrix dictionary
# {mat1: [limInf1, limSup1, m1, r1, limInf2, limSup2, -k, r2, baseDir]}
matrixList = {}

global funcDecCont
global funcCallCont
funcDecCont = 0
funcCallCont = 0

quadFunc = 0

quadruples = []
gotoMain = ["GOTO","","",""]
global contParam
global funcParamCont
global cont
funcParamCont = 1
contParam = 1

funcContext = ""

def isPrimitive(t):
    if isinstance(t, str):
        if t == "true" or t == "false":
            return True
        elif t == "void":
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
        elif v == "void":
            return "void", "value"
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

 #     quadruples.append(["ret","*0*","",""])
# -------------------------------------------------------------

    elif self.type == "function":
      global quadFunc
      funcName = self.args[0]
      currentTable.add(funcName, self.args[1],self.args[0])
      localTable.add(funcName, "funcType", self.args[0])
      auxFuncType = ["func", funcName, self.args[1],""]
      quadruples.append(auxFuncType)
      quadFunc = len(quadruples)


      for elem in self.args[2:]:
        if elem is not None:
          elem.semantic(funcName, result)

      quadruples.append(["ENDPROC","","",""])

# -------------------------------------------------------------

    elif self.type == "return":
        resultType, address = self.args[0].expression(funcName, result)
        print("El result de RETURN" + str(resultType))
        funcType = ""

        print(str(globalTable[funcName].keys()))
        if resultType in globalTable[funcName].keys():

            for key in globalTable[funcName].keys():
                funcType = key
                break
            
            quadruples.append(["ret", address,"",globalTable[funcName][funcType][funcName]])
        else:
            if "void" in globalTable[funcName].keys():
                quadruples.append(["ret", "/void/", "", ""])
            else:
                raise Exception("The function " + funcName + " needs to return something of type " + resultType + ".")

# -------------------------------------------------------------

    #TODO: PARAMS
    elif self.type == "params":
      global listParam
      global funcDecCont
      cont = 1
      for i in range(0, len(self.args[0]), 2):
        listParam["param" + str(cont)] = {self.args[0][i]:self.args[0][i+1]}
        cont = cont + 1
        funcDecCont = funcDecCont + 1
        currentTable.add(funcName, self.args[0][i], self.args[0][i+1])
      print("TU LISTA DE PARAMETROS: " + str(listParam))

# -------------------------------------------------------------

    elif self.type == "var":
      if self.args[0] is not None:
        if self.args[1] is not None:
          currentTable.add(funcName, self.args[1], self.args[0])
      if self.args[2] is not None:
        result = self.args[2].semantic(funcName, result)

# -------------------------------------------------------------

    elif self.type == "arrVar":
      global arrayList

      limInf = 1
      limSup = self.args[2]
      r = 1 * (limSup - limInf + 1) # m0
      minusK = (0 + limInf * 1) * -1

      print("ARRAY DECLARATION:")
      print("LIM-INF: " + str(limInf))
      print("LIM-SUP: " + str(limSup))
      print("R: " + str(r))
      print("-K: " + str(minusK))

      #Adds id to currentTable
      currentTable.addArr(funcName, self.args[1], self.args[0], r)
      address = currentTable[funcName][self.args[1]][self.args[0]]
      arrayList[self.args[0]] = [limInf, limSup, minusK, r, address]

      if self.args[3] is not None:
          result = self.args[3].semantic(funcName, result)
      
# -------------------------------------------------------------

    elif self.type == "matVar":
      global matrixList

      limInf1 = 1
      limSup1 = self.args[2]
      limInf2 = 1
      limSup2 = self.args[3]
      
      r1 = 1 * (limSup1 - limInf1 + 1)
      r2 = r1 * (limSup2 - limInf2 + 1) # m0
      
      m1 = int(r2 / (limSup1 - limInf1 + 1))
      sumAux = 0 + limInf1 * m1

      m2 = int(m1 / (limSup2 - limInf2 + 1))
      sumAux = sumAux + limInf2 * m2
      minusK = sumAux * -1

      print("MATRIX DECLARATION:")
      print("LIM-INF1: " + str(limInf1))
      print("LIM-SUP1: " + str(limSup1))
      print("R1: " + str(r1))
      print("M1: " + str(m1))

      print("LIM-INF2: " + str(limInf2))
      print("LIM-SUP2: " + str(limSup2))
      print("R2: " + str(r2))
      print("M2: " + str(m2))
      print("-K: " + str(minusK))

      #Adds id to currentTable
      currentTable.addArr(funcName, self.args[1], self.args[0], r2)
      address = currentTable[funcName][self.args[1]][self.args[0]]
      matrixList[self.args[0]] = [limInf1, limSup1, m1, r1, limInf2, limSup2, minusK, r2, address]

      if self.args[4] is not None:
          result = self.args[4].semantic(funcName, result)
      
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
            raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0].args[0]) + ".")
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
                      raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0].args[0]) + ".")
        
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
        typeGet, valorAdd = getType(self.args[0], funcName, currentTable)
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
        #Gets type of variable and checks if it's global
        typeGet, isGlobal = getType(self.args[0], funcName, currentTable)
        
        if isGlobal:
            return typeGet, globalTable["global"][typeGet][self.args[0]]
        else:
            return typeGet, currentTable[funcName][typeGet][self.args[0]]

# -------------------------------------------------------------

    elif self.type == "idCallArr":
        print("Entro a idCallArr")
        #Gets type of variable and checks if it's global
        arrTypeGet, isGlobal = getType(self.args[0], funcName, currentTable)

        expType, expAddress = self.args[1].expression(funcName, currentTable)

        if expType is "int":
            quadruples.append(["ver", expAddress, "*" + str(arrayList[self.args[0]][0]) + "*", "*" + str(arrayList[self.args[0]][1]) + "*"])

            aux1 = auxTable.add("Aux", expType, "aux")
            # + (-K)
            quadruples.append(["+", expAddress, "*" +str(arrayList[self.args[0]][2]) + "*", aux1])

            aux2 = auxTable.add("Aux", expType, "aux")
            # + dirBase
            quadruples.append(["+", aux1, "*" + str(arrayList[self.args[0]][4]) + "*", aux2])

            if isGlobal:
                return arrTypeGet, ("(" + str(aux2) + ")")
            else:
                return arrTypeGet, ("(" + str(aux2) + ")")
        else:
            raise Exception("Index must be of type int.")

        #globalTable["global"][arrTypeGet][self.args[0]]
        
# -------------------------------------------------------------

    elif self.type == "idCallMat":
        print("Entro a idCallMat")
        #Gets type of variable and checks if it's global
        matTypeGet, isGlobal = getType(self.args[0], funcName, currentTable)

        expType1, expAddress1 = self.args[1].expression(funcName, currentTable)
        expType2, expAddress2 = self.args[2].expression(funcName, currentTable)

        if expType1 is "int" and expType2 is "int":
            #Quadruples for first dimension
            quadruples.append(["ver", expAddress1, "*" + str(matrixList[self.args[0]][0]) + "*", "*" + str(matrixList[self.args[0]][1]) + "*"])
            aux1 = auxTable.add("Aux", expType1, "aux")
            # s1 * m1
            quadruples.append
        

            aux1 = auxTable.add("Aux", expType, "aux")
            # + (-K)
            quadruples.append(["+", expAddress, "*" +str(arrayList[self.args[0]][2]) + "*", aux1])

            aux2 = auxTable.add("Aux", expType, "aux")
            # + dirBase
            quadruples.append(["+", aux1, arrayList[self.args[0]][4], aux2])

            if isGlobal:
                return matTypeGet, aux2
            else:
                return matTypeGet, aux2
        else:
            raise Exception("Index must be of type int.")

        #globalTable["global"][arrTypeGet][self.args[0]]
        
# -------------------------------------------------------------
        
    elif self.type == "print":
      print ("Entro a print") 
      resultType, address = self.args[0].expression(funcName, result)
      quadruples.append(["print", address, "", ""])

# -------------------------------------------------------------

    elif self.type == "read":
      print ("Entro a read") 
      resultType, address = self.args[0].expression(funcName, result)
      quadruples.append(["read", "", "", address])

# -------------------------------------------------------------

    #call function. Receives id(params)
    elif self.type == "functionCall" :
        print("Entro a functionCall")
        print("Args de functionCall: " + str(self.args[1]))#parameters
        global contParam
        global funcCallCont
        contParam = 1
        funcType = ""
        global nextReturn
        global funcContext
        funcContext = self.args[0]

      #separates a space for the function call
        quadruples.append(["ERA", "/" + self.args[0] + "/", "",""])

        #Checking parameters
        for i in self.args[1:]:
            print("Args del parametro: " + str(i))
            if not (i is None):
                resultType, resultAddress = i.expression(funcName, result)

                if funcCallCont != funcDecCont:
                    raise Exception("The number of parameters does not match up.")
            
            auxGosub = ["Gosub", "", "", ""]
            quadruples.append(auxGosub)

            for key in globalTable[self.args[0]].keys():
                funcType = key
                break

            auxGosub[3] = quadFunc - 1
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
        
        paramAddress = auxTable.add("Aux", resultType, "aux")
        auxAddress = localTable[funcContext][resultType][listParam["param" + str(contParam)][resultType]]
        quadruples.append(["param", address, "*" + str(auxAddress) + "*", paramAddress])

        if not (resultType in listParam["param" + str(contParam)].keys()):
            raise Exception("Parameter given not of type " + resultType)

 #       quadruples.append(["=", paramAddress, "", auxAddress])
        
        contParam = contParam + 1
        funcCallCont = funcCallCont + 1
        
        resultType, address = self.args[1].expression(funcName, result)
        return resultType, address


# -------------------------------------------------------------

    elif self.type == "param":
        print("entro a param")
        resultType, address = self.args[0].expression(funcName, result)
        print(resultType)
        print(address)

        paramCont = 0

        paramAddress = auxTable.add("Aux", resultType, "aux")
        auxAddress = localTable[funcContext][resultType][listParam["param" + str(contParam)][resultType]]
        quadruples.append(["param", address, "*" + str(auxAddress) + "*", paramAddress])

        if not (resultType in listParam["param" + str(contParam)].keys()):
            raise Exception("Parameter given not of type " + resultType)

 #       quadruples.append(["asignParam", paramAddress, "", auxAddress])
        
        contParam = contParam + 1
        funcCallCont = funcCallCont + 1
        
        return resultType, address
        

# -------------------------------------------------------------

    elif self.type == "paramF":
        print("entro a paramF")
        resultType, address = self.args[0].expression(funcName, result)
        
        return resultType, address

# -------------------------------------------------------------

    return result
