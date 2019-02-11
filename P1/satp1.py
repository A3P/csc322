#!/usr/bin/env python
#-------------------------------------------------------------------------------
# satp1.py
# Course: CSC 322
# Project 1
#
# Group Members:
# Yves Belliveau (V00815315)
# Lance Lansing (V00819401)
# Ryan Afshar (V00864456)
#
#-------------------------------------------------------------------------------
import re
import sys
import subprocess

#Node class for AST - data is string of operator, tClass is 
class Node(object):
    def __init__(self, data, tClass):
        self.data = data
        self.tClass = tClass
        self.left = None
        self.right = None
        self.treeNum = 0


#GLOBAL VARIABLES--------------------------------------------------
token = ""
root = Node("", 0)
oddNum = 1
minisatInput = ""
maxVar = 0
numClauses = 0 

#Token Class numbers
NEGOP = 1
ANDOP = 2
OROP = 3
IMPOP = 4
LPAREN = 5
RPAREN = 6
VARSYMB = 7


#------------------------------------------------------------------

#FUNCTIONS---------------------------------------------------------

#Wrapper function for starting the recursive descent parser
def createAST():
  sent()

#Recursive Descent Parser Functions++++++++++++++++++++++++++++
#implements "SENT ::= DISJ | DISJ IMPOP SENT"
def sent():
    global root
    disj()
    token = getToken()
    if (token is not None and token.lastindex == IMPOP):
        i = Node(token.group(token.lastindex), token.lastindex)
        i.left = root
        sent()
        i.right = root
        root = i

#implements "DISJ ::= CONJ{OROP CONJ>"
def disj():
    global root
    conj()
    token = getToken()
    while(token is not None and token.lastindex == OROP):
        d = Node(token.group(token.lastindex), token.lastindex)
        d.left = root
        conj()
        d.right = root
        root = d
        token = getToken()

#implements "CONJ ::= LIT{ANDOP LIT}"
def conj():
    global root
    lit()
    token = getToken()
    while(token is not None and token.lastindex == ANDOP):
        c = Node(token.group(token.lastindex), token.lastindex)
        c.left = root
        lit()
        c.right = root
        root = c
        token = getToken()

#implements "LIT ::= ATOM | NEGOP ATOM"
def lit():
    global root
    atom()
    token = getToken()
    if(token is not None and token.lastindex == NEGOP):
        n = Node(token.group(token.lastindex), token.lastindex)
        atom()
        n.left = root
        root = n

#implements "ATOM ::= VAR | LPAREN SENT RPAREN"
def atom():
    global root
    token = scanToken()
    if(token is not None and token.lastindex == VARSYMB):
        root = Node(token.group(token.lastindex), token.lastindex)
        token = scanToken()
        # print (token)
    elif (token is not None and token.lastindex == LPAREN):
        sent()
        scanToken()
#+++++++++++++++++++++++++++++++++++++++++++++++++++++++++

# Scans the next token within the input.
def scanToken():
    global token
    token = scan.match()
    # if(token):
    #     printprint (token.lastindex), repr(token.group(token.lastindex))
    return token

# Returns the latest scanned token.
def getToken():
    return token

def ASTtoCNF(root):
    global oddNum
    global maxVar
    if root is None:
        return

    if root.left is not None:
        ASTtoCNF(root.left)

    if(root.left is None):
        root.treeNum = int(root.data[1:]) * 2
    else:
        root.treeNum = oddNum
        oddNum += 2
    
    if root.treeNum > maxVar:
      maxVar = root.treeNum

    #print(root.data, root.treeNum, root.tClass)

    if root.right is not None:
        ASTtoCNF(root.right)
    
    if root.left is not None:
        getCNFLine(root)

    
#format a CNF line for minisat input based on node numbers and operator
def getCNFLine(root):
    global minisatInput
    global numClauses
    t = root.tClass
    line = ""

    if t == NEGOP: #not operator
      line = line + "{} {} 0\n".format(-root.left.treeNum, -root.treeNum)
      line = line + "{} {} 0\n".format(root.left.treeNum, root.treeNum)
      numClauses += 2
    elif t == ANDOP: #and operator
      line = line + "{} {} {} 0\n".format(-root.left.treeNum, -root.right.treeNum, root.treeNum)
      line = line + "{} {} {} 0\n".format(-root.left.treeNum, root.right.treeNum, -root.treeNum)
      line = line + "{} {} {} 0\n".format(root.left.treeNum, -root.right.treeNum, -root.treeNum)
      line = line + "{} {} {} 0\n".format(root.left.treeNum, root.right.treeNum, -root.treeNum)
      numClauses += 4
    elif t == OROP: #or operator
      line = line + "{} {} {} 0\n".format(-root.left.treeNum, -root.right.treeNum, root.treeNum)
      line = line + "{} {} {} 0\n".format(-root.left.treeNum, root.right.treeNum, root.treeNum)
      line = line + "{} {} {} 0\n".format(root.left.treeNum, -root.right.treeNum, root.treeNum)
      line = line + "{} {} {} 0\n".format(root.left.treeNum, root.right.treeNum, -root.treeNum)
      numClauses += 4
    elif t == IMPOP: #implication operator
      line = line + "{} {} {} 0\n".format(-root.left.treeNum, -root.right.treeNum, root.treeNum)
      line = line + "{} {} {} 0\n".format(-root.left.treeNum, root.right.treeNum, -root.treeNum)
      line = line + "{} {} {} 0\n".format(root.left.treeNum, -root.right.treeNum, root.treeNum)
      line = line + "{} {} {} 0\n".format(root.left.treeNum, root.right.treeNum, root.treeNum)
      numClauses += 4
    minisatInput = minisatInput + line


#MAIN-----------------------------------------------------------------
if __name__ == '__main__':

    #regex pattern for parsing
    pattern = re.compile("(?:"
    "(~)"
    "|(\&)"
    "|(v)"
    "|(->)"
    "|(\()"
    "|(\))"
    "|(A\d+))")

    #take first argument as boolean expression if available
    if len(sys.argv) >= 2:
      expr = sys.argv[1]
    else:
      expr = "(~A9->A31)&(A13vA44)"

    scan = pattern.scanner(expr)

    createAST()

    # print(root)
    # print(root.left)
    # print(root.right)

    ASTtoCNF(root)
    minisatInput = minisatInput + "{} 0\n".format(-root.treeNum) 
    numClauses += 1
    minisatInput = "p cnf {} {}\n".format(maxVar, numClauses) + minisatInput

    # Write minisat input to a file and start a subprocess for minisat.
    f = open("in", "w+")
    f.write(minisatInput)
    f.close()
    subprocess.call(["minisat", "./in", "./out"])
    
    # Reads output and determine if the expression is valid
    f = open("out", "r")
    out = f.read()
    valid = re.search("UNSAT", out)
    result = "\n" + expr
    if valid:
        print result + " is VALID"
    else:
        print result + " is INVALID"



    # while 1:
    #     m = scan.match()
    #     if not m:
    #         break
    #     print m.lastindex, m.group(m.lastindex)

    # t = Node("v")
    # print "My Node: ", t.data,
