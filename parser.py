import sys
import ply.yacc as yacc
import lexer
tokens = lexer.tokens


def p_assign(p):
 	'''assign : NAME EQUALS expr'''
  
#RESERVED_program
def p_program(p):
  '''program : RESERVED ID L_BRACK codeBlock R_BRACK'''

def p_codeBlock(p):
  '''codeBlock : variables functions mainBody
  						 | variables mainBody
               | functions mainBody
               | mainBody'''
  
# RESERVED_var
def p_variables(p):
  '''variables : RESERVED type ID
  						 | RESERVED type ID assignment'''
  
def p_arrays(p):
  '''RESERVED type ID L_KEY NUMBER R_KEY'''
  
# Can be INT, DECIM, BOOL, CHAR, or STRING
# All of them are reserved words for the lexer
def p_type(p):
  '''type : RESERVED'''

# RESERVED_func
def p_functions(p):
  '''functions : RESERVED type ID L_PAR type ID functionHelp R_PAR L_BRACK variables statements R_BRACK
  						 | RESERVED type ID L_PAR type ID functionHelp R_PAR L_BRACK statements R_BRACK'''
def p_functionsHelp(p):
  '''functionsHelp : 
  								 | COMMA type ID functionsHelp'''

# RESERVED_main
def p_mainBody(p):
  '''mainBody : RESERVED L_PAR R_PAR L_BRACK variables statements R_BRACK
  						| RESERVED L_PAR R_PAR L_BRACK statements R_BRACK'''
  
def p_body(p):
  '''body : L_BRACK statements R_BRACK'''

## STATEMENTS
# All statements
def p_statements(p):
  '''statements : assignment DOT_COMMA
  							| functionCall DOT_COMMA
                | ifBlock
                | whileBlock
                | forBlock'''

# Assignment
def p_assignment(p):
  '''assignment : ID optionalArrInd EQUAL megaExp
                | ID optionalArrInd EQUAL functionCall
                | ID optionalArrInd INCREMENT 
                | ID optionalArrInd DECREMENT'''

def P_optionalArrInd(p):
  '''optionalArrInd : 
  										| L_BRACK exp R_BRACK'''
  
# Function call
def p_functionCall(p):
  '''functionCall : ID L_PAR megaExp R_PAR'''
def p_functionCallExtraP(p):
  '''functionCallExtraP : 
  											| COMMA ID optionalArrInd
                        | COMMA ID optionalArrInd functionCallExtraP'''
  
# If block
def p_ifBlock(p): # RESERVED = IF
  '''ifBlock : RESERVED L_PAR megaExp R_PAR body optionalElse'''
def p_optionalElse(p): #RESERVED = ELSE
  '''optionalElse : 
  								| RESERVED body'''
  
def p_whileBlock(p): #RESERVED = WHILE
  '''whileBlock : RESERVED L_PAR megaExp R_PAR body'''
  
def p_forBlock(p): #RESERVED = FOR
  '''forBLock : L_PAR ID DOT_COMMA megaExp DOT_COMMA optionalAssignment R_PAR body'''
def p_optionalAssign(p):
  '''optionalAssign : 
  									| assignment'''

# Operations
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
   '''factor : NUMBER | ALPHANUMERIC | BOOLEAN
             | ID
             | ID L_BRACK exp R_BRACK
             | L_PAR megaExp R_PAR
             | functionCall'''
    
# Print & Read
def p_print(p):
  '''print : PRINT L_PAR MOD ID printHelp QUOTE ALPHANUMERIC QUOTE R_PAR'''
  
def p_print_help(p):
  '''printHelp : 
  						 | COMMA MOD ID printHelp'''

def p_read(p):
  '''read : READ L_PAR MOD type COMMA readHelp ID readHelp2 R_PAR'''
  
def p_readHelp(p):
  '''readHelp : 
  						| MOD type readHelp'''
  
def p_readHelp2(p):
  '''readHelp2 : 
  						 | COMMA ID readHelp2'''
  
## COMMENTS
def p_lineComment(p):
  '''lineComment : COMMENT_LINE ALPHANUMERIC END_LINE'''
    
# Build the parser to check on grammar's sintaxis
yacc.yacc()
