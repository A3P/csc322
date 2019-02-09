#-------------------------------------------------------------------------------
# CSC322A1P1.py
# Course: CSC 322
# Assignment 1 Task 1
#
# Group Members:
# Yves Belliveau (V00815315)
#
#
#
# Tokenizer implemented with help from code located at https://gist.github.com/eliben/5797351
#-------------------------------------------------------------------------------
import re
import sys

class Tree(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

class Token(object):
    def __init__(self, type, val, pos):
        self.type = type
        self.val = val
        self.pos = pos

    def __str__(self):
        return '%s(%s) at %s' % (self.type, self.val, self.pos)

class LexerError(Exception):
    def __init__(self, pos):
        self.pos = pos


class Lexer(object):
    def __init__(self, rules):
        idx = 1
        regex_parts = []
        self.group_type = {}

        for regex, type in rules:
            groupname = 'GROUP%s' % idx
            regex_parts.append('(?P<%s>%s)' % (groupname, regex))
            self.group_type[groupname] = type
            idx += 1

        self.regex = re.compile('|'.join(regex_parts))
        self.re_ws_skip = re.compile('\S')

    def input(self, buf):
        self.buf = buf
        self.pos = 0

    def token(self):
        if self.pos >= len(self.buf):
            return None
        else:
            m = self.re_ws_skip.search(self.buf, self.pos)

            if m:
                self.pos = m.start()
            else:
                return None

            m = self.regex.match(self.buf, self.pos)
            if m:
                groupname = m.lastgroup
                tok_type = self.group_type[groupname]
                tok = Token(tok_type, m.group(groupname), self.pos)
                self.pos = m.end()
                return tok

            # if we're here, no rule matched
            raise LexerError(self.pos)

    def tokens(self):
        while 1:
            tok = self.token()
            if tok is None: break
            yield tok

def sent(formula, i, root):
    temp = formula[i]
    if temp[0] == 'VAR':
        temp2 = formula[i+1]
        if temp2[0] == 'IMPOP':
            i = i+2
            sent(formula, i, root)
        else:
            disj(formula, i, root)

def disj(formula, i, root):
    temp = formula[i]
    if temp[0] == 'VAR':
        conj(formula, i, root)
    elif temp[0] == 'OROP':
        while temp[0] == 'OROP':
            i = i+1
            conj(formula, i, root)

def conj(formula, i, root):
    temp = formula[i]
    if temp[0] == 'VAR':
        lit(formula, i, root)
    elif temp[0] == 'ANDOP':
        while temp[0] == 'ANDOP':
            i = i+1
            lit(formula, i, root)

def lit(formula, i, root):
    temp = formula[i]
    if temp[0] == 'VAR':
        atom(formula, i, root)
    elif temp[0] == 'NEGOP':
        i = i+1
        atom(formula, i, root)

def atom(formula, i, root):
    temp = formula[i]
    if temp[0] == 'VAR':
        root = temp[1]
    elif temp[0] == 'LPAREN':
        i = i+1
        sent(formula, i, root)


def inOrder(root):
    if root is None:
        return

    if root.left is not None:
        inOrder(root.left)

    print(root.data, 'one print')

    if root.right is not None:
        inOrder(root.right)

if __name__ == '__main__':
    rules = [
        ('\~',             'NEGOP'),
        ('\&',             'ANDOP'),
        ('v',              'OROP'),
        ('\-\>',           'IMPOP'),
        ('\(',             'LPAREN'),
        ('\)',             'RPAREN'),
        ('A[1-9][0-9]*',   'VAR'),
    ]

    lx = Lexer(rules)
    lx.input('(A1 v A2) -> (A1 & A3)')

    formula = []
    root = Tree('')

    for tok in lx.tokens():
        token = [tok.type,tok.val]
        formula.append(token)

    sent(formula, 0, root)
