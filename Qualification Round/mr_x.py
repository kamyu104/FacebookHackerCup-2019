# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Qualification Round - Mr. X
# https://www.facebook.com/hackercup/problem/589264531559040/
#
# Time:  O(E)
# Space: O(D), D is the depth of expression
#

def mr_x():
    E = raw_input()
    return eval(E.replace('x', '0').replace('X', '1')) ^ \
           eval(E.replace('x', '1').replace('X', '0'))

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, mr_x())
