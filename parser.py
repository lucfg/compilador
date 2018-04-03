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
  p[0] = FuncNode('program', p[2], p[4], p[5], p[6])

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
  	       | VAR type assignment DOT_COMMA variables'''
  if len(p) > 2 :
    p[0] = FuncNode('var', p[3], p[2], p[5])  
  #TODO: Revisar ID y assignment en punto neuralgico
  
# Variable array declaration
def p_arrays(p):
  '''arrays : VAR type ID L_KEY NUMBER R_KEY DOT_COMMA'''
  p[0] = FuncNode('arrVar', p[3], p[2], p[5])

# Function declaration
def p_functions(p):
  '''functions :
               | FUNCTION type ID L_PAR functionsHelp R_PAR L_BRACK variables statements R_BRACK'''
  p[0] = FuncNode('function', p[3], p[2], p[5], p[8], p[9])

def p_functionsHelp(p):
  '''functionsHelp :
  		   | type ID
  		   | type ID COMMA functionsHelp2'''
  if len(p) > 3 :
    p[0] = FuncNode('params', (p[1], p[2]) + p[4].args[0])
  else :
    p[0] = FuncNode('params', (p[1], p[2]))
 
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
# ---------------------------------------------------------------------------

## STATEMENTS
# ---------------------------------------------------------------------------
def p_statements(p):
  '''statements:
               | statement statements'''

def p_statement(p):
  '''statement :
                | assignment DOT_COMMA
  		| functionCall DOT_COMMA
                | ifBlock
                | whileBlock
                | forBlock
                | print DOT_COMMA
                | read DOT_COMMA
                | lineComment
                | arrays DOT_COMMA'''
  
# Assignment
def p_assignment(p):
  '''assignment : idCall ASSIGN megaExp
                | idCall ASSIGN functionCall
                | idCall INCREMENT 
                | idCall DECREMENT'''

#def p_optionalArrInd(p):
#  '''optionalArrInd : 
#  		    | L_BRACK exp R_BRACK'''
  
# Function call
def p_functionCall(p):
  '''functionCall : ID L_PAR functionCallParams R_PAR'''
def p_functionCallParams(p):
  '''functionCallParams : functionCallParamsOptional
                        | functionCallParamsMultiple'''
def p_functionCallParamsOptional(p):
  '''functionCallParamsOptional :
                                | megaExp'''
def p_functionCallParamsMultiple(p):
  '''functionCallParamsMultiple : megaExp
                                | megaExp COMMA functionCallParamsMultiple'''

  
# If block
def p_ifBlock(p):
  '''ifBlock : IF L_PAR megaExp R_PAR body optionalElse'''
def p_optionalElse(p):
  '''optionalElse : 
  		  | ELSE body'''
  
def p_whileBlock(p): 
  '''whileBlock : WHILE L_PAR megaExp R_PAR body'''
  
def p_forBlock(p): 
  '''forBlock : FOR L_PAR assignment DOT_COMMA megaExp DOT_COMMA optionalAssign R_PAR body'''
def p_optionalAssign(p):
  '''optionalAssign : 
  		    | assignment'''
# ---------------------------------------------------------------------------

## OPERATIONS
# ---------------------------------------------------------------------------
def p_megaExp(p):
  '''megaExp : superExp
             | superExp AND superExp
             | superExp OR superExp'''
  
def p_superExp(p):
  '''superExp : exp
              | exp MORE_THAN exp
              | exp LESS_THAN exp
              | exp MORE_EQUAL exp
              | exp LESS_EQUAL exp
              | exp EQUAL exp
              | exp NOT_EQUAL exp'''
  
def p_exp(p):
   '''exp : term
          | term PLUS term
          | term MINUS term'''
    
def p_term(p):
   '''term : factor
           | factor TIMES factor
           | factor DIVIDE factor
           | factor MOD factor'''
    
def p_factor(p): 
   '''factor : NUMBER 
             | ALPHANUMERIC 
             | CHARACTER
             | BOOLEAN
             | idCall
             | L_PAR megaExp R_PAR
             | functionCall'''
# ---------------------------------------------------------------------------

## OTHERS
def p_idCall(p):
  '''idCall : ID
  	    | ID L_KEY exp R_KEY'''
 # symTable.symbolTable[actualFunc].findVarKey(p[1])
# ---------------------------------------------------------------------------

## INPUT AND OUTPUT
# ---------------------------------------------------------------------------
def p_print(p):
  '''print : PRINT L_PAR print_help R_PAR'''
def p_print_help(p):
  '''print_help : 
  		| ALPHANUMERIC
  		| idCall
  		| functionCall'''

def p_read(p):
  '''read : READ L_PAR idCall R_PAR'''
# ---------------------------------------------------------------------------

## COMMENTS
# ---------------------------------------------------------------------------
def p_lineComment(p):
  '''lineComment : COMMENT_LINE ALPHANUMERIC END_LINE'''
# ---------------------------------------------------------------------------

# Syntax Error
# ---------------------------------------------------------------------------
def p_error(p):
    print("Syntax error in input!")
    print(p)
# ---------------------------------------------------------------------------
    
# Build the parser to check on grammar's sintaxis
parser = yacc.yacc()

while True:
   try:
       s = input('code> ')
   except EOFError:
       break
   if not s: continue
   result = parser.parse(s)
   print(result)
