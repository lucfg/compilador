
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'ALPHANUMERIC AND ASSIGN BOOL BOOLEAN BOOLEAN CHAR CHARACTER COMMA COMMENT_LINE DECIM DECREMENT DIVIDE DOT_COMMA ELSE END_LINE EQUAL FOR FUNCTION ID IF INCREMENT INT LESS_EQUAL LESS_THAN L_BRACK L_KEY L_PAR MAIN MINUS MOD MORE_EQUAL MORE_THAN NOT_EQUAL NUMBER OR PLUS PRINT PROGRAM READ R_BRACK R_KEY R_PAR STRING TIMES VAR WHILEprogram : PROGRAM ID L_BRACK variables functions mainBody R_BRACKmainBody : MAIN L_PAR R_PAR L_BRACK variables statements R_BRACKbody : L_BRACK statements R_BRACKvariables :\n               | VAR type ID DOT_COMMA variables\n  \t       | VAR type assignment DOT_COMMA variablesarrays : VAR type ID L_KEY NUMBER R_KEY DOT_COMMAfunctions :\n               | FUNCTION type ID L_PAR functionsHelp R_PAR L_BRACK variables statements R_BRACKfunctionsHelp :\n  \t\t   | type ID\n  \t\t   | type ID COMMA functionsHelp2functionsHelp2 : type ID\n                    | type ID COMMA functionsHelp2type : INT\n  \t  | DECIM\n          | BOOL\n          | CHAR\n          | STRINGstatements :\n                | statement statementsstatement :\n                | assignment DOT_COMMA\n  \t\t| functionCall DOT_COMMA\n                | ifBlock\n                | whileBlock\n                | forBlock\n                | print DOT_COMMA\n                | read DOT_COMMA\n                | lineComment\n                | arrays DOT_COMMAassignment : idCall ASSIGN megaExp\n                | idCall ASSIGN functionCall\n                | idCall INCREMENT \n                | idCall DECREMENTfunctionCall : ID L_PAR functionCallParams R_PARfunctionCallParams : functionCallParamsOptionalfunctionCallParamsOptional :\n                                | megaExp functionCallParamsMultiplefunctionCallParamsMultiple :\n                                | COMMA functionCallParamsOptionalifBlock : IF L_PAR megaExp R_PAR body optionalElseoptionalElse : \n  \t\t  | ELSE bodywhileBlock : WHILE L_PAR megaExp R_PAR bodyforBlock : FOR L_PAR assignment DOT_COMMA megaExp DOT_COMMA optionalAssign R_PAR bodyoptionalAssign : \n  \t\t    | assignmentmegaExp : superExp\n             | superExp AND superExp\n             | superExp OR superExpsuperExp : exp\n              | exp MORE_THAN exp\n              | exp LESS_THAN exp\n              | exp MORE_EQUAL exp\n              | exp LESS_EQUAL exp\n              | exp EQUAL exp\n              | exp NOT_EQUAL expexp : term\n          | term PLUS exp\n          | term MINUS expterm : factor\n           | factor TIMES term\n           | factor DIVIDE term\n           | factor MOD termfactor : NUMBER \n             | ALPHANUMERIC \n             | CHARACTER\n             | BOOLEAN\n             | idCall\n             | L_PAR megaExp R_PAR\n             | functionCallidCall : ID\n  \t    | ID L_KEY exp R_KEYprint : PRINT L_PAR print_help R_PARprint_help : \n  \t\t| ALPHANUMERIC\n  \t\t| idCall\n  \t\t| functionCall\n  \t\t| megaExpread : READ L_PAR idCall R_PARlineComment : COMMENT_LINE ALPHANUMERIC END_LINE'
    
_lr_action_items = {'PROGRAM':([0,],[2,]),'$end':([1,21,],[0,-1,]),'ID':([2,9,10,11,12,13,14,17,24,25,26,27,32,42,44,50,51,53,55,56,57,58,59,61,62,63,64,65,66,67,68,69,90,93,94,95,98,108,111,114,115,116,117,118,119,120,121,122,123,125,126,128,140,146,152,153,154,158,161,163,164,169,],[3,18,-15,-16,-17,-18,-19,23,-4,33,-4,48,-5,33,-6,-4,70,33,33,33,33,33,33,33,33,33,33,33,33,33,33,48,48,-25,-26,-27,-30,-4,33,-23,-24,-28,-29,-31,33,33,133,33,133,141,142,48,-82,33,-43,48,-45,-42,133,-44,-3,-46,]),'L_BRACK':([3,30,71,144,145,159,168,],[4,50,108,153,153,153,153,]),'FUNCTION':([4,5,24,26,32,44,],[-4,8,-4,-4,-5,-6,]),'MAIN':([4,5,7,24,26,32,44,151,],[-4,-8,16,-4,-4,-5,-6,-9,]),'VAR':([4,24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[6,6,6,-5,-6,6,106,106,-25,-26,-27,-30,6,-23,-24,-28,-29,-31,106,-82,-43,106,-45,-42,-44,-3,-46,]),'INT':([6,8,31,106,107,150,],[10,10,10,10,10,10,]),'DECIM':([6,8,31,106,107,150,],[11,11,11,11,11,11,]),'BOOL':([6,8,31,106,107,150,],[12,12,12,12,12,12,]),'CHAR':([6,8,31,106,107,150,],[13,13,13,13,13,13,]),'STRING':([6,8,31,106,107,150,],[14,14,14,14,14,14,]),'R_BRACK':([15,24,26,32,44,50,69,89,90,93,94,95,98,108,112,113,114,115,116,117,118,128,140,143,152,153,154,158,160,163,164,169,],[21,-4,-4,-5,-6,-4,-20,112,-20,-25,-26,-27,-30,-4,-2,-21,-23,-24,-28,-29,-31,-20,-82,151,-43,-20,-45,-42,164,-44,-3,-46,]),'L_PAR':([16,23,25,27,33,42,48,53,55,56,57,58,59,61,62,63,64,65,66,67,68,100,101,102,103,104,111,119,120,122,146,],[22,31,42,42,53,42,53,42,42,42,42,42,42,42,42,42,42,42,42,42,42,119,120,121,122,123,42,42,42,42,42,]),'DOT_COMMA':([18,19,28,29,33,35,36,37,38,39,40,41,43,45,46,47,48,49,54,75,76,77,78,79,80,81,82,83,84,85,86,87,88,91,92,96,97,99,109,132,147,148,155,162,167,],[24,26,-34,-35,-73,-59,-62,-66,-67,-68,-69,-70,-72,-32,-33,-49,-73,-52,-74,-60,-61,-63,-64,-65,-71,-50,-51,-53,-54,-55,-56,-57,-58,114,115,116,117,118,-36,146,-75,-81,161,167,-7,]),'ASSIGN':([18,20,48,54,133,],[-73,27,-73,-74,-73,]),'INCREMENT':([18,20,48,54,133,],[-73,28,-73,-74,-73,]),'DECREMENT':([18,20,48,54,133,],[-73,29,-73,-74,-73,]),'L_KEY':([18,33,48,133,141,],[25,25,25,25,149,]),'R_PAR':([22,28,29,31,33,35,36,37,38,39,40,41,43,45,46,47,48,49,52,53,54,60,70,72,73,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,109,110,111,122,127,129,130,131,133,134,135,136,137,138,139,142,157,161,165,166,],[30,-34,-35,-10,-73,-59,-62,-66,-67,-68,-69,-70,-72,-32,-33,-49,-73,-52,71,-38,-74,80,-11,109,-37,-40,-60,-61,-63,-64,-65,-71,-50,-51,-53,-54,-55,-56,-57,-58,-36,-39,-38,-76,-12,-41,144,145,-73,147,-67,-70,-72,-80,148,-13,-14,-47,-48,168,]),'IF':([24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[-4,-4,-5,-6,-4,100,100,-25,-26,-27,-30,-4,-23,-24,-28,-29,-31,100,-82,-43,100,-45,-42,-44,-3,-46,]),'WHILE':([24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[-4,-4,-5,-6,-4,101,101,-25,-26,-27,-30,-4,-23,-24,-28,-29,-31,101,-82,-43,101,-45,-42,-44,-3,-46,]),'FOR':([24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[-4,-4,-5,-6,-4,102,102,-25,-26,-27,-30,-4,-23,-24,-28,-29,-31,102,-82,-43,102,-45,-42,-44,-3,-46,]),'PRINT':([24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[-4,-4,-5,-6,-4,103,103,-25,-26,-27,-30,-4,-23,-24,-28,-29,-31,103,-82,-43,103,-45,-42,-44,-3,-46,]),'READ':([24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[-4,-4,-5,-6,-4,104,104,-25,-26,-27,-30,-4,-23,-24,-28,-29,-31,104,-82,-43,104,-45,-42,-44,-3,-46,]),'COMMENT_LINE':([24,26,32,44,50,69,90,93,94,95,98,108,114,115,116,117,118,128,140,152,153,154,158,163,164,169,],[-4,-4,-5,-6,-4,105,105,-25,-26,-27,-30,-4,-23,-24,-28,-29,-31,105,-82,-43,105,-45,-42,-44,-3,-46,]),'NUMBER':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,111,119,120,122,146,149,],[37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,37,156,]),'ALPHANUMERIC':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,105,111,119,120,122,146,],[38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,38,124,38,38,38,135,38,]),'CHARACTER':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,111,119,120,122,146,],[39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,39,]),'BOOLEAN':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,111,119,120,122,146,],[40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,]),'TIMES':([33,36,37,38,39,40,41,43,46,48,54,80,109,135,136,137,],[-73,57,-66,-67,-68,-69,-70,-72,-72,-73,-74,-71,-36,-67,-70,-72,]),'DIVIDE':([33,36,37,38,39,40,41,43,46,48,54,80,109,135,136,137,],[-73,58,-66,-67,-68,-69,-70,-72,-72,-73,-74,-71,-36,-67,-70,-72,]),'MOD':([33,36,37,38,39,40,41,43,46,48,54,80,109,135,136,137,],[-73,59,-66,-67,-68,-69,-70,-72,-72,-73,-74,-71,-36,-67,-70,-72,]),'PLUS':([33,35,36,37,38,39,40,41,43,46,48,54,77,78,79,80,109,135,136,137,],[-73,55,-62,-66,-67,-68,-69,-70,-72,-72,-73,-74,-63,-64,-65,-71,-36,-67,-70,-72,]),'MINUS':([33,35,36,37,38,39,40,41,43,46,48,54,77,78,79,80,109,135,136,137,],[-73,56,-62,-66,-67,-68,-69,-70,-72,-72,-73,-74,-63,-64,-65,-71,-36,-67,-70,-72,]),'R_KEY':([33,34,35,36,37,38,39,40,41,43,54,75,76,77,78,79,80,109,156,],[-73,54,-59,-62,-66,-67,-68,-69,-70,-72,-74,-60,-61,-63,-64,-65,-71,-36,162,]),'MORE_THAN':([33,35,36,37,38,39,40,41,43,46,48,49,54,75,76,77,78,79,80,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,-73,63,-74,-60,-61,-63,-64,-65,-71,-36,-67,-70,-72,]),'LESS_THAN':([33,35,36,37,38,39,40,41,43,46,48,49,54,75,76,77,78,79,80,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,-73,64,-74,-60,-61,-63,-64,-65,-71,-36,-67,-70,-72,]),'MORE_EQUAL':([33,35,36,37,38,39,40,41,43,46,48,49,54,75,76,77,78,79,80,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,-73,65,-74,-60,-61,-63,-64,-65,-71,-36,-67,-70,-72,]),'LESS_EQUAL':([33,35,36,37,38,39,40,41,43,46,48,49,54,75,76,77,78,79,80,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,-73,66,-74,-60,-61,-63,-64,-65,-71,-36,-67,-70,-72,]),'EQUAL':([33,35,36,37,38,39,40,41,43,46,48,49,54,75,76,77,78,79,80,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,-73,67,-74,-60,-61,-63,-64,-65,-71,-36,-67,-70,-72,]),'NOT_EQUAL':([33,35,36,37,38,39,40,41,43,46,48,49,54,75,76,77,78,79,80,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,-73,68,-74,-60,-61,-63,-64,-65,-71,-36,-67,-70,-72,]),'AND':([33,35,36,37,38,39,40,41,43,46,47,48,49,54,75,76,77,78,79,80,83,84,85,86,87,88,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,61,-73,-52,-74,-60,-61,-63,-64,-65,-71,-53,-54,-55,-56,-57,-58,-36,-67,-70,-72,]),'OR':([33,35,36,37,38,39,40,41,43,46,47,48,49,54,75,76,77,78,79,80,83,84,85,86,87,88,109,135,136,137,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-72,62,-73,-52,-74,-60,-61,-63,-64,-65,-71,-53,-54,-55,-56,-57,-58,-36,-67,-70,-72,]),'COMMA':([33,35,36,37,38,39,40,41,43,47,49,54,70,74,75,76,77,78,79,80,81,82,83,84,85,86,87,88,109,142,],[-73,-59,-62,-66,-67,-68,-69,-70,-72,-49,-52,-74,107,111,-60,-61,-63,-64,-65,-71,-50,-51,-53,-54,-55,-56,-57,-58,-36,150,]),'END_LINE':([124,],[140,]),'ELSE':([152,164,],[159,-3,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'program':([0,],[1,]),'variables':([4,24,26,50,108,],[5,32,44,69,128,]),'functions':([5,],[7,]),'type':([6,8,31,106,107,150,],[9,17,51,125,126,126,]),'mainBody':([7,],[15,]),'assignment':([9,69,90,121,128,153,161,],[19,91,91,132,91,91,165,]),'idCall':([9,25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,69,90,111,119,120,121,122,123,128,146,153,161,],[20,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,41,20,20,41,41,41,20,136,139,20,41,20,20,]),'exp':([25,27,42,53,55,56,61,62,63,64,65,66,67,68,111,119,120,122,146,],[34,49,49,49,75,76,49,49,83,84,85,86,87,88,49,49,49,49,49,]),'term':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,111,119,120,122,146,],[35,35,35,35,35,35,77,78,79,35,35,35,35,35,35,35,35,35,35,35,35,35,]),'factor':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,111,119,120,122,146,],[36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,36,]),'functionCall':([25,27,42,53,55,56,57,58,59,61,62,63,64,65,66,67,68,69,90,111,119,120,122,128,146,153,],[43,46,43,43,43,43,43,43,43,43,43,43,43,43,43,43,43,92,92,43,43,43,137,92,43,92,]),'megaExp':([27,42,53,111,119,120,122,146,],[45,60,74,74,130,131,138,155,]),'superExp':([27,42,53,61,62,111,119,120,122,146,],[47,47,47,81,82,47,47,47,47,47,]),'functionsHelp':([31,],[52,]),'functionCallParams':([53,],[72,]),'functionCallParamsOptional':([53,111,],[73,129,]),'statements':([69,90,128,153,],[89,113,143,160,]),'statement':([69,90,128,153,],[90,90,90,90,]),'ifBlock':([69,90,128,153,],[93,93,93,93,]),'whileBlock':([69,90,128,153,],[94,94,94,94,]),'forBlock':([69,90,128,153,],[95,95,95,95,]),'print':([69,90,128,153,],[96,96,96,96,]),'read':([69,90,128,153,],[97,97,97,97,]),'lineComment':([69,90,128,153,],[98,98,98,98,]),'arrays':([69,90,128,153,],[99,99,99,99,]),'functionCallParamsMultiple':([74,],[110,]),'functionsHelp2':([107,150,],[127,157,]),'print_help':([122,],[134,]),'body':([144,145,159,168,],[152,154,163,169,]),'optionalElse':([152,],[158,]),'optionalAssign':([161,],[166,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> program","S'",1,None,None,None),
  ('program -> PROGRAM ID L_BRACK variables functions mainBody R_BRACK','program',7,'p_program','parser.py',14),
  ('mainBody -> MAIN L_PAR R_PAR L_BRACK variables statements R_BRACK','mainBody',7,'p_mainBody','parser.py',19),
  ('body -> L_BRACK statements R_BRACK','body',3,'p_body','parser.py',24),
  ('variables -> <empty>','variables',0,'p_variables','parser.py',29),
  ('variables -> VAR type ID DOT_COMMA variables','variables',5,'p_variables','parser.py',30),
  ('variables -> VAR type assignment DOT_COMMA variables','variables',5,'p_variables','parser.py',31),
  ('arrays -> VAR type ID L_KEY NUMBER R_KEY DOT_COMMA','arrays',7,'p_arrays','parser.py',38),
  ('functions -> <empty>','functions',0,'p_functions','parser.py',43),
  ('functions -> FUNCTION type ID L_PAR functionsHelp R_PAR L_BRACK variables statements R_BRACK','functions',10,'p_functions','parser.py',44),
  ('functionsHelp -> <empty>','functionsHelp',0,'p_functionsHelp','parser.py',49),
  ('functionsHelp -> type ID','functionsHelp',2,'p_functionsHelp','parser.py',50),
  ('functionsHelp -> type ID COMMA functionsHelp2','functionsHelp',4,'p_functionsHelp','parser.py',51),
  ('functionsHelp2 -> type ID','functionsHelp2',2,'p_functionsHelp2','parser.py',58),
  ('functionsHelp2 -> type ID COMMA functionsHelp2','functionsHelp2',4,'p_functionsHelp2','parser.py',59),
  ('type -> INT','type',1,'p_type','parser.py',69),
  ('type -> DECIM','type',1,'p_type','parser.py',70),
  ('type -> BOOL','type',1,'p_type','parser.py',71),
  ('type -> CHAR','type',1,'p_type','parser.py',72),
  ('type -> STRING','type',1,'p_type','parser.py',73),
  ('statements -> <empty>','statements',0,'p_statements','parser.py',80),
  ('statements -> statement statements','statements',2,'p_statements','parser.py',81),
  ('statement -> <empty>','statement',0,'p_statement','parser.py',89),
  ('statement -> assignment DOT_COMMA','statement',2,'p_statement','parser.py',90),
  ('statement -> functionCall DOT_COMMA','statement',2,'p_statement','parser.py',91),
  ('statement -> ifBlock','statement',1,'p_statement','parser.py',92),
  ('statement -> whileBlock','statement',1,'p_statement','parser.py',93),
  ('statement -> forBlock','statement',1,'p_statement','parser.py',94),
  ('statement -> print DOT_COMMA','statement',2,'p_statement','parser.py',95),
  ('statement -> read DOT_COMMA','statement',2,'p_statement','parser.py',96),
  ('statement -> lineComment','statement',1,'p_statement','parser.py',97),
  ('statement -> arrays DOT_COMMA','statement',2,'p_statement','parser.py',98),
  ('assignment -> idCall ASSIGN megaExp','assignment',3,'p_assignment','parser.py',103),
  ('assignment -> idCall ASSIGN functionCall','assignment',3,'p_assignment','parser.py',104),
  ('assignment -> idCall INCREMENT','assignment',2,'p_assignment','parser.py',105),
  ('assignment -> idCall DECREMENT','assignment',2,'p_assignment','parser.py',106),
  ('functionCall -> ID L_PAR functionCallParams R_PAR','functionCall',4,'p_functionCall','parser.py',114),
  ('functionCallParams -> functionCallParamsOptional','functionCallParams',1,'p_functionCallParams','parser.py',118),
  ('functionCallParamsOptional -> <empty>','functionCallParamsOptional',0,'p_functionCallParamsOptional','parser.py',122),
  ('functionCallParamsOptional -> megaExp functionCallParamsMultiple','functionCallParamsOptional',2,'p_functionCallParamsOptional','parser.py',123),
  ('functionCallParamsMultiple -> <empty>','functionCallParamsMultiple',0,'p_functionCallParamsMultiple','parser.py',130),
  ('functionCallParamsMultiple -> COMMA functionCallParamsOptional','functionCallParamsMultiple',2,'p_functionCallParamsMultiple','parser.py',131),
  ('ifBlock -> IF L_PAR megaExp R_PAR body optionalElse','ifBlock',6,'p_ifBlock','parser.py',142),
  ('optionalElse -> <empty>','optionalElse',0,'p_optionalElse','parser.py',149),
  ('optionalElse -> ELSE body','optionalElse',2,'p_optionalElse','parser.py',150),
  ('whileBlock -> WHILE L_PAR megaExp R_PAR body','whileBlock',5,'p_whileBlock','parser.py',155),
  ('forBlock -> FOR L_PAR assignment DOT_COMMA megaExp DOT_COMMA optionalAssign R_PAR body','forBlock',9,'p_forBlock','parser.py',159),
  ('optionalAssign -> <empty>','optionalAssign',0,'p_optionalAssign','parser.py',166),
  ('optionalAssign -> assignment','optionalAssign',1,'p_optionalAssign','parser.py',167),
  ('megaExp -> superExp','megaExp',1,'p_megaExp','parser.py',174),
  ('megaExp -> superExp AND superExp','megaExp',3,'p_megaExp','parser.py',175),
  ('megaExp -> superExp OR superExp','megaExp',3,'p_megaExp','parser.py',176),
  ('superExp -> exp','superExp',1,'p_superExp','parser.py',183),
  ('superExp -> exp MORE_THAN exp','superExp',3,'p_superExp','parser.py',184),
  ('superExp -> exp LESS_THAN exp','superExp',3,'p_superExp','parser.py',185),
  ('superExp -> exp MORE_EQUAL exp','superExp',3,'p_superExp','parser.py',186),
  ('superExp -> exp LESS_EQUAL exp','superExp',3,'p_superExp','parser.py',187),
  ('superExp -> exp EQUAL exp','superExp',3,'p_superExp','parser.py',188),
  ('superExp -> exp NOT_EQUAL exp','superExp',3,'p_superExp','parser.py',189),
  ('exp -> term','exp',1,'p_exp','parser.py',196),
  ('exp -> term PLUS exp','exp',3,'p_exp','parser.py',197),
  ('exp -> term MINUS exp','exp',3,'p_exp','parser.py',198),
  ('term -> factor','term',1,'p_term','parser.py',205),
  ('term -> factor TIMES term','term',3,'p_term','parser.py',206),
  ('term -> factor DIVIDE term','term',3,'p_term','parser.py',207),
  ('term -> factor MOD term','term',3,'p_term','parser.py',208),
  ('factor -> NUMBER','factor',1,'p_factor','parser.py',215),
  ('factor -> ALPHANUMERIC','factor',1,'p_factor','parser.py',216),
  ('factor -> CHARACTER','factor',1,'p_factor','parser.py',217),
  ('factor -> BOOLEAN','factor',1,'p_factor','parser.py',218),
  ('factor -> idCall','factor',1,'p_factor','parser.py',219),
  ('factor -> L_PAR megaExp R_PAR','factor',3,'p_factor','parser.py',220),
  ('factor -> functionCall','factor',1,'p_factor','parser.py',221),
  ('idCall -> ID','idCall',1,'p_idCall','parser.py',230),
  ('idCall -> ID L_KEY exp R_KEY','idCall',4,'p_idCall','parser.py',231),
  ('print -> PRINT L_PAR print_help R_PAR','print',4,'p_print','parser.py',241),
  ('print_help -> <empty>','print_help',0,'p_print_help','parser.py',248),
  ('print_help -> ALPHANUMERIC','print_help',1,'p_print_help','parser.py',249),
  ('print_help -> idCall','print_help',1,'p_print_help','parser.py',250),
  ('print_help -> functionCall','print_help',1,'p_print_help','parser.py',251),
  ('print_help -> megaExp','print_help',1,'p_print_help','parser.py',252),
  ('read -> READ L_PAR idCall R_PAR','read',4,'p_read','parser.py',256),
  ('lineComment -> COMMENT_LINE ALPHANUMERIC END_LINE','lineComment',3,'p_lineComment','parser.py',263),
]
