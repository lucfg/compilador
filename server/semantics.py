import sys
from semanticCube import *
from varTable import *

# Variable Tables
globalTable = VarTable()
localTable = VarTable(20001, 25001, 30001, 35001)
auxTable = VarTable(40001, 45001, 50001, 55001)

# Dictionary used to sort a list of parameters from certain function
listParam = {}

#Array dictionary
# {arr1: [limInf, limSup, -k, r, baseDir]}
arrayList = {}

#Matrix dictionary
# {mat1: [limInf1, limSup1, m1, r1, limInf2, limSup2, -k, r2, baseDir]}
matrixList = {}

# General counters for several rules
global funcDecCont
global funcCallCont
global contParam
global funcParamCont
global cont
funcParamCont = 1
contParam = 1
funcDecCont = 0
funcCallCont = 0

# Saves the quadruple number of a function
quadFunc = 0

# List of quadruples to send to the virtual machine
quadruples = []

# Quadruple used at the beginning of the program
gotoMain = ["GOTO","","",""]

# Saves the name of the current function used
funcContext = ""

# isPrimitive
# This method checks that the input is not a variable

# Receives: numeric value, true, false, a string
# or the name of a variable
# Returns: True or False

# Commonly used in methods who may use both variables
# and numbers or other data types.
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


# getType
# This method checks the type of a variable

# Receives: a variable, the name of the current function using it,
# and the current table in where the variable may be
# Returns: the type of the variable, as well as a dummy that might
# be used as a boolean or a string

# Commonly used in methods that need to check the type of certain
# variable
def getType(v, funcName="missingFuncName", currentTable="error"):
    print("Getting type of " + str(v))

    # Checks if the variable is a string, void or boolean type
    if isinstance(v, str):
        if v == "true" or v == "false":
            return "bool", "value"
        elif v == "void":
            return "void", "value"
        elif v[0] == "\"":
            return "string", "value"
        else:
            # Checks if the variable is in the current table
            found = False
            for key in currentTable[funcName]:
            #verifies that the variable has been declared
                if v in currentTable[funcName][key].keys():
                    found = True
                    return key, False
                    break
            # Checks if the variable is in the global table
            for key in globalTable["global"]:
            #verifies that the variable has been declared
                if not found and (v in globalTable["global"][key].keys()):
                    found = True
                    return key, True
                    break
        # If the varaible was not declared
        if not found:
            raise Exception("Variable '" + str(v) + "' has not been declared. Cannot assign value.")
    # Checks if variable is either int or decim type
    elif isinstance(v, int):
        return "int", "value"
    elif isinstance(v, float):
        return "decim", "value"
    else:
        return "void", "value"

# Object FuncNode
# Main class for the semantic, in charge of analyzing all the rules from the
# syntax
# Attributes: Type, which contains the name of the rule; and args, which are
# the rest of the possible rules on the main FuncNode
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
  # SemanticAll
  # Method in charge of calling the semantic function to start the
  # program
  def semanticAll(self):
    class_dir = []
    quadruples = []
    return self.semantic("global", class_dir)

# -------------------------------------------------------------
  # Semantic
  # Main function of the semantics file. In charge of reading all the rules
  # from the syntax and create the appropiate quadruples for the virtual
  # machine

  # Receives: the name of the current function name being used; and a result
  # parameter to store the final result
  def semantic(self, funcName, result):
    result = {}

    # Depending on the current function used, assigns the variable table to use
    if funcName is None:
      funcName = "global"
      
    if funcName == "global":
      currentTable = globalTable
    else:
      currentTable = localTable

# -------------------------------------------------------------
    # Program
    # This condition recieves a FuncNode object with type 'program'
    # Comunicates only with the method 'semantic'
    if self.type == "program":
        
      # Creates a 'goto' quadruple to make a jump to the main function
      quadruples.append(gotoMain)

      # For each element of the FuncNode, it calls the semantic method
      # for the element
      for elem in self.args:
        if elem is not None:
            
          # Checks the name of the program
          if isinstance(elem, str):
            print("Processing program " + elem + ".")
          else:
            elem.semantic(funcName, result)
      # Creates a 'END' quadruple to tell the virtual machine to stop the
      # execution
      quadruples.append(["END","","",""])

# -------------------------------------------------------------
    # Main
    # This condition recieves a FuncNode object with type 'main'
    # Comunicates only with the method 'semantic'
    elif self.type == "main":

      # Creates a 'main' quadruple as a marker
      quadruples.append(["main","","",""])
      # Assign the current quadruple position to the first 'goto' quadruple
      gotoMain[3] = len(quadruples) - 1

      # Updates the current function name
      funcName = self.type

      # Adds main as a variable to the global table and local table
      currentTable.add(funcName, "int", "main")
      localTable.add(funcName, "funcType", self.args[0])

      # For each element of the FuncNode, it calls the semantic method
      # for the element
      for elem in self.args[1:]:
        if elem is not None:
          elem.semantic(funcName, result)

# -------------------------------------------------------------
    # Function
    # This condition recieves a FuncNode object with type 'function'
    # Comunicates only with the method 'semantic'
    elif self.type == "function":
      global quadFunc

      # Updates the current function in use
      funcName = self.args[0]

      # Adds the function as a variable in the global and local tables
      currentTable.add(funcName, self.args[1],self.args[0])
      localTable.add(funcName, "funcType", self.args[0])
      auxFuncType = ["func", funcName, self.args[1],""]
      quadruples.append(auxFuncType)

      # Saves the function's quadruple position
      quadFunc = len(quadruples)

      # For each element of the FuncNode, it calls the semantic method
      # for the element
      for elem in self.args[2:]:
        if elem is not None:
          elem.semantic(funcName, result)

      # Creates quadruple to indicate the end of the function
      quadruples.append(["ENDPROC","","",""])

# -------------------------------------------------------------
    # Return
    # This condition recieves a FuncNode object with type 'return'
    # Comunicates only with the method 'expression'
    elif self.type == "return":
        # Solves the expression for the return
        resultType, address = self.args[0].expression(funcName, result)
        print("El result de RETURN" + str(resultType))
        funcType = ""

        print(str(globalTable[funcName].keys()))
        # Searches for the type of the return expression in the global table
        if resultType in globalTable[funcName].keys():

            for key in globalTable[funcName].keys():
                funcType = key
                break
            # Creates quadruple to store the result of the result in the function variable            
            quadruples.append(["ret", address,"",globalTable[funcName][funcType][funcName]])
        else:
            # Creates quadruple in case the function is of type void
            if "void" in globalTable[funcName].keys():
                quadruples.append(["ret", "/void/", "", ""])
            else:
                raise Exception("The function " + funcName + " needs to return something of type " + resultType + ".")

# -------------------------------------------------------------

    # Params
    # This condition recieves a FuncNode object with type 'params'
    elif self.type == "params":
      global listParam
      global funcDecCont
      cont = 1

      # For each parameter, add it to the parameter list and add it to the variable in
      # the current table
      for i in range(0, len(self.args[0]), 2):
        listParam["param" + str(cont)] = {self.args[0][i]:self.args[0][i+1]}
        cont = cont + 1
        funcDecCont = funcDecCont + 1
        currentTable.add(funcName, self.args[0][i], self.args[0][i+1])
      print("TU LISTA DE PARAMETROS: " + str(listParam))

# -------------------------------------------------------------
    # Var
    # This condition recieves a FuncNode object with type 'var'
    # Comunicates only with the method 'semantic'
    elif self.type == "var":
      # Adds the variable to the current table and function in use
      if self.args[0] is not None:
        if self.args[1] is not None:
          currentTable.add(funcName, self.args[1], self.args[0])
      # If more variables, calls the semantic method for them    
      if self.args[2] is not None:
        result = self.args[2].semantic(funcName, result)

# -------------------------------------------------------------
    # arrVar
    # This condition recieves a FuncNode object with type 'arrVar'
    # Comunicates only with the method 'semantic'
    elif self.type == "arrVar":
      print("Entro a arrVar")
      global arrayList

      # Makes calculations to get the actual size of the variable
      limInf = 1
      limSup = self.args[2]
      r = 1 * (limSup - limInf + 1) # m0
      minusK = (0 + limInf * 1) * -1

      print("ARRAY DECLARATION:")
      print("LIM-INF: " + str(limInf))
      print("LIM-SUP: " + str(limSup))
      print("R: " + str(r))
      print("-K: " + str(minusK))

      #Adds variable to the current table and the array dictionary
      currentTable.addArr(funcName, self.args[1], self.args[0], r)
      address = currentTable[funcName][self.args[1]][self.args[0]]
      arrayList[self.args[0]] = [limInf, limSup, minusK, r, address]

      # If more variables, calls the semantic method for them 
      if self.args[3] is not None:
          result = self.args[3].semantic(funcName, result)
      
# -------------------------------------------------------------
    # matVar
    # This condition recieves a FuncNode object with type 'matVar'
    # Comunicates only with the method 'semantic'
    elif self.type == "matVar":
      global matrixList

      # Makes calculations to get the actual size of the variable
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

      #Adds variable to the current table and the matrix dictionary
      currentTable.addArr(funcName, self.args[1], self.args[0], r2)
      address = currentTable[funcName][self.args[1]][self.args[0]]
      matrixList[self.args[0]] = [limInf1, limSup1, m1, r1, limInf2, limSup2, minusK, r2, address]

      # If more variables, calls the semantic method for them 
      if self.args[4] is not None:
          result = self.args[4].semantic(funcName, result)
      
# -------------------------------------------------------------
    # Statement
    # This condition recieves a FuncNode object with type 'statement'
    # Comunicates with both methods 'semantic' and 'expression'
    elif self.type == "statement":
      print("Entro a statement")
      # If there are statements
      if self.args[0] is not None:
        # If the next statement is a type of expression, semantic calls the
        # expression method. If not, calls the semantic method for the statement
        if self.args[0].type == "assignment" or self.args[0].type == "functionCall" or self.args[0].type == "print" or self.args[0].type == "read":
            result = self.args[0].expression(funcName, result)
        else:
            result = self.args[0].semantic(funcName, result)

# -------------------------------------------------------------
    # Statements
    # This condition recieves a FuncNode object with type 'statements'
    # Comunicates with both methods 'semantic' and 'expression'
    elif self.type == "statements":
      print("Entro a statements")
      # If the next statement is a type of expression, semantic calls the
      # expression method. If not, calls the semantic method for the statement
      if self.args[0].type == "assignment" or self.args[0].type == "functionCall" or self.args[0].type == "print" or self.args[0].type == "read":
          result = self.args[0].expression(funcName, result)
      else:
          result = self.args[0].semantic(funcName, result)
      # If more statements, calles the method more suited for the next
      # argument
      if self.args[1] is not None:
          result = self.args[1].semantic(funcName, result)

# -------------------------------------------------------------

    # If
    # This condition recieves a FuncNode object with type 'if'
    # Comunicates with both methods 'semantic' and 'expression'
    elif self.type == "if":
      print ("Entro al if")
      # Solves the expression inside the condition of the if
      resultType, address = self.args[0].expression(funcName, result)
      if resultType != 'bool':
        raise Exception("Condition must be bool type")

      # Creates gotoF quadruple to jump if the condition is false
      gotof = ['gotof', address, "", ""]
      quadruples.append(gotof)

      # Solves the expressions inside the if
      result = self.args[1].semantic(funcName, result)
      auxQuadDesp = len(quadruples)

      # Creates quadruple at the end of the if the condition is false
      goto = ['goto', "", "", ""]
      quadruples.append(goto)
      gotof[3] = auxQuadDesp + 1

      # If an else exists
      if self.args[2] is not None:
        auxElseAnt = len(quadruples)
        # Solves the expression inside the else
        result = self.args[2].semantic(funcName, result)
        auxElseDesp = len(quadruples)
        #Changes the 'goto' quadruple to jump the else if the condition
        # is false
        goto[3] = auxElseDesp

# -------------------------------------------------------------

    # While
    # This condition recieves a FuncNode object with type 'while'
    # Comunicates with both methods 'semantic' and 'expression'
    elif self.type == "while":
      print ("Entro al while")
      auxQuadAnt = len(quadruples)

      # Solves the expression inside the condition of the while
      resultType, address = self.args[0].expression(funcName, result)
      if resultType != 'bool':
        raise Exception("Condition must be bool type")

      # Creates gotoF quadruple to jump if the condition is false
      gotof = ['gotof', address, "", ""]
      quadruples.append(gotof)
      result = self.args[1].semantic(funcName, result)
      auxQuadDesp = len(quadruples)

      # Creates 'goto' quadruple to jump to the beginning of the while
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
  # Expression
  # Main function of the semantics file. In charge of evaluating all the
  # expressions from the syntax and create the appropiate quadruples for
  # the virtual machine

  # Receives: the name of the current function name being used; and a result
  # parameter to store the final result
  # Returns: the result type and the result address
  def expression(self, funcName, result):
    # Depending on the current function used, assigns the variable table to use
    if funcName == "global":
      currentTable = globalTable
    else:
      currentTable = localTable

# -------------------------------------------------------------

    print(funcName)
    # Assignment
    # This condition recieves a FuncNode object with type 'assignment'
    # Comunicates with only the method 'expression'
    if self.type == "assignment":
      print("Entro a assignment")
      # Check that the next FuncNode is an array or a matrix
      if self.args[0].type == "idCallArr" or self.args[0].type == "idCallMat":
          resultArrType, addressArr = self.args[0].expression(funcName, result)
      varName = self.args[0].args[0]
      address = ""
      auxValue = ""
      #Check if the variable is a primitive. If not, solve the type of the variable
      if isPrimitive(self.args[2]):
          resultType, auxValue = getType(self.args[2], funcName, currentTable)
      else:
          resultType, address = self.args[2].expression(funcName, result)
      print("auxValue" + auxValue)

      # Search the variable name in the current table
      found = False
      for key in currentTable[funcName]:
      #verifies that the variable has been declared in current table
        if varName in currentTable[funcName][key].keys():
          if resultType == key:
            found = True
            if auxValue == "value":
                # Check if the next variable is an array or a matrix
                if self.args[0].type == "idCallArr" or self.args[0].type == "idCallMat":
                    quadruples.append([self.args[1], currentTable[funcName][resultType][varName], "*1*", addressArr])
                else:
                    quadruples.append([self.args[1], currentTable[funcName][resultType][varName], "*1*", currentTable[funcName][resultType][varName]])
            else:
                # Check if the next variable is an array or a matrix
                if self.args[0].type == "idCallArr" or self.args[0].type == "idCallMat":
                    quadruples.append(["=", address, "", addressArr])
                else:
                    quadruples.append(["=", address, "", currentTable[funcName][resultType][varName]])
            break
          else:
            raise Exception("Cannot assign a value of different type to the variable " + str(self.args[0].args[0]) + ".")
      print(str(globalTable))
      # Search the viaraible name in the global table
      if "global" in globalTable.keys():
          for key in globalTable["global"]:
          #verifies that the variable has been declared in global table
              if not found and (varName in globalTable["global"][key].keys()):
                  if resultType == key:
                      found = True
                      if auxValue == "value":
                          # Check if the next variable is an array or a matrix
                          if self.args[0].type == "idCallArr" or selfargs[0].type == "idCallMat":
                              quadruples.append([self.args[1], globalTable["global"][resultType][varName], "*1*", addressArr])
                          else:
                              quadruples.append([self.args[1], globalTable["global"][resultType][varName], "*1*", currentTable[funcName][resultType][varName]])
                      else:
                          # Check if the next variable is an array or a matrix
                          if self.args[0].type == "idCallArr" or selfargs[0].type == "idCallMat":
                              quadruples.append(["=", address, "", addressArr])
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

        if (expType == "int"):
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

        if (expType1 == "int") and (expType2 == "int"):
            #Quadruple for first dimension
            quadruples.append(["ver", expAddress1, "*" + str(matrixList[self.args[0]][0]) + "*", "*" + str(matrixList[self.args[0]][1]) + "*"])

            aux1 = auxTable.add("Aux", expType1, "aux")
            # s1 * m1
            quadruples.append(["*", expAddress1, "*" + str(matrixList[self.args[0]][2]) + "*", aux1])

            #Quadruple for second dimension
            quadruples.append(["ver", expAddress2, "*" + str(matrixList[self.args[0]][4]) + "*", "*" + str(matrixList[self.args[0]][5]) + "*"])

            aux2 = auxTable.add("Aux", expType2, "aux")
            # (s1 * m1) = s2
            quadruples.append(["+", aux1, expAddress2, aux2])
        
            aux3 = auxTable.add("Aux", expType2, "aux")
            # + (-K)
            quadruples.append(["+", aux2, "*" +str(matrixList[self.args[0]][6]) + "*", aux3])

            aux4 = auxTable.add("Aux", expType2, "aux")
            # + dirBase
            quadruples.append(["+", aux3, matrixList[self.args[0]][8], aux4])

            if isGlobal:
                return matTypeGet, ("(" + str(aux4) + ")")
            else:
                return matTypeGet, ("(" + str(aux4) + ")")
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
        funcCallCont = 0
        contParam = 1
        funcType = ""
        global nextReturn
        global funcContext
        funcContext = self.args[0]
        print("FUNCCONTEXT: " + str(self.args[0]))

      #separates a space for the function call
        quadruples.append(["ERA", "/" + self.args[0] + "/", "",""])

        #Checking parameters
        for i in self.args[1:]:
            print("Args del parametro: " + str(i))
            if not (i is None):
                resultType, resultAddress = i.expression(funcName, result)

                print("FUNCCALLCONT: " + str(funcCallCont))
                print("FUNCDECCONT: " + str(funcDecCont))
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
        print("FUNCCONTEXT: " + str(funcContext))
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
        print("FUNCCONTEXT: " + str(funcContext))
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
