# Project 1 - CSC322 - Feb 2019
## Yves Belliveau - Lance Lansing - Amir Afshar

### vcheck1
vcheck1 is used by typing "./vcheck1" in the folder containing the executable and then entering a valid input into stdin.
    eg. A1v((A2->A1)&(A31->A2))
Output will be the minisat output, followed by the expression and whether it is invalid or valid.

### vcheck2
vcheck2 is used by typing "./vcheck2" in the folder containing the executable and then entering a valid input into stdin .
    eg. A1v((A2->A1)&(A31->A2))
Output will be the minisat output, followed by the expression and whether it is invalid or valid, followed by an assignment of truth values to variables that gives the expression a truth value of false.

### satp1.py
This python file is used by both vcheck1 and vcheck 2 and performs the work of both task 1 and 2 (and it accounts for the general case, only outputting the truth values of real variables inputted, regardless of contiguity).
It parses input into tokens, then uses recursive descent parser to create the AST (making nodes). ASTtoCNF then assigns numbers to nodes and creates clauses for input into minisat. The output is printed into a file "in". Then minisat is called and given "in" as input and minisats output is put into "out" file. 
If vcheck 2 was called it then the truth values are taken from the minisat output and a line of output is created.

### Notes
    - Task 1 and 2 are implemented with satp1.py and vcheck1 and 2 shell scripts
    - Task 3 and 4 were not completed