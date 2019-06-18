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

def evaluate(E, curr, lookup):
    left, operator, right = None, None, None
    while curr[0] != len(E) and E[curr[0]] != ")":
        if E[curr[0]] in lookup:
            if left is None:
                left = lookup[E[curr[0]]]
            else:
                right = lookup[E[curr[0]]]
            curr[0] += 1
        elif E[curr[0]] == '(':
            curr[0] += 1
            tmp = evaluate(E, curr, lookup)
            if left is None:
                left = tmp
            else:
                right = tmp
        else:
            operator = E[curr[0]]
            curr[0] += 1
 
    if curr[0] != len(E) and E[curr[0]] == ")":
        curr[0] += 1
    return calc(operator, left, right) if operator else left

def mr_x():
    E = raw_input()
    return evaluate(E, [0], {'0':0, '1':1, 'x':0 ,'X':1}) ^ \
           evaluate(E, [0], {'0':0, '1':1, 'x':1 ,'X':0})

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, mr_x())
