#! /usr/bin/env python3
# Charlie Conneely
# G00348887

def shunt(infix):
    # Convert input to a stack like list 
    infix = list(infix)[::-1]

    # Operator stack
    opers = []

    # Output list
    postfix = []

    # Operator precedence
    prec = {'*': 100, '?': 90, '.': 80, '|': 60, ')': 40, '(': 20}

    # Loop through the input one character at a time
    while infix:
        # pop a character from the input 
        c = infix.pop()

        # Decide precedence
        if c == '(':
            opers.append(c)
        elif c == ')':
            # pop the opers stack until you find the )
            while opers[-1] != '(':
                postfix.append(opers.pop())
            # Get rid of the '('
            opers.pop()
        elif c in prec:
            # push any ops on the opers stack with higher prec to the output
            while opers and prec[c] < prec[opers[-1]]:
                postfix.append(opers.pop())
            # Push c to the opers stack
            opers.append(c)
        else:
            postfix.append(c)

    # Pop all operators to the output
    while opers:
        postfix.append(opers.pop())

    # convert output list to string
    postfix = ''.join(postfix)
    return postfix



# ========================
# Thompsons's Classes 18/02
# ========================

class State:
    edges = []
    # label for arrows - None = epsilon
    label = None

    # Constructor
    def __init__(self, label=None, edges=[]):
        self.label = label
        self.edges = edges


class Fragment:
    # Start state of NFA fragment
    start = None
    # Accept state of NFA fragment
    accept = None

    # Constructor
    def __init__(self, start, accept):
        self.start = start
        self.accept = accept

# =================
# Thompson's Classes
# =================



def regex_compile(infix):
    postfix = shunt(infix)
    postfix = list(postfix)[::-1]

    nfa_stack = []

    while postfix:
        # Pop a character from postfix 
        c = postfix.pop()
        if c == '.':
            # append
            # pop 2 fragments off the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()
            # point frag2's accept state at frag1's start state
            frag2.accept.edges.append(frag1.start)
            
            # Create new instance of Fragment to represent the new NFA 
            newFrag = Fragment(frag2.start, frag1.accept)
            # Push the new NFA to the NFA stack 
        elif c == '|':
            # or
            # Pop 2 fragments off the stack
            frag1 = nfa_stack.pop()
            frag2 = nfa_stack.pop()

            # Create new start and accept states 
            accept = State()
            start = State(edges = [frag2.start, frag1.start])
            # Point the old accept states at the new one
            frag2.accept.edges.append(accept)
            frag1.accept.edges.append(accept)
            newFrag = Fragment(start, accept)
        elif c == '*':
            # Pop a single fragment off the stack 
            frag = nfa_stack.pop()
            # create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])
            # point the arrows
            frag.accept.edges = [frag.start, accept]
            # Create new instance of fragment
            newFrag = Fragment(start, accept)
        elif c == '?':
            # Zero or one 
            frag = nfa_stack.pop()
            # create new start and accept states
            accept = State()
            start = State(edges=[frag.start, accept])
            frag.accept.edges = [accept]
            # untested
            newFrag = Fragment(start, accept)
        else:
            accept = State()
            start = State(label=c, edges=[accept])
            newFrag = Fragment(start, accept)

        # Push the new NFA to the stack 
        nfa_stack.append(newFrag)

    # NFA should contain just one NFA 
    return nfa_stack.pop()

def loopForEpsilons(state, current):
    # check if state hasn't already been looped through
    if state not in current:
        current.add(state)
        if state.label is None:
            for moreEdges in state.edges:
                loopForEpsilons(moreEdges, current)


def loopForMatches(prev, current, c):
    for state in prev:
        if state.label is not None:
            if state.label == c:
                loopForEpsilons(state.edges[0], current)


def compareStringToNFA(nfa, s):

    result = False
    # create list of chars from string
    text = list(s)[::-1]
    current = set()
    prev = set()
    allStates = set()
 
    # run through epsilons and add all states to set 
    loopForEpsilons(nfa.start, current)  
    
    # run through char list
    while text:
        prev = current
        current = set()
        # pop one off the top
        c = text.pop()

        # search from beginning for matching labels
        loopForMatches(prev, current, c)


    if nfa.accept in current:
        result = True

    return result            





def match(regex, s):
    # returns true if regex matches the text
    # returns false otherwise

    # compile regex into NFA
    nfa = regex_compile(regex)
    # check if nfa matches string s 
    # function to run the text through the nfa
    result = compareStringToNFA(nfa, s)
    return result

inputString = input("Enter your string: ")
inputRegex = input("Enter your regular expression: ")

result = match(inputRegex, inputString)

print("Regex: ", inputRegex)
print("String: ", inputString)
print("Result is: ", str(result))
