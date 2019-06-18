# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Qualification Round - Mr. X
# https://www.facebook.com/hackercup/problem/589264531559040/
#
# Time:  O(E)
# Space: O(E)
#

def calc(operator, x, y):
    if operator == '&':
        return x & y
    elif operator == '|':
        return x | y
    return x ^ y

def evaluate(E, curr):
    left, operator, right = None, None, None
    while curr[0] != len(E) and E[curr[0]] != ")":
        if E[curr[0]] in ('0', '1'):
            if left is None:
                left = int(E[curr[0]])
            else:
                right = int(E[curr[0]])
            curr[0] += 1
        elif E[curr[0]] == '(':
            curr[0] += 1
            tmp = evaluate(E, curr)
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
    return evaluate(E.replace('x', '0').replace('X', '1'), [0]) ^ \
           evaluate(E.replace('x', '1').replace('X', '0'), [0])

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, mr_x())
