
# parsetab.py
# This file is automatically generated. Do not edit.
# pylint: disable=W,C,R
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'leftANDleftORleftPLUSMINUSleftMULDIVIDEAND DIVIDE EQ ID LE LPAREN LT MINUS MUL NUM OR PLUS RPAREN SE STexpr : expr AND exprexpr : expr OR exprexpr : term LE termexpr : term LT termexpr : term SE termexpr : term ST termexpr : term EQ termterm : term PLUS termterm : term MINUS termterm : term MUL termterm : term DIVIDE term\n    expr : LPAREN expr RPAREN\n    term : LPAREN term RPAREN\n    term : NUMterm : ID'
    
_lr_action_items = {'LPAREN':([0,3,6,7,8,9,10,11,12,13,14,15,16,22,],[3,3,3,3,22,22,22,22,22,22,22,22,22,22,]),'NUM':([0,3,6,7,8,9,10,11,12,13,14,15,16,22,],[4,4,4,4,4,4,4,4,4,4,4,4,4,4,]),'ID':([0,3,6,7,8,9,10,11,12,13,14,15,16,22,],[5,5,5,5,5,5,5,5,5,5,5,5,5,5,]),'$end':([1,4,5,19,20,21,23,24,25,26,27,28,29,30,31,32,],[0,-14,-15,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,]),'AND':([1,4,5,17,19,20,21,23,24,25,26,27,28,29,30,31,32,],[6,-14,-15,6,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,]),'OR':([1,4,5,17,19,20,21,23,24,25,26,27,28,29,30,31,32,],[7,-14,-15,7,7,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,]),'LE':([2,4,5,18,27,28,29,30,32,],[8,-14,-15,8,-8,-9,-10,-11,-13,]),'LT':([2,4,5,18,27,28,29,30,32,],[9,-14,-15,9,-8,-9,-10,-11,-13,]),'SE':([2,4,5,18,27,28,29,30,32,],[10,-14,-15,10,-8,-9,-10,-11,-13,]),'ST':([2,4,5,18,27,28,29,30,32,],[11,-14,-15,11,-8,-9,-10,-11,-13,]),'EQ':([2,4,5,18,27,28,29,30,32,],[12,-14,-15,12,-8,-9,-10,-11,-13,]),'PLUS':([2,4,5,18,21,23,24,25,26,27,28,29,30,32,33,],[13,-14,-15,13,13,13,13,13,13,-8,-9,-10,-11,-13,13,]),'MINUS':([2,4,5,18,21,23,24,25,26,27,28,29,30,32,33,],[14,-14,-15,14,14,14,14,14,14,-8,-9,-10,-11,-13,14,]),'MUL':([2,4,5,18,21,23,24,25,26,27,28,29,30,32,33,],[15,-14,-15,15,15,15,15,15,15,15,15,-10,-11,-13,15,]),'DIVIDE':([2,4,5,18,21,23,24,25,26,27,28,29,30,32,33,],[16,-14,-15,16,16,16,16,16,16,16,16,-10,-11,-13,16,]),'RPAREN':([4,5,17,18,19,20,21,23,24,25,26,27,28,29,30,31,32,33,],[-14,-15,31,32,-1,-2,-3,-4,-5,-6,-7,-8,-9,-10,-11,-12,-13,32,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'expr':([0,3,6,7,],[1,17,19,20,]),'term':([0,3,6,7,8,9,10,11,12,13,14,15,16,22,],[2,18,2,2,21,23,24,25,26,27,28,29,30,33,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> expr","S'",1,None,None,None),
  ('expr -> expr AND expr','expr',3,'p_expression_and','parser.py',14),
  ('expr -> expr OR expr','expr',3,'p_expression_or','parser.py',20),
  ('expr -> term LE term','expr',3,'p_expression_le','parser.py',26),
  ('expr -> term LT term','expr',3,'p_expression_lt','parser.py',32),
  ('expr -> term SE term','expr',3,'p_expression_se','parser.py',38),
  ('expr -> term ST term','expr',3,'p_expression_st','parser.py',44),
  ('expr -> term EQ term','expr',3,'p_expression_eq','parser.py',50),
  ('term -> term PLUS term','term',3,'p_term_plus','parser.py',57),
  ('term -> term MINUS term','term',3,'p_term_minus','parser.py',63),
  ('term -> term MUL term','term',3,'p_term_mul','parser.py',69),
  ('term -> term DIVIDE term','term',3,'p_term_div','parser.py',75),
  ('expr -> LPAREN expr RPAREN','expr',3,'p_paren','parser.py',83),
  ('term -> LPAREN term RPAREN','term',3,'p_paren','parser.py',84),
  ('term -> NUM','term',1,'p_term_num','parser.py',91),
  ('term -> ID','term',1,'p_term_id','parser.py',97),
]
