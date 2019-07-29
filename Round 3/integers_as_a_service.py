# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Integers as a Service
# https://www.facebook.com/hackercup/problem/367172063898266/
#
# Time:  O(NlogN)
# Space: O(1)
#

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def lcm(a, b):
    return a // gcd(a, b) * b

def integers_as_a_service():
    N = input()
    O_V_R = []
    for _ in xrange(N):
        O_V_R.append(raw_input().strip().split())
        O_V_R[-1][1] = int(O_V_R[-1][1])
        O_V_R[-1][2] = int(O_V_R[-1][2])

    X = 1
    for O, V, R in O_V_R:  # find min candidate of X
        if O != 'G':
            continue
        X = lcm(X, R)
        if X > LIMIT:
            return -1

    for _ in xrange(2):  # make X satisfy lcm requirements and check them again
        for O, V, R in O_V_R:
            if O != 'L':
                continue
            curr = lcm(X, V)
            if R % curr:
                return -1
            if R != curr:
                X *= R // curr
                if X > LIMIT:
                    return -1

    for O, V, R in O_V_R:  # check gcd requirements again
        if O != 'G':
            continue
        if gcd(X, V) != R:
            return -1
    return X

LIMIT = 10**9
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, integers_as_a_service())