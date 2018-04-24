
import sys
import ply.lex as lex
import ply.yacc as yacc
from semantics import *
from parser import *
from lexer import *
lexer = lex.lex() 
# program_file = str(sys.argv[1])
# f = open(program_file, 'r').read()
# print (f)
   

def test(input_string):
    lexer.input(input_string)
    print("Tokens generated by lexer:")
    print (list(lexer))
    parser = yacc.yacc() 
    parse_tree = parser.parse(input_string, lexer=lexer) 
    print ('Successfully built parse tree:')
    print (parse_tree)
    if isinstance(parse_tree, FuncNode):
        print (parse_tree.semantic_all())
        # print (memory[0])
        # print (virtual_machine(cuadruplos, memory[0]))
    else:
        print ('Failed program')


while True:
    try:
        s = input('code> ')
    except EOFError:
        break
    if not s: continue
    test(s)