import sys
import ply.yacc as yacc
import lexer
from semantics import FuncNode
tokens = lexer.tokens

actualFunc = 'program'


## Base Code
# ---------------------------------------------------------------------------
# Program declaration
def p_program(p):
  '''program : PROGRAM ID L_BRACK variables functions mainBody R_BRACK'''
  p[0] = FuncNode('program', p[2], p[4], p[5], p[6]).semanticAll
  print ("p0 is :" + str(p[0]) + ": that's it")

# Main body (with variable declaration)
def p_mainBody(p):
  '''mainBody : MAIN L_PAR R_PAR L_BRACK variables statements R_BRACK'''
  p[0] = FuncNode('main', 'void', p[5], p[6])

# Body (without variable declaration)
def p_body(p):
  '''body : L_BRACK statements R_BRACK'''
  p[0] = p[2]
  
# Variable declaration
def p_variables(p):
  '''variables :
               | VAR type ID DOT_COMMA variables
  	       | VAR type assignment DOT_COMMA variables
  	       | VAR type ID L_KEY NUMBER R_KEY DOT_COMMA variables'''
  if len(p) > 2 :
    if len(p) > 8:
      p[0] = FuncNode('arrVar', p[3], p[2], p[5], p[8])
    else:
      p[0] = FuncNode('var', p[3], p[2], p[5])  
  #TODO: Revisar ID y assignment en punto neuralgico

# Function declaration
def p_functions(p):
  '''functions :
               | FUNCTION type ID L_PAR functionsHelp R_PAR L_BRACK variables statements R_BRACK'''
  if len(p) > 2:
    p[0] = FuncNode('function', p[3], p[2], p[5], p[8], p[9])

def p_functionsHelp(p):
  '''functionsHelp :
  		   | type ID
  		   | type ID COMMA functionsHelp2'''
  if len(p) == 3 :
    p[0] = FuncNode('params', (p[1], p[2]))
  elif len(p) >= 3 :
    p[0] = FuncNode('params', (p[1], p[2]) + p[4].args[0])
 
def p_functionsHelp2(p):
  '''functionsHelp2 : type ID
                    | type ID COMMA functionsHelp2'''
  if len(p) > 3 :
    p[0] = (p[1], p[2]) + p[4].args[0]
  else :
    p[0] = (p[1], p[2])
# ---------------------------------------------------------------------------
  
## Data Types
# ---------------------------------------------------------------------------
def p_type(p):
  '''type : INT
  	  | DECIM
          | BOOL
          | CHAR
          | STRING'''
  p[0] = p[1]
# ---------------------------------------------------------------------------

## STATEMENTS
# ---------------------------------------------------------------------------
def p_statements(p):
  '''statements :
                | statement statements'''
  if len(p) > 2:
    if p[2] is None:
      p[0] = FuncNode('statement', p[1])
    else:
      p[0] = FuncNode('statement', p[1], p[2])

def p_statement(p):
  '''statement :
                | assignment DOT_COMMA
  		| functionCall DOT_COMMA
                | ifBlock
                | whileBlock
                | forBlock
                | print DOT_COMMA
                | read DOT_COMMA
                | lineComment'''
  p[0] = p[1]
  
# Assignment
def p_assignment(p):
  '''assignment : idCall ASSIGN megaExp
                | idCall ASSIGN functionCall
                | assignIncr
                | assignDecr'''
  if len(p) > 3:
    p[0] = FuncNode('assignment', p[1], p[2], p[3])
  else:
    p[0] = p[1]
def p_assignIncr(p):
  '''assignIncr : idCall INCREMENT'''
  p[0] = FuncNode('assignmentIncrease', p[1], p[2])
def p_assignDecr(p):
  '''assignDecr : idCall DECREMENT'''
  p[0] = FuncNode('assignmentDecrease', p[1], p[2])

  
# Function call
def p_functionCall(p):
  '''functionCall : ID L_PAR functionCallParams R_PAR'''
  p[0] = FuncNode('functionCall', p[1])
  
def p_functionCallParams(p):
  '''functionCallParams : functionCallParamsOptional'''
  p[0] = FuncNode('params', p[1].args[0])
  
def p_functionCallParamsOptional(p):
  '''functionCallParamsOptional :
                                | megaExp functionCallParamsMultiple'''
  if len(p) > 2:
    #p[0] = FuncNode('params', p[1] + p[2].args[0])
    p[0] = p[1] + p[2].args[0]

#TODO: Revisar punto neuralgico para FunctionCall
def p_functionCallParamsMultiple(p):
  '''functionCallParamsMultiple :
                                | COMMA functionCallParamsOptional'''
  if len(p) > 2:
    p[0] = p[1]
  
#def p_functionCallParamsMultiple(p):
 # '''functionCallParamsMultiple : megaExp
#                                | megaExp COMMA functionCallParamsMultiple'''

  
# If block
def p_ifBlock(p):
  '''ifBlock : IF L_PAR megaExp R_PAR body optionalElse'''
  if p[6] is None:
    p[0] = FuncNode('if', p[3], p[5])
  else:
    p[0] = FuncNode('if', p[3], p[5], p[6])
  
def p_optionalElse(p):
  '''optionalElse : 
  		  | ELSE body'''
  if len(p) > 2:
    p[0] = p[2]
  
def p_whileBlock(p): 
  '''whileBlock : WHILE L_PAR megaExp R_PAR body'''
  p[0] = FuncNode('while', p[3], p[5])
  
def p_forBlock(p): 
  '''forBlock : FOR L_PAR assignment DOT_COMMA megaExp DOT_COMMA optionalAssign R_PAR body'''
  if p[7] is None:
    FuncNode('for', p[3], p[5], p[9])
  else:
    FuncNode('for', p[3], p[5], p[7], p[9])
  
def p_optionalAssign(p):
  '''optionalAssign : 
  		    | assignment'''
  p[0] = p[1]
# ---------------------------------------------------------------------------

## OPERATIONS
# ---------------------------------------------------------------------------
def p_megaExp(p):
  '''megaExp : superExp
             | superExp AND superExp
             | superExp OR superExp'''
  if len(p) > 2:
     p[0] = FuncNode('megaExp', p[1], p[2], p[3])
  else:
     p[0] = FuncNode('megaExp', p[1])
  
def p_superExp(p):
  '''superExp : exp
              | exp MORE_THAN exp
              | exp LESS_THAN exp
              | exp MORE_EQUAL exp
              | exp LESS_EQUAL exp
              | exp EQUAL exp
              | exp NOT_EQUAL exp'''
  if len(p) > 2:
     p[0] = FuncNode('superExp', p[1], p[2], p[3])
  else:
     p[0] = FuncNode('superExp', p[1])
  
def p_exp(p):
   '''exp : term
          | term PLUS exp
          | term MINUS exp'''
   if len(p) > 2:
     p[0] = FuncNode('exp', p[1], p[2], p[3])
   else:
     p[0] = FuncNode('exp', p[1])
    
def p_term(p):
   '''term : factor
           | factor TIMES term
           | factor DIVIDE term
           | factor MOD term'''
   if len(p) > 2:
     p[0] = FuncNode('term', p[1], p[2], p[3])
   else:
     p[0] = FuncNode('term', p[1])
    
def p_factor(p): 
   '''factor : NUMBER 
             | ALPHANUMERIC 
             | CHARACTER
             | BOOLEAN
             | idCall
             | L_PAR megaExp R_PAR
             | functionCall'''
   if len(p) > 2:
     p[0] = p[2]
   else:
     p[0] = p[1]
# ---------------------------------------------------------------------------

## OTHERS
def p_idCall(p):
  '''idCall : ID
  	    | ID L_KEY exp R_KEY'''
  if len(p) > 2:
    p[0] = FuncNode('idCall', p[1], p[3])
  else:
    p[0] = p[1]
# ---------------------------------------------------------------------------

## INPUT AND OUTPUT
# ---------------------------------------------------------------------------
def p_print(p):
  '''print : PRINT L_PAR print_help R_PAR'''
  if p[3] is None:
    p[0] = FuncNode('print', '')
  else:
    p[0] = FuncNode('print', p[3])
    
def p_print_help(p):
  '''print_help : 
  		| ALPHANUMERIC
  		| idCall
  		| functionCall
  		| megaExp'''
  p[0] = p[1]

def p_read(p):
  '''read : READ L_PAR idCall R_PAR'''
  p[0] = FuncNode('read', p[3])
# ---------------------------------------------------------------------------

## COMMENTS
# ---------------------------------------------------------------------------
def p_lineComment(p):
  '''lineComment : COMMENT_LINE ALPHANUMERIC END_LINE'''
  p[0] = p[2]
# ---------------------------------------------------------------------------

# Syntax Error
# ---------------------------------------------------------------------------
def p_error(p):
    print("Syntax error in input!")
    print(p)
# ---------------------------------------------------------------------------
    
# Build the parser to check on grammar's sintaxis
#parser = yacc.yacc()

#while True:
#   try:
#       s = input('code> ')
#   except EOFError:
#       break
#   if not s: continue
#   result = parser.parse(s)
#   print("Result of semantics")
#   print (result.semanticAll())
#   print("debug: your result is:")
#   print(result)
#   print("debug: And that's about it!")
