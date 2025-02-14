# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Renovations
# https://www.facebook.com/hackercup/problem/2038302866474992/
#
# Time:  O(NlogK)
# Space: O(N)
#

def add(a, b):
    return (a + b) % MOD

def sub(a, b):
    return (a - b) % MOD

def mul(a, b):
    return (a * b) % MOD

def div(a, b):
    # Euler's Theorem: x^(p - 1) mod p = 1
    # For p prime, the inverse of any number x mod p is x^(p - 2) mod p.
    def inv(x):
        return pow(x, MOD-2, MOD)

    return mul(a, inv(b))

def renovations():
    N, K, A, B = map(int, raw_input().strip().split())
    A -= 1
    B -= 1
    P = [-1]*N
    for i in xrange(1, N):
        P[i] = input()-1

    lookup = [0]*N
    result = 0
    for i in [A, B]:
        EXP_D = 0
        c = 0
        while i:
            EXP_D = add(EXP_D, pow(div(N-1-c, N-1), K, MOD))
            lookup[i] += 1
            i = P[i]
            c += 1
        result = add(result, EXP_D)

    count = [0]*3
    for i in xrange(N):
        count[lookup[i]] += 1
    EXP_D_L = 0
    for c in xrange(count[2]):
        EXP_D_L = add(EXP_D_L, pow(div(N-1-count[1]-c, N-1), K, MOD))
    result = sub(result, 2*EXP_D_L)
    return result  # result = E(D(A)) + E(D(B)) - 2*E(D(L))

MOD = 10**9+7
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, renovations())