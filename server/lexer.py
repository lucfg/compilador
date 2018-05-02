import ply.lex as lex

# Reserved Words
reserved = {
  #Input & Output
  'print' : 'PRINT',
  'read' : 'READ',
  #Key Words
  'main' : 'MAIN',
  'program' : 'PROGRAM',
  'func' : 'FUNCTION',
  'var' : 'VAR',
  'true' : 'BOOLEAN',
  'false' : 'BOOLEAN',
  # Conditionals
	'if' : 'IF',
  'else' : 'ELSE',
  'while' : 'WHILE',
  # Primitives
  'int' : 'INT',
  'decim' : 'DECIM',
  'bool' : 'BOOL',
  'char' : 'CHAR',
  'string' : 'STRING'
}
tokens = [
  	# Primitives	
  	'ID',
  	# Data
    'INTEGER', 'DECIMAL', 'ALPHANUMERIC', 'CHARACTER',
  	# Arithmetic operators
		'INCREMENT', 'DECREMENT','PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MOD',    
    # Boolean operators
    'EQUAL','NOT_EQUAL','MORE_EQUAL','LESS_EQUAL', 
    'MORE_THAN', 'LESS_THAN', 'AND', 'OR',
    # Block delimitators
    'L_KEY', 'R_KEY', 'L_BRACK', 'R_BRACK', 'L_PAR', 'R_PAR',  
    # Others
    'ASSIGN', 'COMMA', 'DOT_COMMA', 'COMMENT_LINE', 'END_LINE'
		] + list(reserved.values())

# Ignore whitespaces
t_ignore = ' \t'

# Primitives
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    if t.value in reserved:
      t.type = reserved[t.value]
    return t
  
# Data

def t_DECIMAL(t):
    r'[0-9]*\.[0-9]+'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'\d+'
    t.value = int(t.value)
    return t
    
# FALTA ALPHANUMERIC ////////////////////FALTA ESTO//////////////////////
t_CHARACTER = r'[a-zA-Z_]'
t_ALPHANUMERIC = r'\"[a-zA-Z_0-9\s]*\"'
# FALTA BOOLEAN ////////////////////FALTA ESTO//////////////////////

# Arithmetic operators
t_INCREMENT = r'\+\+'
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
t_OR = r'\|\|'

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
t_COMMENT_LINE = r'\#.*'
t_END_LINE = r'\n'

# The lexer is built for token generation
lexer = lex.lex()

def prueba():
    lex.input('''program programa {main () {var int c; c=2;}}''')
    while True:
        tok = lexer.token()
        if not tok:
            break      # No more input
        print(tok)
