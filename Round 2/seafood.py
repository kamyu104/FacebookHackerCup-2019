# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 2 - Seafood
# https://www.facebook.com/hackercup/problem/404425766835121/
#
# Time:  O(NlogN)
# Space: O(N)
#

from bisect import bisect_left
           
def seafood():
    N = input()
    G = [[None for _ in xrange(N)] for _ in xrange(2)]
    for i in xrange(2):
        G[i][0], G[i][1], A, B, C, D = map(int, raw_input().strip().split())
        for j in xrange(2, N):
            G[i][j] = (A*G[i][j-2] + B*G[i][j-1] + C) % D + 1
    O = raw_input().strip()

    P = sorted((G[0][i], (O[i], G[1][i])) for i in xrange(N))
    C = []
    for i in xrange(N):
        if P[i][1][0] == 'C':
            C.append(i)
    st = []
    for i in reversed(xrange(C[-1])):
        if (P[i][1][0] == 'R') and (not st or (P[i][1][1] > st[-1][0])):
            st.append((P[i][1][1], P[i][0]))
    B = [-1]*len(C)
    for i in xrange(len(C)):
        j = bisect_left(st, (P[C[i]][1][1]+1, 0))
        if j == len(st):
            break
        B[i] = st[j][1]
    sufCB = [float("inf")]*(len(C)+1)
    sufCH = [float("-inf")]*(len(C)+1)
    for i in reversed(xrange(len(C))):
        sufCB[i] = min(sufCB[i+1], B[i])
        sufCH[i] = max(sufCH[i+1], P[C[i]][1][1])
    fr = []
    for i in xrange(C[-1]+1, N):
        if not fr or P[i][1][1] > fr[-1][0]:
            fr.append((P[i][1][1], P[i][0]))

    result = float("inf")
    st = []
    for i in xrange(len(C)):
        if not i:
            d = 0
        else:
            p = P[C[i-1]][0]
            while len(st) > 1:
                a = st[-1][1]
                b = min(a, st[-2][1])
                if st[-1][0] + 2*max(0, p-a) < st[-2][0] + 2*max(0, p-b):
                    break
                st[-2][1] = b
                st.pop()
            d = st[-1][0] + 2*max(0, p-st[-1][1])
        st.append([d, B[i]])
        p = P[C[-1]][0]
        if sufCB[i] >= 0:
           result =  min(result, d+max(0, p-sufCB[i]))
        a = bisect_left(fr, (sufCH[i]+1, 0))
        if a < len(fr):
            result = min(result, d+(fr[a][1]-p))
        if B[i] < 0:
            break
    return -1 if result == float("inf") else result + P[C[-1]][0]

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, seafood())