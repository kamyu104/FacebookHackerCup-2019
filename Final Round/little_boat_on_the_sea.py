# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round - Little Boat on the Sea
# https://www.facebook.com/hackercup/problem/1956356724467896/
#
# Time:  O(NlogN)
# Space: O(NlogN), due to skip-list of tree node ancestors
#

from collections import defaultdict
from functools import partial

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2018/blob/master/Round%202/fossil_fuels.py
class SegmentTree(object):
    def __init__(self, N,
                 build_fn=lambda x, y: [y]*(2*x),
                 query_fn=min,
                 update_fn=lambda x, y: y,
                 default_val=float("inf")):
        self.N = N
        self.H = (N-1).bit_length()
        self.query_fn = query_fn
        self.update_fn = update_fn
        self.default_val = default_val
        self.tree = build_fn(N, default_val)
        self.lazy = [None]*N

    def __apply(self, x, val):
        self.tree[x] = self.update_fn(self.tree[x], val)
        if x < self.N:
            self.lazy[x] = self.update_fn(self.lazy[x], val)

    def update(self, L, R, h):  # Time: O(logN), Space: O(N)
        def pull(x):
            while x > 1:
                x //= 2
                self.tree[x] = self.query_fn(self.tree[x*2], self.tree[x*2+1])
                if self.lazy[x] is not None:
                    self.tree[x] = self.update_fn(self.tree[x], self.lazy[x])
        L += self.N
        R += self.N
        L0, R0 = L, R
        while L <= R:
            if L & 1:  # is right child
                self.__apply(L, h)
                L += 1
            if R & 1 == 0:  # is left child
                self.__apply(R, h)
                R -= 1
            L //= 2
            R //= 2
        pull(L0)
        pull(R0)

    def query(self, L, R):  # Time: O(logN), Space: O(N)
        def push(x):
            n = 2**self.H
            while n != 1:
                y = x // n
                if self.lazy[y] is not None:
                    self.__apply(y*2, self.lazy[y])
                    self.__apply(y*2 + 1, self.lazy[y])
                    self.lazy[y] = None
                n //= 2

        result = self.default_val
        if L > R:
            return result

        L += self.N
        R += self.N
        push(L)
        push(R)
        while L <= R:
            if L & 1:  # is right child
                result = self.query_fn(result, self.tree[L])
                L += 1
            if R & 1 == 0:  # is left child
                result = self.query_fn(result, self.tree[R])
                R -= 1
            L //= 2
            R //= 2
        return result
    
    def __str__(self):
        showList = []
        for i in xrange(self.N):
            showList.append(self.query(i, i))
        return ",".join(map(str, showList))

def find_tree_infos(N, E):
    def preprocess(L, D, P, C, curr, parent):
        # depth of the node i
        D[curr] = 1 if parent == -1 else D[parent]+1
        # ancestors of the node i
        P[curr].append(parent)
        i = 0
        while P[curr][i] != -1:
            P[curr].append(P[P[curr][i]][i] if i < len(P[P[curr][i]]) else -1)
            i += 1
        # the subtree of the node i is represented by traversal index L[i]..R[i]
        C[0] += 1
        L[curr] = C[0]

    def divide(stk, L, R, D, P, C, curr, parent):
        stk.append(partial(postprocess, R, C, curr))
        for i in reversed(xrange(len(E[curr]))):
            child = E[curr][i]
            if child == parent:
                continue
            stk.append(partial(divide, stk, L, R, D, P, C, child, curr))
        stk.append(partial(preprocess, L, D, P, C, curr, parent))

    def postprocess(R, C, curr):
        R[curr] = C[0]

    L, R, D, P, C = [0]*N, [0]*N, [0]*N, [[] for _ in xrange(N)], [-1]
    stk = []
    stk.append(partial(divide, stk, L, R, D, P, C, 0, -1))
    while stk:
        stk.pop()()
    assert(C[0] == N-1)
    return L, R, D, P

def find_invalidated_rectangles(N, A, L, R, D, P):
    def is_ancestor(L, R, a, b):  # includes itself
        return L[a] <= L[b] <= R[b] <= R[a]

    def find_ancestor_with_depth(P, curr, d):
        i, pow_i_of_2 = 0, 1
        while pow_i_of_2 <= d:
            if d & pow_i_of_2:
                curr = P[curr][i]
            i += 1
            pow_i_of_2 *= 2
        return curr

    def add_rectangle(l1, r1, l2, r2, O, C):
        O[l1].append((l2, r2))
        C[r1+1].append((l2, r2))
        O[l2].append((l1, r1))
        C[r2+1].append((l1, r1))

    O, C = defaultdict(list), defaultdict(list)
    for Ai in A.itervalues():
        if len(Ai) != 2:
            continue
        a, b = Ai
        if is_ancestor(L, R, b, a):
            a, b = b, a
        if is_ancestor(L, R, a, b):
            c = find_ancestor_with_depth(P, b, D[b]-D[a]-1)
            assert(P[c][0] == a)
            assert(is_ancestor(L, R, c, b))
            if 0 <= L[c]-1:
                add_rectangle(L[b], R[b], 0, L[c]-1, O, C)
            if R[c]+1 <= N-1:
                add_rectangle(L[b], R[b], R[c]+1, N-1, O, C)
        else:  # a, b are disjoint
            add_rectangle(L[a], R[a], L[b], R[b], O, C)
    return O, C  # open intervals and close intervals of the invalidated rectangles

def line_sweep(N, O, C):
    def build_fn(N, default_val):
        # tree[x]: [minimum number of rectangles covering any of the cells in its interval,
        #           the number of cells covered by that minimum number of rectangles]
        tree = [None]*(2*N)
        for x in reversed(xrange(1, len(tree))):
            tree[x] = [0, 1 if x >= N else tree[x*2][1]+tree[x*2+1][1]]
        return tree

    def query_fn(x, y):
        if x[0] != y[0]:
            return min(x, y)
        return [x[0], x[1]+y[1]]

    def update_fn(x, y):
        if x is None:
            return y
        return [x[0]+y[0], x[1]]

    result = 0
    segment_tree = SegmentTree(N, build_fn, query_fn, update_fn, [float("inf"), None])
    for i in xrange(N+1):
        if i in O:
            for l, r in O[i]:
                segment_tree.update(l, r, [+1, None])
        if i in C:
            for l, r in C[i]:
                segment_tree.update(l, r, [-1, None])
        rmq = segment_tree.query(0, N-1)
        assert(rmq[0] == 0)
        if i < N:
            result += rmq[1]
        else:
            assert(rmq[1] == N)
    return result-N  # discounting the path from each node to itself

def little_boat_on_the_sea():
    N = input()
    A = defaultdict(list)
    for i in xrange(N):
        Ai = raw_input().strip()
        if Ai == "-":
            continue
        A[Ai].append(i)
    E = defaultdict(list)
    for _ in xrange(N-1):
        u, v = map(int, raw_input().strip().split())
        E[u-1].append(v-1)
        E[v-1].append(u-1)

    L, R, D, P = find_tree_infos(N, E)
    O, C = find_invalidated_rectangles(N, A, L, R, D, P)
    return line_sweep(N, O, C)

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, little_boat_on_the_sea())
