import re

class Node(object):
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

token = ""
root = Node("")

def sent():
    disj()

def disj():
    global root
    conj()
    token = getToken()
    while(token is not None and token.lastindex == 3):
        d = Node("v")
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
        d = Node("&")
        d.left = root
        conj()
        d.right = root
        root = d
        token = getToken()

def lit():
    global root
    atom()
    t = getToken()
    if(t is not None and t.lastindex == 1):
        n = Node("~")
        atom()
        n.left = root
        root = n

def atom():
    global root
    t = scanToken()
    if(t is not None and t.lastindex == 7):
        root = Node(t.group(t.lastindex))
        t = scanToken()
        print (t)
    elif (t is not None and t.lastindex == 5):
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
    #print ("traversal: " ,root)
    if root is None:
        return

    if root.left is not None:
        inOrder(root.left)

    print(root.data)

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

expr = "(A1v~A2)&A3"

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
