import ply.lex as lex

# Reserved Words
reserved = {
  # Conditionals
	'if' : 'IF',
  'else' : 'ELSE',
	'for' : 'FOR',
  'while' : 'WHILE',
  # Primitives
  'int' : 'INT',
  'decim' : 'DECIM',
  'bool' : 'BOOL',
  'char' : 'CHAR',
  'string' : 'STRING',
  #Key Words
  'main' : 'MAIN',
  'program' : 'PROGRAM',
  'func' : 'FUNCTION',
  'var' : 'VAR'
}
tokens = [
  	# Primitives	
  	'RESERVED','ID',
  	# Data
    'NUMBER', 'ALPHANUMERIC', 'CHARACTER', 'BOOLEAN',
  	# Arithmetic operators
		'INCREMENT', 'DECREMENT','PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',    
    # Boolean operators
    'EQUAL','NOT_EQUAL','MORE_EQUAL','LESS_EQUAL', 
    'MORE_THAN', 'LESS_THAN', 'AND', 'OR'
    # Block delimitators
    'L_KEY', 'R_KEY', 'L_BRACK', 'R_BRACK', 'L_PAR', 'R_PAR',  
    # Others
    'ASSIGN', 'COMMA', 'DOT_COMMA', 'COMMENT_LINE', 'END_LINE','PRINT','READ','QUOTE'
		] + list(reserved.values())

# Ignore whitespaces
t_ignore = ' \t'

# Primitives
def t_RESERVED(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t
t_ID = r'[a-zA-Z_][a-zA-Z_0-9]*'
  
# Data
def t_NUMBER(t):
 	r'\d+'
 	t.value = int(t.value)
 	return t
# FALTA ALPHANUMERIC ////////////////////FALTA ESTO//////////////////////
t_CHARACTER = r'[a-zA-Z_]'
# FALTA BOOLEAN ////////////////////FALTA ESTO//////////////////////

# Arithmetic operators
t_INCREMENT = r'\++'
t_DECREMENT = r'--'
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MOD = r'%'

#Boolean operators
t_EQUAL = r'\=='
t_NOT_EQUAL = r'\!='
t_MORE_EQUAL = r'\>='
t_LESS_EQUAL = r'\<='
t_MORE_THAN = r'\>'
t_LESS_THAN = r'\<'
t_AND = r'&&'
t_OR = r'||'

#Block delimitators
t_L_KEY = r'\['
t_R_KEY = r'\]'
t_L_BRACK = r'\{'
t_R_BRACK = r'\}'
t_L_PAR = r'\('
t_R_PAR = r'\)'

#Conditionals
#Others
t_ASSIGN = r'='
t_COMMA = r'\,'
t_DOT_COMMA = r';'
t_COMMENT_LINE = r'#'
t_END_LINE = r'\n'
t_PRINT = r'\print'
t_READ = r'\read'
t_QUOTE = r'\"'

# The lexer is built for token generation
lex.lex()