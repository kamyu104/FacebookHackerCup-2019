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
        self.__adj = [list(c) for c in adj]  # Space: O(N)
        self.__parent = [-1]*len(adj)
        self.__size = [-1]*len(adj)
        self.__left = [-1]*len(adj)
        self.__right = [-1]*len(adj)
        self.__nxt = [-1]*len(adj)

        for parent, children in enumerate(adj):
            for c in children:
                self.__parent[c] = parent
        self.__nxt[root] = root
        self.__find_heavy_light(root)
        self.__decompose(root)

    def __find_heavy_light(self, i):  # Time: O(N)
        self.__size[i] = 1
        for j in xrange(len(self.__adj[i])):
            c = self.__adj[i][j]
            self.__find_heavy_light(c)
            self.__size[i] += self.__size[c]
            if self.__size[c] > self.__size[self.__adj[i][0]]:
                self.__adj[i][0], self.__adj[i][j] = self.__adj[i][j], self.__adj[i][0]  # put heavy idx in adj[i][0]

    def __decompose(self, i):  # Time: O(N)
        self.__left[i] = self.__idx
        self.__idx += 1
        for j in xrange(len(self.__adj[i])):
            c = self.__adj[i][j]
            self.__nxt[c] = c if j > 0 else self.__nxt[i]  # new chain if not heavy
            self.__decompose(c)
        self.__right[i] = self.__idx

    def adj(self, i):
        return self.__adj[i]

    def parent(self, i):
        return self.__parent[i]

    def left(self, i):
        return self.__left[i]

    def right(self, i):
        return self.__right[i]

    def nxt(self, i):
        return self.__nxt[i]

class BIT(object):  # Fenwick Tree
    def __init__(self, n):
        self.__bit = [0] * n  # Space: O(N)

    def add(self, i, val):  # Time: O(logN)
        while i < len(self.__bit):
            self.__bit[i] += val
            i += (i & -i)

    def query(self, i):  # Time: O(logN)
        ret = 0
        while i > 0:
            ret += self.__bit[i]
            i -= (i & -i)
        return ret

def query_X_to_root(i, hld, bit_X):
    count = 1
    while i >= 0:  # Time: O((logN)^2), O(logN) queries with O(logN) costs
        j = hld.nxt(i)
        count = add(count, bit_X.query(hld.left(i)+1)-bit_X.query(hld.left(j)))
        i = hld.parent(j)
    return count

def query_B_in_subtree(i, hld, bit_B):
    return bit_B.query(hld.right(i))-bit_B.query(hld.left(i))

def set_X(i, hld, bit_B, bit_X, lookup_X):
    if i in lookup_X:
        return 0
    lookup_X.add(i)
    bit_X.add(hld.left(i)+1, 1)
    return query_B_in_subtree(i, hld, bit_B)

def bribe(i, hld, bit_B, bit_X, lookup_X, lookup_upward):
    result = 0
    bit_B.add(hld.left(i)+1, 1)  # set B to i
    result = add(result, query_X_to_root(i, hld, bit_X))  # Time: O((logN)^2)
    for j in xrange(len(hld.adj(i))):  # set X to children of i
        result = add(result, set_X(hld.adj(i)[j], hld, bit_B, bit_X, lookup_X))
    while i not in lookup_upward:  # set X to siblings of i and upwards
        lookup_upward.add(i)  # avoid duplicated upward
        c = hld.parent(i)
        if c < 0:
            break
        for j in xrange(len(hld.adj(c))):
            if hld.adj(c)[j] != i:
                result = add(result, set_X(hld.adj(c)[j], hld, bit_B, bit_X, lookup_X))
        i = c
    return result

def chain_of_command():
    N = input()
    adj = [[] for _ in xrange(N)]
    for i in xrange(N):
        C = input()-1
        if C < 0:
            root = i
        else:
            adj[C].append(i)

    hld = HLD(root, adj)
    bit_B, bit_X = BIT(N+1), BIT(N+1)
    lookup_X, lookup_upward = set(), set()
    result, curr = 1, 0
    for i in xrange(N):
        curr = add(curr, bribe(i, hld, bit_B, bit_X, lookup_X, lookup_upward))
        result = mul(result, curr)
    return result

MOD = 10**9+7
setrecursionlimit(800000+2)  # ulimit -S -s unlimited
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, chain_of_command())