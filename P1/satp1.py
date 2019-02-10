import re

class Node(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None
        self.treeNum = 0

token = ""
root = Node("")
oddNum = 1

def sent():
    global root
    disj()
    token = getToken()
    if (token is not None and token.lastindex == 4):
        i = Node(token.group(token.lastindex))
        i.left = root
        sent()
        i.right = root
        root = i

def disj():
    global root
    conj()
    token = getToken()
    while(token is not None and token.lastindex == 3):
        d = Node(token.group(token.lastindex))
        d.left = root
        conj()
        d.right = root
        root = d
        token = getToken()

def conj():
    global root
    lit()
    token = getToken()
    while(token is not None and token.lastindex == 2):
        c = Node(token.group(token.lastindex))
        c.left = root
        lit()
        c.right = root
        root = c
        token = getToken()

def lit():
    global root
    atom()
    token = getToken()
    if(token is not None and token.lastindex == 1):
        n = Node(token.group(token.lastindex))
        atom()
        n.left = root
        root = n

def atom():
    global root
    token = scanToken()
    if(token is not None and token.lastindex == 7):
        root = Node(token.group(token.lastindex))
        token = scanToken()
        print (token)
    elif (token is not None and token.lastindex == 5):
        sent()
        scanToken()


def scanToken():
    global token
    token = scan.match()
    if(token):
        print (token.lastindex), repr(token.group(token.lastindex))
    return token

def getToken():
    return token

def inOrder(root):
    global oddNum
    if root is None:
        return

    if root.left is not None:
        inOrder(root.left)

    if(root.left is None):
        root.treeNum = int(root.data[1:]) * 2
    else:
        root.treeNum = oddNum
        oddNum += 2
    print(root.data, root.treeNum)

    if root.right is not None:
        inOrder(root.right)

pattern = re.compile("(?:"
"(~)"
"|(\&)"
"|(v)"
"|(->)"
"|(\()"
"|(\))"
"|(A\d+))")

expr = "(A1->(A3->A2))&(A4vA5)"

scan = pattern.scanner(expr)

sent()

# print(root)
# print(root.left)
# print(root.right)

inOrder(root)

# while 1:
#     m = scan.match()
#     if not m:
#         break
#     print m.lastindex, m.group(m.lastindex)

# t = Node("v")
# print "My Node: ", t.data,
