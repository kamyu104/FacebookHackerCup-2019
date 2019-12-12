# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Final Round - Temporal Revision
# https://www.facebook.com/hackercup/problem/1165177510537433/
#
# Time:  O((S + N)logN + (M + K) * (log*)(N)), p.s. (log*)(N) <= 5
# Space: O(NlogN), due to skip-list of tree node ancestors
#

from collections import defaultdict
from functools import partial

# Template:
# https://github.com/kamyu104/LeetCode-Solutions/blob/master/Python/accounts-merge.py
class UnionFind(object):
    def __init__(self, n):
        self.set = range(n)

    def get_id(self):
        self.set.append(len(self.set))
        return len(self.set)-1

    def find_set(self, x):
        stk = []
        while self.set[x] != x:  # path compression.
            stk.append(x)
            x = self.set[x]
        while stk:
            self.set[stk.pop()] = x
        return x

    def union_set(self, x, y):
        x_root, y_root = map(self.find_set, (x, y))
        if x_root == y_root:
            return False
        self.set[min(x_root, y_root)] = max(x_root, y_root)
        return True

# Template:
# https://github.com/kamyu104/FacebookHackerCup-2019/blob/master/Final%20Round/little_boat_on_the_sea.py
def find_binary_tree_infos(N, children):
    def preprocess(L, P, C, curr, parent):
        # ancestors of the node i
        P[curr].append(parent)
        i = 0
        while P[curr][i] != -1:
            P[curr].append(P[P[curr][i]][i] if i < len(P[P[curr][i]]) else -1)
            i += 1
        # the subtree of the node i is represented by traversal index L[i]..R[i]
        C[0] += 1
        L[curr] = C[0]

    def divide(stk, L, R, P, C, curr, parent):
        stk.append(partial(postprocess, R, C, curr))
        for i in reversed(xrange(len(children[curr]))):
            child = children[curr][i]
            stk.append(partial(divide, stk, L, R, P, C, child, curr))
        stk.append(partial(preprocess, L, P, C, curr, parent))

    def postprocess(R, C, curr):
        R[curr] = C[0]

    L, R, P, C = [0]*N, [0]*N, [[] for _ in xrange(N)], [-1]
    stk = []
    stk.append(partial(divide, stk, L, R, P, C, N-1, -1))  # root is the last node id: N-1
    while stk:
        stk.pop()()
    return L, R, P

def build_binary_tree(N, A, B, E, V, activity_type):
    union_find = UnionFind(N)
    children = defaultdict(list)
    when = defaultdict(lambda x: len(E))
    curr_active_cnt_from_node = defaultdict(int)
    for i in xrange(N):
        curr_active_cnt_from_node[i] = int(activity_type[i] == OPEN)
    dp1, dp2 = defaultdict(int), defaultdict(int)
    for i in reversed(xrange(len(E))):  # O((M+K)*alpha(N))
        q = V[i]
        if E[i] == 1:
            x, y = union_find.find_set(A[q]), union_find.find_set(B[q])
            if x == y:
                continue
            v = union_find.get_id()
            union_find.union_set(v, x), union_find.union_set(v, y)
            children[v], when[v] = [x, y], i
            curr_active_cnt_from_node[v] = curr_active_cnt_from_node[x] + curr_active_cnt_from_node[y]
            dp1[v] = max(dp1[x], dp1[y])
            dp2[v] = max(dp2[x], dp2[y], dp1[x]+dp1[y])
        else:
            v, x = union_find.get_id(), union_find.find_set(q)
            union_find.union_set(v, x)
            children[v], when[v] = [x], i
            curr_active_cnt_from_node[v] = curr_active_cnt_from_node[x] + (-1 if E[i] == 2 else 1)  # -1 means not yet activated, +1 means activated
            dp1[v] = int(E[i] == 2) + dp1[x]
            dp2[v] = int(E[i] == 2) + dp2[x]
    return len(union_find.set), children, when, curr_active_cnt_from_node, dp1, dp2

def query_binary_tree(E, V, end_hr, children, when, curr_active_cnt_from_node, dp1, dp2, L, R, P, X, Y):
    def is_ancestor(L, R, a, b):  # includes itself
        return L[a] <= L[b] <= R[b] <= R[a]

    v = X
    for i in reversed(xrange(len(P[v]))):  # O(logN)
        if i < len(P[v]) and P[v][i] != -1 and when[P[v][i]] >= Y:
            v = P[v][i]
    stk = [v]
    while P[v][0] != -1:  # O(1)
        v = P[v][0]
        if when[v] < Y-24:
            break
        stk.append(v)
    stk = stk[::-1]
    assert(len(stk) <= 25)
    active_cnt_to_the_end_from_hr = [0]*len(stk)
    accumulated_cnt = dp1[stk[-1]]
    for i in reversed(xrange(len(stk)-1)):
        active_cnt_to_the_end_from_hr[i] = accumulated_cnt
        h = when[stk[i]]
        if E[h] == 2 and end_hr[V[h]] >= Y and is_ancestor(L, R, stk[-1], V[h]):
            accumulated_cnt += 1
    max_cnt, curr_cnt = 0, curr_active_cnt_from_node[stk[0]]
    for i in xrange(len(stk)-1):
        h = when[stk[i]]
        curr_cnt += int(E[h] == 2)
        if len(children[stk[i]]) == 2:
            other_sibling = children[stk[i]][0] if children[stk[i]][0] != stk[i+1] else children[stk[i]][1]
            max_cnt = max(max_cnt, curr_cnt + dp1[other_sibling] + active_cnt_to_the_end_from_hr[i])
    return max(max_cnt, curr_cnt + dp2[stk[-1]])

def temporal_revision():
    N, M, K, S = map(int, raw_input().strip().split())
    A, B = [0]*M, [0]*M
    E, V = [0]*K, [0]*K
    for i in xrange(M):
        A[i], B[i] = map(int, raw_input().strip().split())
        A[i], B[i] = A[i]-1, B[i]-1
    activity_type, is_collapsed, end_hr = [0]*N, [False]*M, [0]*N
    for i in xrange(K):
        E[i], V[i] = map(int, raw_input().strip().split())
        V[i] -= 1
        if E[i] == 1:
            is_collapsed[V[i]] = True
        elif E[i] == 2:
            activity_type[V[i]] |= OPEN
        else:  # E[i] == 3
            activity_type[V[i]] |= CLOSE
            end_hr[V[i]] = i
    for i in xrange(M):  # make remaining conduit split into only one planet
        if is_collapsed[i] == False:
            E.append(1), V.append(i)
    for i in xrange(N):
        if activity_type[i] == OPEN:
            end_hr[i] = len(E)  # set the max time to end activity

    node_count, children, when, curr_active_cnt_from_node, dp1, dp2 = build_binary_tree(N, A, B, E, V, activity_type)
    L, R, P = find_binary_tree_infos(node_count, children)
    result, ans = 0, 0
    for _ in xrange(S):
        X, Y = map(int, raw_input().strip().split())
        X, Y = X^ans, Y^ans
        assert(1 <= X <= N and 1 <= Y <= K)
        X, Y = X-1, Y-1
        ans = query_binary_tree(E, V, end_hr,
                                children, when, curr_active_cnt_from_node, dp1, dp2,
                                L, R, P, X, Y)
        result += ans
    return result

OPEN, CLOSE = range(1, 3)
for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, temporal_revision())
