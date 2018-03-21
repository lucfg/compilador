import sys
import ply.yacc as yacc
import lexer
import symTable
tokens = lexer.tokens

actualFunc = 'program'


## Base Code
# ---------------------------------------------------------------------------
# Program declaration
def p_program(p):
  '''program : PROGRAM ID L_BRACK codeBlock R_BRACK'''
  symTable.addFuncKey(p[1], 'NP')

# Code block
def p_codeBlock(p):
  '''codeBlock : variables functions mainBody
  	       | variables mainBody
               | functions mainBody
               | mainBody'''

# Main body (with variable declaration)
def p_mainBody(p):
  '''mainBody : MAIN L_PAR R_PAR L_BRACK variables statements R_BRACK
  	      | MAIN L_PAR R_PAR L_BRACK statements R_BRACK'''

# Body (without variable declaration)
def p_body(p):
  '''body : L_BRACK statements R_BRACK'''
  
# Variable declaration
def p_variables(p):
  '''variables : VAR type ID DOT_COMMA
  	       | VAR type ID assignment DOT_COMMA'''
  symTable.symbolTable[actualFunc].addVarKey(p[3], p[2])

  
# Variable array declaration
def p_arrays(p):
  '''arrays : VAR type ID L_KEY NUMBER R_KEY DOT_COMMA'''

# Function declaration
def p_functions(p):
  '''functions : FUNCTION type ID L_PAR type ID functionsHelp R_PAR L_BRACK variables statements R_BRACK
  	       | FUNCTION type ID L_PAR type ID functionsHelp R_PAR L_BRACK statements R_BRACK'''
  actualFunc = p[3]
  symTable.addFuncKey(p[3], p[2])
def p_functionsHelp(p):
  '''functionsHelp : 
  		   | COMMA type ID functionsHelp'''
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
  '''statements : assignment DOT_COMMA
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
  '''functionCall : ID L_PAR megaExp R_PAR'''
def p_functionCallExtraP(p):
  '''functionCallExtraP : 
  											| COMMA idCall
                        | COMMA idCall functionCallExtraP'''
  
# If block
def p_ifBlock(p):
  '''ifBlock : IF L_PAR megaExp R_PAR body optionalElse'''
def p_optionalElse(p):
  '''optionalElse : 
  		  | ELSE body'''
  
def p_whileBlock(p): 
  '''whileBlock : WHILE L_PAR megaExp R_PAR body'''
  
def p_forBlock(p): 
  '''forBlock : FOR L_PAR idCall DOT_COMMA megaExp DOT_COMMA optionalAssign R_PAR body'''
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
   '''term : factor TIMES factor
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
  	    | ID L_BRACK exp R_BRACK'''
  symTable.symbolTable[actualFunc].findVarKey(p[1])
# ---------------------------------------------------------------------------

## INPUT AND OUTPUT
# ---------------------------------------------------------------------------
def p_print(p):
  '''print : PRINT L_PAR print_help ALPHANUMERIC R_PAR'''
def p_print_help(p):
  '''print_help : 
  		| MOD idCall print_help2'''
def p_print_help2(p):
  '''print_help2 : 
  		 | COMMA MOD idCall print_help2'''

def p_read(p):
  '''read : READ L_PAR MOD type COMMA readHelp idCall readHelp2 R_PAR'''
def p_readHelp(p):
  '''readHelp : 
  	      | MOD type readHelp'''
def p_readHelp2(p):
  '''readHelp2 : 
  	       | COMMA idCall readHelp2'''
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
