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
        self.__children = adj
        self.__parent = [-1]*len(adj)  # Space: O(N)
        self.__size = [-1]*len(adj)
        self.__left = [-1]*len(adj)
        self.__right = [-1]*len(adj)
        self.__chain = [-1]*len(adj)

        for parent, children in enumerate(adj):
            for c in children:
                self.__parent[c] = parent
        self.__chain[root] = root
        self.__find_heavy_light(root)
        self.__decompose(root)

    def __find_heavy_light(self, i):  # Time: O(N)
        self.__size[i] = 1
        for j in xrange(len(self.__children[i])):
            c = self.__children[i][j]
            self.__find_heavy_light(c)
            self.__size[i] += self.__size[c]
            if self.__size[c] > self.__size[self.__children[i][0]]:
                self.__children[i][0], self.__children[i][j] = self.__children[i][j], self.__children[i][0]  # put heavy idx in children[i][0]

    def __decompose(self, i):  # Time: O(N)
        self.__left[i] = self.__idx
        self.__idx += 1
        for j in xrange(len(self.__children[i])):
            c = self.__children[i][j]
            self.__chain[c] = c if j > 0 else self.__chain[i]  # create a new chain if not heavy
            self.__decompose(c)
        self.__right[i] = self.__idx

    def children(self, i):
        return self.__children[i]

    def parent(self, i):
        return self.__parent[i]

    def left(self, i):
        return self.__left[i]

    def right(self, i):
        return self.__right[i]

    def chain(self, i):
        return self.__chain[i]

class BIT(object):  # Fenwick Tree
    def __init__(self, n):
        self.__bit = [0] * n  # Space: O(N)

    def add(self, i, val):  # Time: O(logN)
        i += 1
        while i < len(self.__bit):
            self.__bit[i] += val
            i += (i & -i)

    def query(self, i):  # Time: O(logN)
        ret = 0
        i += 1
        while i > 0:
            ret += self.__bit[i]
            i -= (i & -i)
        return ret

def query_X_to_root(i, hld, bit_X):
    count = 1
    while i >= 0:  # Time: O((logN)^2), O(logN) queries with O(logN) costs
        j = hld.chain(i)  # find head of chain
        count = add(count, bit_X.query(hld.left(i))-bit_X.query(hld.left(j)-1))
        i = hld.parent(j)  # move to parent chain
    return count

def query_B_in_subtree(i, hld, bit_B):
    return bit_B.query(hld.right(i)-1)-bit_B.query(hld.left(i)-1)

def set_X(i, hld, bit_B, bit_X, lookup_X):
    if i in lookup_X:
        return 0
    lookup_X.add(i)
    bit_X.add(hld.left(i), 1)
    return query_B_in_subtree(i, hld, bit_B)

def bribe(i, hld, bit_B, bit_X, lookup_X, lookup_upward):
    result = 0
    bit_B.add(hld.left(i), 1)  # set B to i
    result = add(result, query_X_to_root(i, hld, bit_X))  # Time: O((logN)^2)
    for j in xrange(len(hld.children(i))):  # set X to children of i
        result = add(result, set_X(hld.children(i)[j], hld, bit_B, bit_X, lookup_X))
    while i not in lookup_upward:  # set X to siblings of i and upwards
        lookup_upward.add(i)  # avoid duplicated upward
        p = hld.parent(i)
        if p < 0:
            break
        for j in xrange(len(hld.children(p))):
            if hld.children(p)[j] != i:  # siblings of current i
                result = add(result, set_X(hld.children(p)[j], hld, bit_B, bit_X, lookup_X))
        i = p
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