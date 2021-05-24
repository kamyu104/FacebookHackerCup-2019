# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Qualification Round - Mr. X
# https://www.facebook.com/hackercup/problem/589264531559040/
#
# Time:  O(E)
# Space: O(D), D is the depth of expression
#

def calc(operator, x, y):
    if operator == '&':
        return x & y
    elif operator == '|':
        return x | y
    return x ^ y

def evaluate(s, lookup):
    operands, operators = [], []
    for i in xrange(len(s)):
        if s[i] in lookup:
            operands.append(lookup[s[i]])
        elif s[i] == ')':
            right, left = operands.pop(), operands.pop()
            operands.append(calc(operators.pop(), left, right))
        elif s[i] != '(':
            operators.append(s[i])
    return operands[-1]

def mr_x():
    E = raw_input()
    return evaluate(E, {'0':0, '1':1, 'x':0 ,'X':1}) ^ \
           evaluate(E, {'0':0, '1':1, 'x':1 ,'X':0})

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, mr_x())
