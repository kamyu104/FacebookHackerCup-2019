# Copyright (c) 2019 kamyu. All rights reserved.
#
# Facebook Hacker Cup 2019 Round 2 - On the Run
# https://www.facebook.com/hackercup/problem/432000547357525/
#
# Time:  O(1)
# Space: O(1)
#
            
def on_the_run():
    N, M, K = map(int, raw_input().strip().split())
    lookup = set()
    for _ in xrange(K+1):
        lookup.add(sum(map(int, raw_input().strip().split())) % 2)

    return "Y" if K == 2 and len(lookup) == 1 else "N"

for case in xrange(input()):
    print 'Case #%d: %s' % (case+1, on_the_run())