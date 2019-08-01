# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 3 - Chain of Command
# https://www.facebook.com/hackercup/problem/427797291330788/
#
# Time:  O(N * (logN)^2), may happen segmentation fault due to high depth of recursion
# Space: O(N)
#

from sys import setrecursionlimit

def add(a, b):
    return (a + b) % MOD

def mul(a, b):
    return (a * b) % MOD

class HLD(object):  # Heavy-Light Decomposition
    def __init__(self, root, adj):
        self.__idx = 0
        self.__adj = [list(c) for c in adj]
        self.__size = [-1]*len(adj)
        self.__left = [-1]*len(adj)
        self.__right = [-1]*len(adj)
        self.__nxt = [-1]*len(adj)

        self.__nxt[root] = root
        self.__find_heavy_light(root)
        self.__decompose(root)

    def __find_heavy_light(self, i):
        self.__size[i] = 1
        for j in xrange(len(self.__adj[i])):
            c = self.__adj[i][j]
            self.__find_heavy_light(c)
            self.__size[i] += self.__size[c]
            if self.__size[c] > self.__size[self.__adj[i][0]]:
                self.__adj[i][0], self.__adj[i][j] = self.__adj[i][j], self.__adj[i][0]

    def __decompose(self, i):
        self.__left[i] = self.__idx
        self.__idx += 1
        for j in xrange(len(self.__adj[i])):
            c = self.__adj[i][j]
            self.__nxt[c] = c if j > 0 else self.__nxt[i]  # new chain if not heavy
            self.__decompose(c)
        self.__right[i] = self.__idx

    def nxt(self, i):
        return self.__nxt[i]

    def left(self, i):
        return self.__left[i]

    def right(self, i):
        return self.__right[i]

class BIT(object):  # Fenwick Tree
    def __init__(self, n):
        self.__bit = [0] * n

    def add(self, i, val):
        while i < len(self.__bit):
            self.__bit[i] += val
            i += (i & -i)

    def query(self, i):
        ret = 0
        while i > 0:
            ret += self.__bit[i]
            i -= (i & -i)
        return ret

def query_X_to_root(C, i, hld, bit_X):
    count = 1
    while i >= 0:
        j = hld.nxt(i)
        count = add(count, bit_X.query(hld.left(i)+1)-bit_X.query(hld.left(j)))
        i = C[j]
    return count

def query_B_in_subtree(i, hld, bit_B):
    return bit_B.query(hld.right(i))-bit_B.query(hld.left(i))

def set_X(i, hld, bit_B, bit_X, lookup_X):
    if i in lookup_X:
        return 0
    lookup_X.add(i)
    bit_X.add(hld.left(i)+1, 1)
    return query_B_in_subtree(i, hld, bit_B)

def bribe(C, i, adj, hld, bit_B, bit_X, lookup_X, lookup_upward):
    result = 0
    bit_B.add(hld.left(i)+1, 1)  # set B to i
    result = add(result, query_X_to_root(C, i, hld, bit_X))
    for j in xrange(len(adj[i])):  # set X to children
        result = add(result, set_X(adj[i][j], hld, bit_B, bit_X, lookup_X))
    while i not in lookup_upward:  # set X to siblings and upward siblings
        lookup_upward.add(i)  # avoid duplicated upward
        c = C[i]
        if c < 0:
            break
        for j in xrange(len(adj[c])):
            if adj[c][j] != i:
                result = add(result, set_X(adj[c][j], hld, bit_B, bit_X, lookup_X))
        adj[c] = [i]  # remaining node without X
        i = c
    return result

def chain_of_command():
    N = input()
    C = [0]*N
    adj = [[] for _ in xrange(N)]
    for i in xrange(N):
        C[i] = input()-1
        if C[i] < 0:
            root = i
        else:
            adj[C[i]].append(i)
    hld = HLD(root, adj)
    bit_B, bit_X = BIT(N+1), BIT(N+1)
    lookup_X, lookup_upward = set(), set()
    result = 1
    curr = 0
    for i in xrange(N):
        curr = add(curr, bribe(C, i, adj, hld, bit_B, bit_X, lookup_X, lookup_upward))
        result = mul(result, curr)
    return result

MOD = 10**9+7
setrecursionlimit(800000+2)  # ulimit -S -s unlimited
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, chain_of_command())