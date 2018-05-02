
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
    parse_tree = parser.parse(input_string) 
    print ('Successfully built parse tree:')
    print (parse_tree)
    print(parse_tree.semanticAll())
        #debug
    #print ("Your quads: " + str(quadruples))
    for i in range (0, len(quadruples), 1):
        print (str(i) + str(quadruples[i]))
    print("Global: " + str(globalTable.items()))
    print("Local: " + str(localTable.items()))
    print("Aux: " + str(auxTable.items()))

    jsonQuads = ""
    for quad in quadruples:
        jsonQuads += "{\"quad\":" + str(quad) + "},"
    #print ("{" + "\"quadruples\":" + str(quadruples) + "}")
    print (str(quadruples))
    #if isinstance(parse_tree, FuncNode):
#        print (parse_tree.semanticAll())
        # print (memory[0])
        # print (virtual_machine(cuadruplos, memory[0]))
#    else:
#        print ('Failed program')
if len(sys.argv) < 2:
    while True:
        try:
            s = input('code> ')
        except EOFError:
            break
        if not s: continue
        test(s)
else:
    i = 0
    s = ""
    for arg in sys.argv:
        if i == 1:
            s = str(arg)
        i += 1

    test(s)
