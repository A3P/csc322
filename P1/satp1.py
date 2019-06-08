#!/usr/bin/env python
#-------------------------------------------------------------------------------
# satp1.py
# Course: CSC 322
# Project 1
#
# Group Members:
# Yves Belliveau
# Lance Lansing
# Ryan Afshar
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
varNumList = []

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
    return token

# Returns the latest scanned token.
def getToken():
    return token

def ASTtoCNF(root):
    global oddNum
    global maxVar
    global varNumList
    if root is None:
        return

    if root.left is not None:
        ASTtoCNF(root.left)

    if(root.left is None):
        root.treeNum = int(root.data[1:]) * 2
        #add variable number to varNumList for task 2
        if root.treeNum not in varNumList:
          varNumList.append(root.treeNum)
    else:
        root.treeNum = oddNum
        oddNum += 2
    
    if root.treeNum > maxVar:
      maxVar = root.treeNum

    if root.right is not None:
        ASTtoCNF(root.right)
    
    if root.left is not None:
        getCNFLine(root)

    
#format a CNF line for minisat input based on node numbers and operator
#adds CNF lines to minisatInput variable
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
    
    #set vcheckNum to 2 if 2 is passed (default vcheckNum 1)
    #and 3rd argument as boolean expression if available
    vcheckNum = 1
    if len(sys.argv) >= 3:
      expr = sys.argv[2]
      if sys.argv[1] == '2':
        vcheckNum = 2
    else:
      expr = "(~A9->A31)&(A13vA44)"
      print("Using example expression: {}".format(expr))

    scan = pattern.scanner(expr)

    createAST()

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
    f.close()
    valid = re.search("UNSAT", out)
    result = "\n" + expr

    if valid:
      print result + " is VALID"
    else:
      print result + " is INVALID"

      #segment for vcheck2
      if vcheckNum == 2:
        vcheck2output = ""
        numList = out.split()
        #split out into its numbers
        #get the value at each index equal to variable numbers and
        #append to output string with appropriate truth value
        for varNum in varNumList:
          current = int(numList[varNum])
          truthValue = ""
          if current < 0:
            truthValue = "F"
          elif current > 0:
            truthValue = "T"
          vcheck2output = vcheck2output + "A{} = {} ".format(varNum/2, truthValue)
        print(vcheck2output)
