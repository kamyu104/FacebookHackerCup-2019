# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Qualification Round - Trees as a Service
# https://www.facebook.com/hackercup/problem/330920680938986/
#
# Time:  O(N^2 * (N + M))
# Space: O(N)
#

from collections import defaultdict

def make_root(LCAs, root, tree_set, not_neighbors, neighbors):
    for X, Y, Z in LCAs:
        if not (X in tree_set and Y in tree_set and Z in tree_set):
            continue
        if X == root or Y == root:
            if Z != root:
                return False
        elif Z == root:
            not_neighbors[X].add(Y)
            not_neighbors[Y].add(X)
        else:
            neighbors[X].add(Y)
            neighbors[Y].add(X)
            neighbors[X].add(Z)
            neighbors[Z].add(X)
    return True

def make_subtree(LCAs, root, tree, not_neighbors, neighbors, subtrees):
    lookup = set([root])
    for node in tree:
        if node in lookup:
            continue
        subtree = []
        stk = [node]
        lookup.add(node)
        while stk:
            node = stk.pop()
            subtree.append(node)
            for neighbor in neighbors[node]:
                if neighbor not in lookup:
                    stk.append(neighbor)
                    lookup.add(neighbor)
        for i in xrange(len(subtree)):
            for j in xrange(i):
                if subtree[j] in not_neighbors[subtree[i]]:
                    return False
        subtrees.append(subtree)
    return True

def trees_as_a_service_helper(LCAs, parent, tree, result):  # at most visit N times => Time: N * N * O(M + N) = O(N^2 * (N + M))
    tree_set = set(tree)
    for root in tree:  # at most N times
        not_neighbors, neighbors = defaultdict(set), defaultdict(set)
        if not make_root(LCAs, root, tree_set, not_neighbors, neighbors):  # Time: O(M)
            continue
        subtrees = []
        if not make_subtree(LCAs, root, tree, not_neighbors, neighbors, subtrees):  # Time: O(N)
            continue
        result[root] = parent
        for subtree in subtrees:
            if not trees_as_a_service_helper(LCAs, root, subtree, result):
                return False  # make trees_as_a_service_helper called at most N times
        return True
    return False

def trees_as_a_service():
    N, M = map(int, raw_input().strip().split())
    LCAs = []
    for _ in xrange(M):
        X, Y, Z = map(int, raw_input().strip().split())
        LCAs.append((X-1, Y-1, Z-1))

    result = [-1]*N
    if trees_as_a_service_helper(LCAs, -1, range(N), result):
        return " ".join(map(lambda x: str(x+1), result))
    return "Impossible"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, trees_as_a_service())
